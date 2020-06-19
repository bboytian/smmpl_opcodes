# imports
import alphashape as aps
import matplotlib.path as mpath
import numpy as np

from ....params import *


# params
_swathplotang = np.deg2rad(SWATHPLOTANG)


# main class
class cone:

    def __init__(
            self,
            timeobj, sunforecaster,
            grid_lst,
            Thetas,
    ):
        '''
        Parameters
            timeobj : defined in parent folder
            sunforecaster : defined in parent folder
            grid_lst (lst): list of grid objects, to get intersections

            Thetas (float): [rad] angle b/n solar dir and lidar SNR limit dir
                            ; i.e. half angle with of cone

        Methods
            gen: generates sun swath for specified timeobj
                 generates grid_mask for each grid in grid_lst according to 
                 defined sunswath
        '''
        # Attributes
        self.grid_lst = grid_lst
        self.to = timeobj
        self.sf = sunforecaster

        self.Thetas = Thetas

        ## For future calc
        self.grid_masklst = None

        ## for visualisation
        self.swath_pathlst = None # returning polygon instead of path in case
                                     # path alters the input points
                                     
        
        # init
        self.gen()
    

    # main meth
    def gen(self):

        # getting sun angles from time of interest
        time_ara = self.to.get_timeara(fine_boo=True)
        angles_tup = self.sf.get_anglesvec(time_ara)
        thetas_ara, phis_ara = angles_tup
        boo_ara = thetas_ara<_swathplotang
        thetas_ara = thetas_ara[boo_ara]
        phis_ara = phis_ara[boo_ara]
        
        # rotation matrix; (3, 3, frames)
        rot_mat = np.array([
            [np.cos(phis_ara)*np.cos(thetas_ara), -np.sin(phis_ara),
             np.cos(phis_ara)*np.sin(thetas_ara)],
            [np.sin(phis_ara)*np.cos(thetas_ara), np.cos(phis_ara),
             np.sin(phis_ara)*np.sin(thetas_ara)],
            [-np.sin(thetas_ara), np.zeros_like(thetas_ara),
             np.cos(thetas_ara)]
        ])

        # getting points
        self.swath_pathlst = []
        self.grid_masklst = []
        for grid in self.grid_lst:
            h, l = grid.h, grid.l
            coord_mat = grid.coord_mat

            # generating cone slice
            phinum = PHINUMINTS * int(h)
            rhonum = RHONUMINTS * int(h)

            phi_ara = np.linspace(0, 2*np.pi, phinum)
            thetasexp_ara = thetas_ara[..., None]
            z_ara = h / (np.cos(thetasexp_ara)\
                    - np.tan(self.Thetas)*np.sin(thetasexp_ara)*np.cos(phi_ara))
            rhoh = z_ara * np.tan(self.Thetas)
            x_ara = rhoh  * np.cos(phi_ara)
            y_ara = rhoh * np.sin(phi_ara)
            vec_mat = np.array([x_ara, y_ara, z_ara]) # (3, frames, phinum)

            # rotating cone
            ## (3, phinum, frames) <=> (spatial dim, circle resolution, time)
            res = np.einsum('ijl,jlk->ikl', rot_mat, vec_mat, optimize=True)
            res_shape = res.shape
            x_ara, y_ara, z_ara = res.reshape(*res_shape[:-2],
                                              res_shape[-2]*res_shape[-1])
            points_ara = np.array([x_ara, y_ara, z_ara])

            # filtering portions that are not in the plane
            out_mask = ((np.abs(x_ara) > l/2) + (np.abs(y_ara) > l/2))
            points_ara = points_ara[:,~out_mask]
            points = points_ara[:2].T

            # generating grid edges
            lnum = LNUMSWATH * int(l)
            xedge_ara, yedge_ara = np.mgrid[-l/2:l/2:lnum*1j, -l/2:l/2:lnum*1j]
            xedge_ara = np.concatenate((xedge_ara[0], xedge_ara[-1],
                                        xedge_ara[1:-1, [0,-1]].flatten()))
            yedge_ara = np.concatenate((yedge_ara[0], yedge_ara[-1],
                                        yedge_ara[1:-1, [0,-1]].flatten()))
            edgepoints_ara = np.array([xedge_ara, yedge_ara]).T
            
            # adding grid edge points that are in the concave hull
            edgeboo_ara = np.zeros(len(edgepoints_ara))
            for i in range(res_shape[-1]): # iterating through circles
                circ_path = mpath.Path(res[:2, ..., i].T)
                edgeboo_ara += circ_path.contains_points(edgepoints_ara)
            edgepoints_ara = edgepoints_ara[edgeboo_ara.astype(np.bool)]
            points = np.append(points, edgepoints_ara, axis=0)

            # generating
            swath_poly = aps.alphashape(points, ALPHASHAPE) # swath polygon
            try:
                swath_path = mpath.Path(swath_poly.exterior.coords)
            except AttributeError: # in the event swath path is outside grid
                swath_path = None
            x_mat, y_mat = coord_mat[..., 0], coord_mat[..., 1]
            points2d_ara = np.stack((x_mat.flatten(), y_mat.flatten()),
                                    axis=-1)       
            try:
                grid_mask = ~swath_path.contains_points(points2d_ara)
            except AttributeError:
                grid_mask = np.ones(len(points2d_ara))      
            grid_mask = grid_mask.reshape(x_mat.shape)

            # Storing
            self.swath_pathlst.append(swath_path)

            self.grid_masklst.append(grid_mask)
