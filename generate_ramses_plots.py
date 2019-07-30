from clump_finder import ClumpFinder

cf = ClumpFinder(16)

cf.plot_ramses()
cf.plot_ramses(fields='velocity_x')
cf.plot_ramses(fields='velocity_y')
cf.plot_ramses(fields='velocity_z')