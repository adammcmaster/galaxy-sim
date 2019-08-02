import os 

import holoviews
import numpy

from clump_finder import ClumpFinder, PLOT_DIR

cf = ClumpFinder(16)

def plot_hist(
    label,
    bins=50,
    width=1000,
    height=500,
):
    frequencies, edges = numpy.histogram(
        [c[label] for c in cf.molecular_clouds],
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
        os.path.join(PLOT_DIR, '{}_hist_{}'.format(cf.label, label)),
    )

plot_hist('volume')
plot_hist('mass')
plot_hist('density')