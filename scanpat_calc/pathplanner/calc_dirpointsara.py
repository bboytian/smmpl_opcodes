# imports
import numpy as  np

from ...globalimports import *



# defining functions
'''
RAVELSTR = s

unravels points according to s shape
points within each sqaure is flattened without discremination

with respect to North,
RAVELARGS = 0: ravel in vertical reflected S pattern
            1: ravel in S pattern
            2: ravel in horizontal reflected N pattern
            3: ravel N pattern
'''



def s0_func(coord_mat, mask_mat):
    coord1_mat, mask1_mat = coord_mat.copy(), mask_mat.copy()
    coord1_mat[1::2] = np.flip(coord_mat[1::2], 1)
    mask1_mat[1::2] = np.flip(mask_mat[1::2], 1)

    mask_ara = mask1_mat.ravel()
    x_ara = coord1_mat[..., 0].ravel()[mask_ara]
    y_ara = coord1_mat[..., 1].ravel()[mask_ara]
    z_ara = coord1_mat[..., 2].ravel()[mask_ara]

    points_ara = np.stack((x_ara, y_ara, z_ara), 1)
    return points_ara


def s2_func(coord_mat, mask_mat):

    x_ara = coord_mat[..., 0].ravel()
    y_ara = coord_mat[..., 1].ravel()
    z_ara = coord_mat[..., 2].ravel()
    
    coord1_mat, mask1_mat = coord_mat.copy(), mask_mat.copy()
    coord1_mat[:, 1::2] = np.flip(coord_mat[:, 1::2], 0)
    mask1_mat[:, 1::2] = np.flip(mask_mat[:, 1::2], 0)

    mask_ara = mask1_mat.ravel('F') # 'F' is necessary for row ravelling
    x_ara = coord1_mat[..., 0].ravel('F')[mask_ara]
    y_ara = coord1_mat[..., 1].ravel('F')[mask_ara]
    z_ara = coord1_mat[..., 2].ravel('F')[mask_ara]

    points_ara = np.stack((x_ara, y_ara, z_ara), 1)
    return points_ara    


# main func
if RAVELSTR == 's':
    
    exec('func = s{}_func'.format(RAVELARGS), locals())


    
def calc_dirpointsara(
        self,
        coord_mat, mask_mat, 
):
    '''
    Parameters
        coord_mat (np.array): (N, N, ..., 3), '...' depend on grid.disp_str, 
                              mat follows the shape of the points on the grid                                  shape[-1] = 3 is for x, y, z component values
        mask_mat (np.array): (N, N, ...), mask for coord_mat component values

    Return
        dir_ara (np.array): lidar init points 
                            (N x N x np.prod(...), 2(theta, phi))
        points_ara (np.array): catersian of dir_ara
                               (N x N x np.prod(...), 3(x, y, z))    
    '''    
    points_ara = func(coord_mat, mask_mat)
    x_ara, y_ara, z_ara = points_ara.T
    
    r_ara = np.linalg.norm(points_ara, axis=-1)
    theta_ara = np.arccos(z_ara/r_ara)
    phi_ara = np.arctan2(y_ara, x_ara) # arctan2 chooses the right quadrant
    dir_ara = np.stack((theta_ara, phi_ara), axis=-1)
    
    return dir_ara, points_ara
