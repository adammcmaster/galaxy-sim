import os 

import yt

from clump_finder import ClumpFinder, GALAXY_CENTRE, PLOT_DIR

cf = ClumpFinder(16)

def plot_ramses(axis='x', fields='density'):
    plot = yt.ProjectionPlot(
        cf.ramses_ds,
        axis,
        fields,
        center=GALAXY_CENTRE,
        width=(5, 'kpc')
    )
    plot.save(os.path.join(PLOT_DIR, '{}_ramses'.format(cf.label)))

plot_ramses()
plot_ramses(fields='velocity_x')
plot_ramses(fields='velocity_y')
plot_ramses(fields='velocity_z')