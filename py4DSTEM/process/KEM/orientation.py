# Functions for mapping orientation of semi-crystalline materials

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.ndimage.filters import gaussian_filter


def get_orientation_array(braggpeaks,x0,y0,r_inner,r_outer,log=False):
    
    angle,intensity = np.zeros(braggpeaks.shape),np.zeros(braggpeaks.shape) 

    for i in range(braggpeaks.shape[0]):
        for j in range(braggpeaks.shape[1]):
            peaks = braggpeaks.get_pointlist(i,j)
            rx,ry = peaks.data['qx']-x0, peaks.data['qy']-y0
            rad = np.sqrt(rx**2+ry**2)
            theta = np.arctan2(rx,ry)
            theta[theta<0] = 2*np.pi + theta[theta<0] 
            
            mask =(rad>r_inner)*(rad<r_outer)

            if len(theta[mask])==0:
                angle[i,j] == False
                intensity[i,j] == 0
            
            else:
                angle[i,j]=theta[mask][0]
                if log:
                    intensity[i,j]=np.log(peaks.data['intensity'][mask][0]+1)
                else:
                    intensity[i,j]=peaks.data['intensity'][mask][0]
    return angle,intensity

def get_orientation_map(angle,intensity,plot=False,**kwargs):
    
    angle = angle/np.max(angle)
    intensity = intensity/np.max(intensity)
    
    if 'upres' in kwargs.keys():
        upres = kwargs['upres']
        angle_s = np.copy(angle)
        intensity_s = np.copy(intensity)
        x,y= angle_s.shape
        angle = np.zeros((x*upres,y*upres))
        intensity = np.zeros((x*upres,y*upres))
        for i in range(x):
            for j in range(y):
                angle[upres*i:upres*(i+1),upres*j:upres*(j+1)]=angle_s[i,j]
                intensity[upres*i:upres*(i+1),upres*j:upres*(j+1)]=intensity_s[i,j]
    
    if 'sigma' in kwargs.keys():
        sigma = kwargs['sigma']
        angle = gaussian_filter(angle,sigma=sigma)
        intensity = gaussian_filter(intensity,sigma=sigma)
    
    if 'cmap' in kwargs.keys():
        assert(isinstance(kwargs['cmap'],str)), "Error: cmap must be string. ie 'hsv', 'jet' "
        color = kwargs['cmap']
    else:
        color = 'hsv'
    hsv = cm.get_cmap(color, 256)
    cmap = mpl.colors.ListedColormap(hsv(np.tile(np.linspace(1,0,256),2)))
    
    intensity = np.dstack((intensity,intensity,intensity))
    hsv = np.delete(cmap(angle), 3, 2)
    
    image = hsv * intensity
    
    if not plot:
        return hsv,intensity
    else:
        fig,ax=plt.subplots(figsize=(6,6))
        ax.matshow(image)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="2%", pad=0.075)
        cbar = fig.colorbar(cm.ScalarMappable(cmap=cmap), cax=cax,ticks=[0, 0.25,0.5,0.75, 1])
        cbar.ax.set_yticklabels(['0', '90', '180','270','360']) 
        ax.axis('off')
        return 


