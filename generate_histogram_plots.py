from clump_finder import ClumpFinder

cf = ClumpFinder(16)

cf.plot_hist('volume')
cf.plot_hist('mass')
cf.plot_hist('density')