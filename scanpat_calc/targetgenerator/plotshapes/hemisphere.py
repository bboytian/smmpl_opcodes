# main class
class hemisphere:

    def __init__(
            self,
            grid_lst,
            r,
    ):
        '''
        Parameters
            grid_lst (list): list of targetgenerator.grid objects
                             ; get intersect mask
            r (float): radius of hemisphere

        Methods
            gen  generates grid_mask for each grid in grid_lst
        '''
        # Attributes
        self.grid_lst = grid_lst
        self.r = r

        ## For future calc
        self.grid_masklst = None
        
        # init
        self.gen()


    # main meth
    def gen(self):

        # calculating intersection mask
        self.grid_masklst = []
        for grid in self.grid_lst:

            # points within the hemisphere
            grid_mask = grid.coordmag_mat <= self.r

            # storing
            self.grid_masklst.append(grid_mask)
