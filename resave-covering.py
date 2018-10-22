import sys

import yt

ds = yt.load('/redwhale/jeg/NUT_suite/new_sf_new_momfb_chab/output_00149/info_00149.txt')

level = int(sys.argv[1])
dims = ds.domain_dimensions * ds.refine_by**level

# We construct an object that describes the data region and structure we want
# In this case, we want all data up to the maximum "level" of refinement
# across the entire simulation volume.  Higher levels than this will not
# contribute to our covering grid.
cube = ds.covering_grid(level,
                        left_edge=[0.0, 0.0, 0.0],
                        dims=dims,
                        # And any fields to preload (this is optional!)
                        fields=["density"])
cube.save_as_dataset(filename='resaved-covering-grid-level{}'.format(level))
