
from os.path import join, exists
from os import makedirs as mkdir
from csv import writer as csv_writer
from pprint import pprint as pp


####

def setupDirs( baseDir ):
    sld = join( baseDir, 'spot_logs' )
    if not exists(sld):
        mkdir(sld)

    # Put camera logs in their own dir
    cld = join( baseDir, 'camera_logs' )
    if not exists(cld):
        mkdir(cld)

    # Put camera states in their own dir
    csd = join( baseDir, 'camera_states' )
    if not exists(csd):
        mkdir(csd)
    
    return sld, cld, csd


def logSpot( spot, logDir ):
    
    # Log spot data
    data = ( [spot.imageTimeStamp, spot.tPresent] 
             + [spot.nEdges] )

    fname = 'spot' + str(spot.number) + '.log'
    ffname = join( logDir, fname )
    if not exists(logDir):
        mkdir( logDir )
    with open(ffname,'a+') as l:
        w = csv_writer(l)
        w.writerow(data)
    
    return

def addState( camera, logDir ):
    
    # append the state to the log
    fname = 'camera' + str(camera['number']) + '_dict.log'
    ffname = join(logDir,fname)
    if not exists(logDir):
        mkdir( logDir )
    with open(ffname,'a+') as out:
        pp( camera, stream=out )
    
    return

def recordState( camera, logDir ):

    # store the current state of the camera
    fname = 'camera' + str(camera['number']) + '.dict'
    ffname = join( logDir, fname )
    if not exists(logDir):
        mkdir( logDir )
    with open(ffname,'w+') as out:
        pp( camera, stream=out )
    
    return

