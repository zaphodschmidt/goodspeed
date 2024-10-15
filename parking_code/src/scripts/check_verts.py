
import os

import numpy as np
import matplotlib.pyplot as plt
import cv2

import json
import pprint as pp

import ipdb



plt.close("all")

def onclick(event):
#    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
#          (event.button, event.x, event.y, event.xdata, event.ydata))
    print('[ %f, %f],' %
          (event.xdata, event.ydata))


from json import load as jl
config_fname = '../../cfg/cam_config.json'
# Read config file 
with open(config_fname) as f:
    cams = jl(f)

camera = cams['cam10']

_plot = True

fname = camera['local_im_full_path']

im = cv2.imread(fname)

#im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny( im, 100, 200 )

if _plot is True:
    #plt.ion()
    imc = np.copy(im)
    imc[:,:,0] = edges
    fig = plt.figure(figsize=(10,6))
#    plt.imshow(imc)
    
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

for spot in camera['spots']:

    verts = np.array(spot['vertices'])
    vs = verts.astype('int32')
    sn = spot['number']
    cv2.polylines(imc,[vs],True,(0,255,255))

plt.imshow(imc)
plt.show()


for spot in camera['spots']:
    
    verts = np.array(spot['vertices']).astype('int32')
    
    mask = np.zeros((im.shape[0],im.shape[1]))
    cv2.fillConvexPoly(mask,verts,1)
    bMask = mask.astype(bool)
    
    spotEdges = edges[bMask]
    edgeInds = np.where(spotEdges == 255)
    spot['base_nEdges'] = np.shape(edgeInds)[1]

#
#    imm = np.zeros_like(im).astype('uint8')
#
#    
#    if _plot is True:
#        
#        for color in range(0,3):
#            imm[bMask,color] = im[bMask,color]
#        imm[bMask,0] = edges[bMask]
#        ims = np.copy(imm)
#        sfig = plt.figure(figsize=(10,6))
#        plt.imshow(ims)
#
#    if _plot is True: 
#        plt.show()

if _plot is True:
    plt.figure()
    plt.ioff()
    plt.close()


#for spot in camera['spots']:
#    pp.pprint(spot)

pp.pprint(camera)

