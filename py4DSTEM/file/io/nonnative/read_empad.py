# Reads an EMPAD 4D-STEM dataset

import numpy as np
from pathlib import Path
from ...datastructure import DataCube
from ....process.utils import bin2D

def read_empad(fp, mem="RAM", binfactor=1, **kwargs):
    """
    Read an EMPAD 4D-STEM file.

    Accepts:
        fp          str or Path Path to the file
        mem         str         (opt) Specifies how the data should be stored; must be "RAM" or "MEMMAP". See
                                docstring for py4DSTEM.file.io.read. Default is "RAM".
        binfactor   int         (opt) Bin the data, in diffraction space, as it's loaded. See docstring for
                                py4DSTEM.file.io.read.  Default is 1.
        **kwargs

    Returns:
        dc          DataCube    The 4D-STEM data.
        md          MetaData    The metadata.
    """
    assert(isinstance(fp,(str,Path))), "Error: filepath fp must be a string or pathlib.Path"
    assert(mem in ['RAM','MEMMAP']), 'Error: argument mem must be either "RAM" or "MEMMAP"'
    assert(isinstance(binfactor,int)), "Error: argument binfactor must be an integer"
    assert(binfactor>=1), "Error: binfactor must be >= 1"

    row = 130
    col = 128
    fPath = Path(fp)

    # Parse the EMPAD metadata for first and last images
    empadDTYPE = np.dtype([('data','16384float32'),('metadata','256float32')])
    with open(fPath,'rb') as fid:
        imFirst = np.fromfile(fid,dtype=empadDTYPE,count=1)
        fid.seek(-128*130*4,2)
        imLast = np.fromfile(fid,dtype=empadDTYPE,count=1)

    # Get the scan shape
    shape0 = imFirst['metadata'][0][128+12:128+16]
    shape1 = imLast['metadata'][0][128+12:128+16]
    kShape = shape0[2:4]                        # detector shape
    rShape = 1 + shape1[0:2] - shape0[0:2]      # scan shape

    # Load the full data set
    with open(fPath,'rb') as fid:
        data = np.fromfile(fid,np.float32)
        data = np.reshape(data, (int(rShape[0]), int(rShape[1]), row, col))
    data = data[:,:,:128,:]

    if binfactor != 1:
        if 'dtype' in kwargs.keys():
            dtype = kwargs['dtype']
        else:
            dtype = data.dtype
        R_Nx,R_Ny,Q_Nx,Q_Ny = data.shape
        Q_Nx, Q_Ny = Q_Nx//binfactor, Q_Ny//binfactor
        databin = np.empty((R_Nx,R_Ny,Q_Nx,Q_Ny),dtype=dtype)
        for Rx in range(R_Nx):
            for Ry in range(R_Ny):
                databin[Rx,Ry,:,:] = bin2D(data[Rx,Ry,:,:,],binfactor,dtype=dtype)
        dc = DataCube(data = databin)

    dc = DataCube(data = data)
    md = None

    return dc, md
