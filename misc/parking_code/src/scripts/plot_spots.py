

import csv
import os, sys
import re
sys.path.append('..')
from json import load as jl
import ipdb


def get_spot_data(log_dir,plot_spots=None):
    spots = []

    f = []
    for (dirpath, dirnames, filenames) in os.walk(log_dir):
        f.extend(filenames)
        break

    for s in f:
        ffname = os.path.join(log_dir,s)
        ft = os.path.splitext(s)
        sn = int( ft[0][4:] )
        
        if not plot_spots is None:
            if sn not in plot_spots:
                continue

        ts = []
        tp = []
        nEdges = []
        with open(ffname) as f:
            rdr = csv.reader(f)
            for r in rdr:
                ts += [float(r[0])]
                tp += [float(r[1])]
                nEdges += [float(r[2])]

        spot = {
            'num':sn,
            'ts':ts,
            'nEdges':nEdges,
        }

        spots += [spot]

    return spots


#######################################
#######################################
#######################################

import matplotlib.pyplot as plt
import numpy as np


plot_spots = range(1,50)
tmin = -24
tmax = 0

fdir = os.path.expanduser('~/work/ap2/archive/0625/spot_logs/')

config_fname = '../../cfg/cam_config.json'

spots = get_spot_data(fdir,plot_spots)


# Read config file 
with open(config_fname) as f:
    camConfig = jl(f)


spot_edges = {}

for c,cam in camConfig.iteritems():
    sl = cam['spots']
    for s in sl:
        sn = s['number']
        spot_edges[sn] = s['base_nEdges']
        print 'spot%d base_nEdges = %d' % (s['number'],s['base_nEdges'])


i = 1
for s in spots:
   
    print 'checking spot %d' % s['num']

    if 'plot_spots' in locals():
        if s['num'] not in plot_spots:
            print '     skipping spot %d' % s['num']
            continue

    time = np.asarray(s['ts'])
    t2end = (time - time[-1]) / 3600
    
    inds = np.where( np.bitwise_and( t2end > tmin, t2end < tmax ) )

    edgelim = spot_edges[s['num']]
    nes = np.asarray( s['nEdges'] )
    
    dname = 'pics'
    if not os.path.exists(dname):
        os.makedirs(dname)

    
    
    plt.figure()
    plt.plot( t2end[inds], nes[inds] )
    plt.plot( t2end[inds], edgelim*np.ones_like(t2end[inds]) )
    plt.title( 'Spot %d: nEdges' % s['num'] )

    #plt.show()
    fname = 'spot' + str(s['num']) + '_nedges.png'
    fname = os.path.join(dname,fname)
    plt.savefig(fname)

    plt.close()
    #plt.waitforbuttonpress(timeout=-1)

    i += 1


plt.figure()
plt.close()

sort_spots = sorted( spots, key=lambda k: k['num'] )

html = """
<html>
    <head>
    <title>Spot Plots</title>
    </head>
    <body>"""
for s in sort_spots:
    ss = str(s['num'])
    
    html += '<h2>'
    html += 'Spot ' + ss + ' History'
    html += '</h2>'
    
    fname = dname + '/spot' + ss + '_nedges.png'
    html += '<img src="' + fname + '" style="width:304px;height:228px;">'


html += '</body></html>'

with open('index.html','w') as f:
    f.write(html)

