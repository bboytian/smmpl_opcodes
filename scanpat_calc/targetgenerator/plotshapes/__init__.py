# imports
import numpy as np

from .aimlines import aimlines
from .aimpath import aimpath
from .cone import cone
from .grid import grid
from .hemisphere import hemisphere

from ....global_imports import *


# params
_h = np.sqrt(R**2 - 0.5 * (L0*2)**2) # [km]


# main class
class plotshapes:

    def __init__(
            self,
            timeobj,
            sunforecaster,
            pathplanner
    ):
        '''
        Parameters
            timeobj: defined in root folder
            sunforecaster: defined in root folder
            pathplanner: defined in root folder
        '''
        # Attributes

        ## grid layers; grids should be sorted in their order of importance
        n = 3
        disp_str = 'polygon'
        self.grid_lst = [
            grid(
                h=14.5, l=15,
                Lp=LP, n=3, disp_str=disp_str,
            ),
            grid(
                h=9, l=15,
                Lp=LP, n=n, disp_str=disp_str,
            ),
            grid(
                h=4, l=15,
                Lp=LP, n=n, disp_str=disp_str,
            ),
        ]


        ## other objects
        self.lidar_hem = hemisphere(
            self.grid_lst,
            R,
        )
        self.sun_cone = cone(
            timeobj, sunforecaster,
            self.grid_lst,
            THETAS,
        )
        self.targ_aimlines = aimlines(
            self.grid_lst,
            self.lidar_hem, self.sun_cone,
            CLOSEPROXTHRES
        )
        self.targ_aimpath = aimpath(
            pathplanner,
            self.grid_lst,
            self.targ_aimlines,
        )



    # update methods
    def gen(self):
        '''
        updates sunswath, aimlines and aimpath for each timeobjseg
        '''
        self.sun_cone.gen()
        self.targ_aimlines.gen()
        self.targ_aimpath.gen()
