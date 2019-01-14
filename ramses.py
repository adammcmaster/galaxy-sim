import os

import numpy

from amr2cube import amr2cube


class RamsesData:
    def __init__(
        self,
        idir,
        sim_type=1,
        xmin=0,
        xmax=1,
        ymin=0,
        ymax=1,
        zmin=0,
        zmax=1,
        lmax=5,
        save_dir=None,
    ):
        """ Read RAMSES data and return a cube """

        cube_path = os.path.join(save_dir, '{}_cube.npy'.format(lmax))
        time_path = os.path.join(save_dir, '{}_time.txt'.format(lmax))

        if (
            save_dir
            and os.path.isfile(cube_path)
            and os.path.isfile(time_path)
        ):
            self.cube = numpy.load(cube_path)
            with open(time_path) as time_file:
                self.time = float(time_file.read().strip())

            return

        #Cube size parameter
        n=2**lmax
        nx=int((xmax-xmin)*n)
        ny=int((ymax-ymin)*n)
        nz=int((zmax-zmin)*n)

        self.xmin=xmin ; self.xmax=xmax
        self.ymin=ymin ; self.ymax=ymax
        self.zmin=zmin ; self.zmax=zmax

        self.cube, self.time = amr2cube(
            idir,
            sim_type,
            xmin,
            xmax,
            ymin,
            ymax,
            zmin,
            zmax,
            lmax,
            nx,
            ny,
            nz,
        )

        if save_dir:
            numpy.save(cube_path, self.cube)
            with open(time_path, 'w') as time_file:
                time_file.write(str(self.time))
