import sys

import yt

ds = yt.load('/redwhale/jeg/NUT_suite/new_sf_new_momfb_chab/output_00149/info_00149.txt')

grid = ds.arbitrary_grid([0.0, 0.0, 0.0], [0.99, 0.99, 0.99],
                       dims=[128, 128, 128])
grid.save_as_dataset(filename='resaved-arbitrary-grid')
