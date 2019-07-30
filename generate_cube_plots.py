from clump_finder import ClumpFinder

cf = ClumpFinder(16)

cf.plot_cube(annotated=False)
cf.plot_cube(field="velocity_x", annotated=False)
cf.plot_cube(field="velocity_y", annotated=False)
cf.plot_cube(field="velocity_z", annotated=False)