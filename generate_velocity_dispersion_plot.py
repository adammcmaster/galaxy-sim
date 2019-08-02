import os 

import holoviews

from clump_finder import ClumpFinder, PLOT_DIR


cf = ClumpFinder(16)

renderer = holoviews.renderer('bokeh')

values = []
for z, axis in enumerate(('x', 'y', 'z')):
    values.extend([
        (c['volume'], c['velocity_{}_var'.format(axis)], z) 
        for c in cf.molecular_clouds
    ])

points = holoviews.Points(values, vdims=('z', 'direction'))
points.opts(color='z', marker='+', size=10)

renderer.save(
    points,
    os.path.join(PLOT_DIR, '{}_velocity_dispersion_volume'.format(cf.label)),
)
