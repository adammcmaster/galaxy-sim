import os
import sys

sys.path.insert(0, '/mnt/zfsusers/mcmaster/.virtualenvs/clumps/lib/python2.7/site-packages')

import holoviews
import numpy

import yt
from yt.analysis_modules.level_sets.api import *

from ramses import RamsesData

GALAXY_CENTRE = [0.706731, 0.333133, 0.339857]
CUBE_PADDING = 0.001
CLOUD_DENSITY_THRESHOLD = 1e6 # TODO: Choose a sensible value for this

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

class ClumpFinder:
    def __init__(self, max_level, label="", file_cache=True):
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
        self._clump_quantities = None
        self._molecular_clouds = None

        self.max_level = int(max_level)
        self.file_cache = file_cache
        if label:
            self.label = label
        else:
            self.label = max_level

    @property
    def ramses_ds(self):
        if not self._ramses_ds:
            self._ramses_ds = yt.load(RAMSES_INPUT_INFO)
        return self._ramses_ds

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
                use_file_cache=self.file_cache,
            )
        return self._cube_data

    @property
    def cube_ds(self):
        if not self._cube_ds:
            self._cube_ds = yt.load_uniform_grid(
                dict(density=self.cube_data.cube),
                self.cube_data.cube.shape,
                # TODO: Fix scaling. Doesn't find many clumps with this enabled.
                #length_unit=self.ramses_ds.length_unit/512,#3080*6.02,
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
            clump_file = os.path.join(
                CLUMP_DIR,
                '{}_clumps.h5'.format(self.max_level)
            )
            # TODO: Fix file format -- saved dataset loses attributes/isn't
            # loaded as the right type
            if False and os.path.isfile(clump_file):
                self._master_clump = yt.load(clump_file)
            else:
                self._master_clump = Clump(self.disk, "density")
                find_clumps(
                    clump=self._master_clump,
                    min_val=self.disk["density"].min(),
                    max_val=self.disk["density"].max(),
                    d_clump=8.0, # Step size
                )
                if self.file_cache:
                    self._master_clump.save_as_dataset(clump_file, ['density'])
        return self._master_clump

    @property
    def leaf_clumps(self):
        if not self._leaf_clumps:
            self._leaf_clumps = get_lowest_clumps(self.master_clump)
        return self._leaf_clumps

    @property
    def clump_quantities(self):
        if not self._clump_quantities:
            self._clump_quantities = []
            for clump in self.leaf_clumps:
                self._clump_quantities.append({
                    'clump': clump,
                    'volume': clump.data.volume().to_value(),
                    'mass': clump.data.quantities.total_mass().to_value()[0],
                })
                self._clump_quantities[-1]['density'] = (
                    self._clump_quantities[-1]['mass'] /
                    self._clump_quantities[-1]['volume']
                )
        return self._clump_quantities

    @property
    def molecular_clouds(self):
        if not self._molecular_clouds:
            self._molecular_clouds = [
                cq for cq in self.clump_quantities
                if cq['density'] >= CLOUD_DENSITY_THRESHOLD
            ]
        return self._molecular_clouds

    def plot_ramses(self):
        plot = yt.ProjectionPlot(
            self.ramses_ds,
            "x",
            "density",
            center=GALAXY_CENTRE,
            width=(5, 'kpc')
        )
        plot.save(os.path.join(PLOT_DIR, '{}_ramses'.format(self.label)))

    def plot_cube(self, annotated=True, plain=True):
        plot = yt.ProjectionPlot(
            self.cube_ds,
            "x",
            "density",
            #center=GALAXY_CENTRE,
            # TODO: Re-enable once scaling is fixed.
          #  width=(5, 'kpc')
        )
        if plain:
            plot.save(os.path.join(PLOT_DIR, '{}_cube'.format(self.label)))
        if annotated:
            plot.annotate_clumps([c['clump'] for c in self.molecular_clouds])
            plot.save(os.path.join(PLOT_DIR, '{}_clumps'.format(self.label)))

    def plot_hist(
        self,
        label,
        bins=50,
        width=1000,
        height=500,
    ):
        frequencies, edges = numpy.histogram(
            [c[label] for c in self.molecular_clouds],
            bins,
        )
        renderer = holoviews.renderer('bokeh')
        hist = holoviews.Histogram((edges, frequencies))
        hist = hist.options(
            width=width,
            height=height,
        )
        renderer.save(
            hist,
            os.path.join(PLOT_DIR, '{}_hist_{}'.format(self.label, label)),
        )


if __name__ == "__main__":
    cf = ClumpFinder(*sys.argv[1:])
    cf.plot_ramses()
    cf.plot_cube()
    cf.plot_hist('volume')
    cf.plot_hist('mass')
    cf.plot_hist('density')
