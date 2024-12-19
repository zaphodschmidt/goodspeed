
import requests
import time
from pprint import pprint as pp
from notifications import send_msg as sm
from os.path import exists, dirname
from os import makedirs as mkdir

class Payment:
    nApiFails = 0
    nJsFails = 0
    url = ''
    usr = ''
    pwd = ''
    key = ''
    log = ''
    notification_reception = ''

    
    def __init__(self, logfname, apicfg, to='' ):
        self.log = logfname
        self.pwd = apicfg['pwd']
        self.usr = apicfg['usr']
        self.url = apicfg['url']
        self.key = apicfg['key']
        self.notification_receiver = to


    def update( self, spots ):

        i = 0
        resp = None
        headers={'x-api-key':self.key,
                 'Authorization':'api_key'}
        while True:
            try:
                resp = requests.get(self.url,
                                    auth=(self.usr,self.pwd),
                                    headers=headers,
                                    verify=True)
                
                # Success means no failures
                self.nApiFails = 0

                break
            except Exception, e:
                i += 1
                print 'BAD NEWS PARKMOBILE!'
                print 'Error number %d' % (i)
                print "Exception: \n%s" % str(e)
                if i==5:
                    msg = """
                    %s
                    Park Mobile API is not responding!
                    Error:
                    %s
                    """ % ( time.asctime(), str(e) )
                    sm('Error',msg,self.notification_receiver)
                    self.nApiFails += 1
                    if self.nApiFails > 5:
                        self.bad(spots,'API')
                        resp = None
                        #raise
                    break
        
        # If returns 401 then no spots are paid
        if resp.status_code == 401:
            return

        # Populate spots based on response
        if (resp is not None) and (resp.status_code != 404):
            i = 0
            while True:
                try:
                    # Read data
                    data = resp.json()
                    
                    # Log it
                    if not exists(dirname(self.log)):
                        mkdir(dirname(self.log))    
                    with open(self.log,'a') as out:
                        print >> out, time.asctime()
                        pp( data, stream=out )
                    
                    # Write it to spot object
                    self.assign( data, spots )
                    
                    # Success means no failures
                    self.nJsFails = 0

                    # Successful read, stop trying
                    break

                except Exception, e:
                    print "PM API returning crap JSON?"
                    print "Time: %s" % time.asctime()
                    print "Exception: \n%s" % str(e)
                    print "Response: \n%s" % resp.text
                    
                    i += 1
                    if i==5:
                        msg = """
                        Park Mobile API returning crap!
                        Time: %s
                        Exception: %s
                        Response: %s
                        """ % ( time.asctime(), str(e), resp.text )
                        sm('Error',msg,self.notification_receiver)
                        self.nJsFails += 1
                        if self.nJsFails > 5:
                            self.bad(spots,'CRAP')
                            #raise
                        break
        
        return




    def assign( self, data, spots ):
        
        # Set all spots as unpaid
        # App only returns info for paid spots
        for sn in spots:
            spots[ sn ].paid = 0

        # Check payments (if exist)
        if 'parkingRights' in data:
            
            # 
            paid = []
            for i in data['parkingRights']:

                # Get space number
                sn = int( i['spaceNumber'] )

                # Make sure space number is a valid spot
                if sn not in spots:
                    continue

                spots[ sn ].lpn = str(i['lpn'])
                spots[ sn ].lps = str(i['lpnState'])
                
                psstr = str(i['startDateLocal'])
                pestr = str(i['endDateLocal'])
                
                if psstr:
                    pstt = time.strptime(psstr[0:19],"%Y-%m-%dT%H:%M:%S")
                    pst = time.mktime(pstt)
                    spots[ sn ].payStartTime = pst
                if pestr:
                    pett = time.strptime(pestr[0:19],"%Y-%m-%dT%H:%M:%S")
                    pet = time.mktime(pett)
                    spots[ sn ].payEndTime = pet
                
                # Mark as paid if currently within paid window
                now = time.time()

                if now > spots[sn].payStartTime:
                    
                    if now < spots[sn].payEndTime:
                        spots[ sn ].paid = 1
                        paid += [sn]
            
            for s,spot in spots.iteritems():
                if s not in paid and not spot.monthly:
                    spot.paid = 0

        return

    def bad( self, spots, flavor ):
        for s,spot in spots.iteritems():
            if flavor is 'API':
                spot.paid = -1
            elif flavor is 'CRAP':
                spot.paid = -2
            else:
                spot.paid = -1000

        

