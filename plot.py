import yt
ds = yt.load('data/output_00149/info_00149.txt')
plot = yt.ProjectionPlot(ds, "x", "density", center=[0.706731, 0.333133, 0.339857], width=(2, 'kpc'))
plot.save('original')
