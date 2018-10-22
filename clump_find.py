import sys

import yt
from yt.analysis_modules.level_sets.api import *

from amr2cube import amr2cube

class RamsesData:

    def __init__(self,idir=1,type=1,xmin=0,xmax=1,ymin=0,ymax=1,zmin=0,zmax=1,lmax=5):
        """ Read RAMSES data and return a cube """

        #Read data in file
        dirname='output_'+str_suffix(idir)

        #Cube size parameter
        n=2**lmax
        nx=int((xmax-xmin)*n)
        ny=int((ymax-ymin)*n)
        nz=int((zmax-zmin)*n)

        self.xmin=xmin ; self.xmax=xmax
        self.ymin=ymin ; self.ymax=ymax
        self.zmin=zmin ; self.zmax=zmax

        self.cube,self.time=amr2cube(dirname,type,xmin,xmax,\
                                       ymin,ymax,zmin,zmax,lmax,nx,ny,nz)

def str_suffix(n,length=5):
    fewzero=''
    for i in range(length-len(str(n))):
        fewzero=fewzero+'0'
    return fewzero+str(n)


cube_data = RamsesData(
    idir=149,
    type=1,
    xmin=0.700731,
    xmax=0.710731,
    ymin=0.330133,
    ymax=0.340133,
    zmin=0.330857,
    zmax=0.350857,
    lmax=16,
)

ds = yt.load_uniform_grid(dict(density=cube_data.cube), cube_data.cube.shape)
data_source = ds.disk(
    [0.706731, 0.333133, 0.339857],
    [0., 0., 1.],
    (1, 'kpc'),
    (0.5, 'kpc'),
)

master_clump = Clump(data_source, "density")

c_min = data_source["density"].min()
c_max = data_source["density"].max()
step = 8.0
find_clumps(master_clump, c_min, c_max, step)

leaf_clumps = get_lowest_clumps(master_clump)

plot = yt.ProjectionPlot(ds, "x", "density", center=[0.706731, 0.333133, 0.339857], width=(2, 'kpc'))
plot.annotate_clumps(leaf_clumps)
plot.save('clumps')
