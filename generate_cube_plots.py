import os 

import yt

from clump_finder import ClumpFinder, PLOT_DIR

cf = ClumpFinder(16)

def plot_cube(dim="x", field="density", annotated=True, plain=True):
    plot = yt.ProjectionPlot(
        cf.cube_ds,
        dim,
        field,
        #center=GALAXY_CENTRE,
        # TODO: Re-enable once scaling is fixed.
        #  width=(5, 'kpc')
    )
    if plain:
        plot.save(os.path.join(PLOT_DIR, '{}_cube_{}_{}'.format(
            cf.label,
            dim,
            field,
        )))
    if annotated:
        plot.annotate_clumps([c['clump'] for c in cf.molecular_clouds])
        plot.save(os.path.join(PLOT_DIR, '{}_clumps_{}_{}'.format(
            cf.label,
            dim,
            field,
        )))

plot_cube()
plot_cube(field="velocity_x", annotated=False)
plot_cube(field="velocity_y", annotated=False)
plot_cube(field="velocity_z", annotated=False)