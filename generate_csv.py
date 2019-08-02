import csv
import os 

from clump_finder import ClumpFinder, PLOT_DIR

cf = ClumpFinder(16)
with open(os.path.join(PLOT_DIR, '{}_clumps.csv'.format(cf.label)), 'w') as out_f:
    fields = [
        k for k in cf.clump_quantities[0].keys() if k != 'clump'
    ]
    w = csv.DictWriter(out_f, fieldnames=fields, extrasaction='ignore')
    w.writerow({f:f for f in fields})
    for cloud in cf.molecular_clouds:
        w.writerow(cloud)