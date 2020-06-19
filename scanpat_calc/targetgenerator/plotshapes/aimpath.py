# imports
import matplotlib.path as mpath
import numpy as np


# class
class aimpath:

    def __init__(
            self,
            pathplanner,
            grid_lst,
            aimlines,
    ):
    
        '''
        Future
            - consider unravelling the points in consideration of all the 
              directions in all the grids
            - maybe shift the whole path planner here?

        Parameters
            pathplanner (..pathplanner)
            grid_lst (lst): list of grid objects, to get target points
            aimlines (aimlines)

        Methods
            gen: generates the following
                     self.dir_aralst => scan pattern list for each grid
                     self.points_aralst => scanpoints for each grid in pat order
                     self.path_aralst => discretised path for each grid
        '''
        # Attributes
        ## static
        self.pp = pathplanner
        self.grid_lst = grid_lst
        ## changing
        self.aimlines = aimlines
        self.coord_matlst = None
        self.mask_matlst = None
        
        ## for future calc
        self.dir_aralst = None
        self.points_aralst = None
        self.path_ara = None
        
        
        # init
        self.gen()

    
    # main meth
    def gen(self):

        # updating changed variables
        self.coord_matlst = self.aimlines.coord_matlst
        self.mask_matlst = self.aimlines.mask_matlst        

        # computing points and path
        self.dir_aralst, self.points_aralst, self.path_ara = \
            self.pp.get_pointsNpath(
                self.coord_matlst, self.mask_matlst, 
                fine_boo=True
            )
