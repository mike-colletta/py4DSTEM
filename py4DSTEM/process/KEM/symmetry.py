# Functions for symmetry contrast imaging

import numpy as np
from ..utils import print_progress_bar, tqdmnd
from scipy import ndimage
from time import time

############################# Symmetry Functions ################################

def score(ar1,ar2):
    return np.max(np.real(np.fft.ifft2(ar1*np.conj(ar2))))
    
def get_symmetry(datacube,angle,normalize=True):
    dc = datacube.data
    symmap = np.zeros((datacube.R_Nx,datacube.R_Ny))
    norm = 1
    t0 = time()
    for (i,j) in tqdmnd(datacube.R_Nx,datacube.R_Ny,desc='Computing symmetry in diffraction pattern',unit='DP',unit_scale=True):
        fft = np.fft.fft2(dc[i,j,:,:])
        if normalize:
            norm = score(fft,fft)
        rot = ndimage.rotate(dc[i,j,:,:], angle , reshape=False ,mode='wrap')
        fftr = np.fft.fft2(rot)
        symmap[i,j] = score(fft,fftr)/norm
    t = time()-t0
    print("Analyzed {} diffraction patterns in {}h {}m {}s".format(datacube.R_N, int(t/3600),
                                                                   int(t/60), int(t%60)))
    return symmap

def get_nfold_symmetry(datacube,n_fold,normalize=True):
    dc = datacube.data
    symmap = np.zeros((datacube.R_Nx,datacube.R_Ny))
    norm = (n_fold-1)
    t0 = time()
    for (i,j) in tqdmnd(datacube.R_Nx,datacube.R_Ny,desc='Computing symmetry in diffraction pattern',unit='DP',unit_scale=True):
        fft = np.fft.fft2(dc[i,j,:,:])
        if normalize:
            norm = (n_fold-1)*score(fft,fft)
        avsym=0
        for n in range(n_fold-1):
            rot = ndimage.rotate(dc[i,j,:,:], 360*(n+1)/n_fold , reshape=False ,mode='wrap')
            fftr = np.fft.fft2(rot)
            sym = score(fft,fftr)/norm
            avsym+=sym                
        symmap[i,j] = avsym
    t = time()-t0
    print("Analyzed {} diffraction patterns in {}h {}m {}s".format(datacube.R_N, int(t/3600),
                                                                   int(t/60), int(t%60)))
    return symmap



















# def get_nfold_symmetry(datacube,n_fold,verbose=True):
#     dc = datacube.data
#     symmap = np.zeros((datacube.R_Nx,datacube.R_Ny))
#     for i in range(datacube.R_Nx):
#         for j in range(datacube.R_Ny):
#             if verbose:
#                 print_progress_bar(i*datacube.R_Ny+j+1, datacube.R_Nx*datacube.R_Ny,
#                                    prefix='Analyzing:', suffix='Complete', length=50)
                
#             norm = np.max(np.real(np.fft.ifft2(np.fft.fft2(dc[i,j,:,:]) * np.conj(np.fft.fft2(dc[i,j,:,:])))))
#             avsym=0
#             for n in range(n_fold-1):
#                 rot = ndimage.rotate(dc[i,j,:,:], 360*(n+1)/n_fold, reshape=False ,mode='wrap')
#                 sym = np.max(np.real(np.fft.ifft2(np.fft.fft2(dc[i,j,:,:]) * np.conj(np.fft.fft2(rot)))))/norm
#                 avsym+=sym
#             avsym=avsym/(n_fold-1)
#             symmap[i,j]=avsym
#     return symmap

            