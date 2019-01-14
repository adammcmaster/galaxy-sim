import os
import sys

sys.path.insert(0, '/mnt/zfsusers/mcmaster/.virtualenvs/clumps/lib/python2.7/site-packages')

import yt
from yt.analysis_modules.level_sets.api import *

from ramses import RamsesData

GALAXY_CENTRE = [0.706731, 0.333133, 0.339857]
CUBE_PADDING = 0.001
#MAX_LEVEL = int(sys.argv[1])

DATA_PATH = 'data'
RAMSES_INPUT_NUM = 149
RAMSES_INPUT_DIR = os.path.join(
    DATA_PATH,
    'output_{:05d}'.format(RAMSES_INPUT_NUM),
)
RAMSES_INPUT_INFO = os.path.join(
    RAMSES_INPUT_DIR,
    'info_{:05d}.txt'.format(RAMSES_INPUT_NUM),
)
CUBE_DIR = os.path.join(DATA_PATH, 'cubes')
PLOT_DIR = os.path.join(DATA_PATH, 'plots')
CLUMP_DIR = os.path.join(DATA_PATH, 'clumps')

USE_FILE_CACHE = False


class ClumpFinder:
    def __init__(self, max_level):
        if not os.path.exists(CUBE_DIR):
            os.makedirs(CUBE_DIR)
        if not os.path.exists(PLOT_DIR):
            os.makedirs(PLOT_DIR)
        if not os.path.exists(CLUMP_DIR):
            os.makedirs(CLUMP_DIR)
            
        self._cube_data = None
        self._ramses_ds = None
        self._cube_ds = None
        self._disk = None
        self._master_clump = None
        self._leaf_clumps = None
        
        self.max_level = max_level
    
    @property
    def cube_data(self):
        if not self._cube_data:
            self._cube_data = RamsesData(
                idir=RAMSES_INPUT_DIR,
                xmin=GALAXY_CENTRE[0] - CUBE_PADDING,
                xmax=GALAXY_CENTRE[0] + CUBE_PADDING,
                ymin=GALAXY_CENTRE[1] - CUBE_PADDING,
                ymax=GALAXY_CENTRE[1] + CUBE_PADDING,
                zmin=GALAXY_CENTRE[2] - CUBE_PADDING,
                zmax=GALAXY_CENTRE[2] + CUBE_PADDING,
                lmax=self.max_level,
                save_dir=CUBE_DIR,
                use_file_cache=USE_FILE_CACHE,
            )
        return self._cube_data
    
    @property
    def ramses_ds(self):
        if not self._ramses_ds:
            self._ramses_ds = yt.load(RAMSES_INPUT_INFO)
        return self._ramses_ds
    
    @property
    def cube_ds(self):
        if not self._cube_ds:
            self._cube_ds = yt.load_uniform_grid(
                dict(density=self.cube_data.cube),
                self.cube_data.cube.shape,
                length_unit=self.ramses_ds.length_unit/512,#3080*6.02,
            )
        return self._cube_ds
    
    @property
    def disk(self):
        if not self._disk:
            self._disk = self.cube_ds.disk(
                GALAXY_CENTRE,
                [0., 0., 1.],
                (1, 'kpc'),
                (0.5, 'kpc'),
            )
        return self._disk

    @property
    def master_clump(self):
        if not self._master_clump:
            clump_file = os.path.join(CLUMP_DIR, '{}_clumps.h5'.format(self.max_level))
            if USE_FILE_CACHE and os.path.isfile(clump_file):
                self._master_clump = yt.load(clump_file)
            else:
                self._master_clump = Clump(self.disk, "density")
                find_clumps(
                    clump=self._master_clump, 
                    min_val=self.disk["density"].min(), 
                    max_val=self.disk["density"].max(), 
                    d_clump=8.0, # Step size
                )
                if USE_FILE_CACHE:
                    self._master_clump.save_as_dataset(clump_file, ['density'])
        
    @property
    def leaf_clumps(self):
        if not self._leaf_clumps:
            self._leaf_clumps = get_lowest_clumps(self.master_clump)
        return self._leaf_clumps

    def plot_ramses(self):
        plot = yt.ProjectionPlot(self.ramses_ds, "x", "density", center=GALAXY_CENTRE, width=(5, 'kpc'))
        plot.save(os.path.join(PLOT_DIR, 'ramses_{}'.format(self.max_level)))

    def plot_cube(self):
        plot = yt.ProjectionPlot(self.cube_ds, "x", "density", center=GALAXY_CENTRE, width=(5, 'kpc'))
        plot.save(os.path.join(PLOT_DIR, 'cube_{}'.format(self.max_level)))
        plot.annotate_clumps(self.leaf_clumps)
        plot.save(os.path.join(PLOT_DIR, 'clumps_{}'.format(self.max_level)))
        

if __name__ == "__main__":
    cf = ClumpFinder(int(sys.argv[1]))
    cf.plot_ramses()
    cf.plot_cube()
