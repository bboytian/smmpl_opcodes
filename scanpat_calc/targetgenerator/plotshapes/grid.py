# imports
import numpy as np

from ....globalimports import *


# supp funcs
def _npoint_func(
        disp_str,
        Lp, n,
        x_mat, y_mat,
):
    '''
    Parameters
        disptype_str (str):
            grid => n must be square rootable
            polygon => n > 1, points form a polygon, with n sides

    Return
        x_ara, y_ara of grid aim points,
        x_mat, y_mat (N, N, ...), N is num grid squares on one side
                                , ... is determined by disp_str
    '''
    # central position of pixel; (N, N, 2)
    coord_mat = np.stack((x_mat[:-1, :-1] + Lp/2,
                          y_mat[:-1, :-1] + Lp/2), axis=2)

    if disp_str == 'grid':
        def f(coord):
            # output is 2D
            sqrtn = int(np.sqrt(n))
            xLbound = coord[0] + Lp*(1/(sqrtn+1) - 1/2)
            xRbound = coord[0] + Lp*(1/2 - 1/(sqrtn+1))
            yLbound = coord[1] + Lp*(1/(sqrtn+1) - 1/2)
            yRbound = coord[1] + Lp*(1/2 - 1/(sqrtn+1))
            x_mat, y_mat = np.mgrid[xLbound : xRbound : sqrtn*1j,
                                    yLbound : yRbound : sqrtn*1j]
            return x_mat, y_mat

    elif disp_str == 'polygon':
        # (length from centroid to point) X 2 = 0.5 * Lp
        # x_mat and y_mat are 1 dimensional
        def f(coord):
            polylen = Lp * POLYLENALPHA / 2
            polyangle = np.deg2rad(360/n)
            ang_a = polyangle * np.arange(n)
            x_mat = np.cos(ang_a) * polylen + coord[0]
            y_mat = np.sin(ang_a) * polylen + coord[1]
            return x_mat, y_mat

    newcoord_mat = np.apply_along_axis(f, -1, coord_mat)  # (N, N, 2, ...)
    newx_mat = newcoord_mat[:, :, 0, ...]                # (N, N, ...)
    newy_mat = newcoord_mat[:, :, 1, ...]
    return newx_mat.flatten(), newy_mat.flatten(), newx_mat, newy_mat


# main class
class grid:

    def __init__(
            self,
            h, l,
            Lp, n, disp_str,
    ):
        '''
        Parameters
            h (float): height of plane
            l (float): length of grid
            Lp (float): pixel size
            n (int): no. of points within each grid, has to be square rootable
            disp_str (str): dispersion type of points

        Methods
            gen: generates coord_mat, coordmag_mat, xp_mat, yp_mat
        '''
        # Attributes
        self.h, self.l = h, l
        self.Lp, self.n, self.disp_str = Lp, n, disp_str

        ## for future calc
        self.coord_mat = None   # coordinates in the shape of the grid
                                # (N, N, ..., 3)
                                # '...' depend on pts spread in each grid sq
        self.coordmag_mat = None

        ## for visualisation
        self.xp_mat, self.yp_mat = None, None
        self.xg_mat, self.yg_mat, self.zg_mat = None, None, None
        self.x_ara, self.y_ara, self.z_ara = None, None, None

        # init
        self.gen()


    # main meth
    def gen(self):

        # computation of grid points
        xp_mat, yp_mat = np.mgrid[
            -self.l/2:self.l/2:2j,
            -self.l/2:self.l/2:2j
        ]
        xg_mat, yg_mat = np.mgrid[
            -self.l/2 : self.l/2 : (self.l/self.Lp + 1)*1j,
            -self.l/2 : self.l/2 : (self.l/self.Lp + 1)*1j
        ]
        zg_mat = self.h*np.ones_like(xg_mat)
        x_ara, y_ara, x_mat, y_mat = _npoint_func(
            self.disp_str,
            self.Lp, self.n,
            xg_mat, yg_mat
        )
        z_ara = self.h*np.ones_like(x_ara)
        coord_mat = np.stack((x_mat, y_mat, self.h*np.ones_like(x_mat)),
                             axis=-1)

        # Storing
        self.coord_mat = coord_mat
        self.coordmag_mat = np.linalg.norm(coord_mat, axis=-1)

        self.xp_mat, self.yp_mat = xp_mat, yp_mat
        self.xg_mat, self.yg_mat, self.zg_mat = xg_mat, yg_mat, zg_mat
        self.x_ara, self.y_ara, self.z_ara = x_ara, y_ara, z_ara
