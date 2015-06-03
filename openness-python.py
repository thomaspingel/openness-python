# -*- coding: utf-8 -*-
"""
Created on Fri May 29 13:20:41 2015

@author: Thomas Pingel
"""

import numpy as np

#%%

def openness(Z,cellsize,lookup_pixels):

    nrows, ncols = np.shape(Z)
        
    # neighbor directions are clockwise from top left
    neighbors = np.arange(8)    
    
    # Define a (fairly large) 3D matrix to hold the minimum angle for each pixel
    # for each of 8 directions
    opn = np.Inf * np.ones((8,nrows,ncols))
    
    # Define an array to calculate distances to neighboring pixels
    dlist = np.array([np.sqrt(2),1])

    # Calculate minimum angles        
    for this_distance in np.arange(1,lookup_pixels+1):
        for direction in neighbors:
            # Map distance to this pixel:
            dist = cellsize * dlist[np.mod(direction,2)]
            # Angle is the arctan of the difference in elevations, divided my distance
            this_angle = 90.0 - np.rad2deg(np.arctan((ashift(Z,direction,lookup_pixels)-Z)/dist))
            # Make the replacement
            this_layer = opn[direction,:,:]
            where_smaller = this_angle < opn[direction,:,:]
            this_layer[where_smaller] = this_angle[where_smaller]
            
            opn[direction,:,:] = this_layer

    # Openness is definted as the mean of the minimum angles of all 8 neighbors        
    return np.mean(opn,0)
    
    
    


#%%
def ashift(surface,direction,n=1):
    surface = surface.copy()
    if direction==0:
        surface[n:,n:] = surface[0:-n,0:-n]
    elif direction==1:
        surface[n:,:] = surface[0:-n,:]
    elif direction==2:
        surface[n:,0:-n] = surface[0:-n,n:]
    elif direction==3:
        surface[:,0:-n] = surface[:,n:]
    elif direction==4:
        surface[0:-n,0:-n] = surface[n:,n:]
    elif direction==5:
        surface[0:-n,:] = surface[n:,:]
    elif direction==6:
        surface[0:-n,n:] = surface[n:,0:-n]
    elif direction==7:
        surface[:,n:] = surface[:,0:-n]
    return surface


#%%

import gdal
import matplotlib.pyplot as plt
im = gdal.Open('data/dk22_dem.tif')
Z = im.ReadAsArray()
cellsize = im.GetGeoTransform()[1]
lookup_pixels = 20
O = openness(Z,cellsize,lookup_pixels)
plt.imshow(O)
