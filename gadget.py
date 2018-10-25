import yt
import numpy as np
import yt.units as units
import pylab

from yt.analysis_modules.level_sets.api import *

bbox = [
    [0., 9000.],
    [0., 16900.],
    [0., 9000.],
]

ds = yt.load(
    'data/output_00149/ramses2gadget_149.0',
    bounding_box=bbox,
)

#px = yt.ParticlePlot(
#    ds, 
#    ('Gas', 'particle_position_x'), 
#    ('Gas', 'particle_position_y'), 
#    ('Gas', 'Mass')
#)
#px.save('gadget_gas_raw')
#
#data_source = ds.disk(
#    [0.706731, 0.333133, 0.339857],
#    [0., 0., 1.],
#    (1, 'kpc'),
#    (0.5, 'kpc'),
#)

#data_source = ds.arbitrary_grid([0.0, 0.0, 0.0], [0.99, 0.99, 0.99],
#                       dims=[128, 128, 128])

level = 18
dims = ds.domain_dimensions * ds.refine_by**level

data_source = ds.covering_grid(level,
                        left_edge=[0.0, 0.0, 0.0],
                        dims=dims,
)
master_clump = Clump(data_source, ('Gas', 'Mass'))

c_min = data_source[('Gas', 'Mass')].min()
c_max = data_source[('Gas', 'Mass')].max()
step = 8.0
find_clumps(master_clump, c_min, c_max, step)

leaf_clumps = get_lowest_clumps(master_clump)

px = yt.ParticlePlot(
    ds, 
    ('Gas', 'particle_position_x'), 
    ('Gas', 'particle_position_y'), 
    ('Gas', 'Mass'),
    center=[0.706731, 0.333133, 0.339857],
    width=(2, 'kpc'),
)
plot.annotate_clumps(leaf_clumps)
px.save('gadget_gas_clumps')
