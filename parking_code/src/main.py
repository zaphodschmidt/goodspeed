#!/usr/bin/env python

from utils.Spot import Spot
from utils.Cam import Cam as Camera
from utils.Payment import Payment
from utils.notifications import send_msg as sm
from utils.Shift import determineEnforcers
import utils.dataRecording as log
import utils.table as table
from json import load as jl

import os
import time
import traceback
from sys import exit as quit

from copy import copy as copy

import ipdb


##########################################
##########################################
##########################################


sleepytime = 300

# Spot numbers is a list of ints
spotNumbers = range(1,50)

violationThresh = 1200

config_fname = '../cfg/cam_config.json'

#toForce = ['test@test.com']
toForce = [
    {'contact'  : 'test0@test.com',
     'shift'    : [0,24],
     'workdays' : [0, 1, 2, 3, 4]
    },
    {'contact': 'test1@test.com',
     'shift'  : [7,17],
     'workdays' : [0, 1, 2, 3, 4, 5, 6, 7]
    },
    {'contact': 'test2@test.com',
     'shift'  : [20,5],
     'workdays' : [7, 8]
    }
]
toErr = ['test@test.com']

# Write to local dirs
dev_mode = True

# Don't even have cams yet
newb_mode = False

if dev_mode:
    #data_dir = os.getcwd()
    data_dir = '/home/c/work/ap2/catch_output/'
    site_dir = '.'
else:
    data_dir = '/mnt/data/catch/ap2/catch_output/'
    site_dir = '/var/www/html/ap2/'

os.environ['TZ'] = 'US/Eastern'


##########################################
##########################################
##########################################

time.tzset()

# Create the spots
spots = {num:Spot(num) for num in spotNumbers}

# Read config file 
with open(config_fname) as f:
    camConfig = jl(f)

# Initialize the cameras (and spot info) from config
cams = {}
for c, cam in camConfig.iteritems():
    tc = Camera( spots, cam, dev_mode )
    cams[cam['number']] = tc


# Read api config, pass to Payment for initialization
payLog = os.path.join(data_dir,'pmAPI.log')
apiConfigFname = '../cfg/apiConfig.json'
with open(apiConfigFname) as f:
    apiConfig = jl(f)
payment = Payment( payLog, apiConfig, toErr )


# When getting the latest image, move it to a directory
# for processing... then delete it when done.
wd = os.path.join( data_dir, 'images_being_processed' )
if not os.path.exists(wd):
    os.makedirs(wd)

cd = os.path.join( data_dir, 'current_images' )
if not os.path.exists(cd):
    os.makedirs(cd)

vd = os.path.join( data_dir, 'images_of_violations' )
if not os.path.exists(vd):
    os.makedirs(vd)

ud = os.path.join( data_dir, 'images_of_undetections' )
if not os.path.exists(ud):
    os.makedirs(ud)

# Put spot logs in their own dir
sld, cld, csd = log.setupDirs( data_dir )

######################################
######################################
######################################

# BEGIN THE LOOP

######################################
######################################
######################################

t0 = time.time()

#for index in range(0,3):
while True:
    
    try:

        now = time.time()
        
        # Get enforcers that are on shift (for notifications)
        sendForce = []
        determineEnforcers( toForce, sendForce )

        # Update spots info from cameras
        for c, cam in cams.iteritems():
            cam.analyze(spots)

        # Update presence
        for s, spot in spots.iteritems():
            spot.update_occupation()

        # Get spot payment status
        payment.update(spots)
        
        # Determine violation
        if not newb_mode: 
            for s, spot in spots.iteritems():
                spot.update_status( sendForce, toErr, violationThresh, cd, vd, ud )
        
        # Update table
        table.write(spots,site_dir,dev_mode)

        # Log spot data
        for s, spot in spots.iteritems():
            log.logSpot(spot,sld)

    except Exception, e:
        tb = traceback.format_exc()
        msg = """
        %s
        Catch is going offline due to user error !
        Check my error logs for details...
        
        Exception:
        %s
        
        Traceback:
        %s""" % (time.asctime(),str(e),tb)
        print "%s\n\n%s" % (msg, str(e))
        sm('Error',msg,toErr)
        quit()

    # Do it all over again, after some rest
    time.sleep(sleepytime)


