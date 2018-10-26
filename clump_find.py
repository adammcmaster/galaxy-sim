import os
import sys

sys.path.insert(0, '/mnt/zfsusers/mcmaster/.virtualenvs/clumps/lib/python2.7/site-packages')

import yt
from yt.analysis_modules.level_sets.api import *

from ramses import RamsesData


GALAXY_CENTRE = [0.706731, 0.333133, 0.339857]
CUBE_PADDING = 0.001
MAX_LEVEL = int(sys.argv[1])

DATA_PATH = 'data'
RAMSES_INPUT_DIR = os.path.join(DATA_PATH, 'output_00149')
CUBE_DIR = os.path.join(DATA_PATH, 'cubes')
PLOT_DIR = os.path.join(DATA_PATH, 'plots')
CLUMP_DIR = os.path.join(DATA_PATH, 'clumps')

if not os.path.exists(CUBE_DIR):
    os.makedirs(CUBE_DIR)
if not os.path.exists(PLOT_DIR):
    os.makedirs(PLOT_DIR)
if not os.path.exists(CLUMP_DIR):
    os.makedirs(CLUMP_DIR)

cube_data = RamsesData(
    idir=RAMSES_INPUT_DIR,
    xmin=GALAXY_CENTRE[0] - CUBE_PADDING,
    xmax=GALAXY_CENTRE[0] + CUBE_PADDING,
    ymin=GALAXY_CENTRE[1] - CUBE_PADDING,
    ymax=GALAXY_CENTRE[1] + CUBE_PADDING,
    zmin=GALAXY_CENTRE[2] - CUBE_PADDING,
    zmax=GALAXY_CENTRE[2] + CUBE_PADDING,
    lmax=MAX_LEVEL,
    save_dir=CUBE_DIR,
)

ds = yt.load_uniform_grid(dict(density=cube_data.cube), cube_data.cube.shape)
data_source = ds.disk(
    GALAXY_CENTRE,
    [0., 0., 1.],
    (1, 'kpc'),
    (0.5, 'kpc'),
)

c_min = data_source["density"].min()
c_max = data_source["density"].max()
step = 8.0

clump_file = os.path.join(CLUMP_DIR, '{}_clumps.h5'.format(MAX_LEVEL))
if os.path.isfile(clump_file):
    master_clump = yt.load(clump_file)
else:
    master_clump = Clump(data_source, "density")
    find_clumps(master_clump, c_min, c_max, step)
    master_clump.save_as_dataset(clump_file, ['density'])

leaf_clumps = get_lowest_clumps(master_clump)

plot = yt.ProjectionPlot(ds, "x", "density", center=GALAXY_CENTRE)
plot.annotate_clumps(leaf_clumps)
plot.save(os.path.join(PLOT_DIR, 'clumps{}'.format(MAX_LEVEL)))
