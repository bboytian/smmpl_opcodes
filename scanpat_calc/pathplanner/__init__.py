# imports
import numpy as np


# class
class pathplanner:

    def __init__(
            self,
            primaryaxis,
            angoffset,
    ):
        '''
        'unravels' the targets to form the scanner pattern and path

        Parameters
            primaryaxis (str): 'azimuth' or 'primary'
            angoffset (float): [rad] angular offset of lidar from north
        '''
        # Attributes
        self.primaryaxis = primaryaxis
        self.angoffset = angoffset


    # path manipulation
    from .calc_dirpointsara import calc_dirpointsara
    from .calc_pathara import calc_pathara
    def get_pointsNpath(
            self,
            coord_matlst, mask_matlst,
            fine_boo=False
    ):
        '''
        Future
            - intelligently cat the scan directions of the grids to optimise
              scan time
            - remove redundancies in points_aralst in the future if not being
              used

        Parameters
            coord_matlst (lst): list of (N, N, ..., 3),
                                '...' depend on grid.disp_str,
                                mat follows the shape of the points on the grid                                  shape[-1] = 3 is for x, y, z component values
            mask_matlst (lst): list of (N, N, ...),
                               mask for coord_mat component values

            fine_boo (boolean): if True, returns a path_ara that is discretised
                                in angle byparam

        Return
            dir_aralst (np.array): lidar init points without offset
                                   (N x N x np.prod(...), 2(theta, phi))
            points_aralst (lst): list of catersian of dir_ara, with grid height
                                 (N x N x np.prod(...), 3(x, y, z))
            path_ara (np.array): for plotting angular array which is the path
                                 of the scanner
                                 (N x N x np.prod(...) x expand, 2(theta, phi))
        '''
        dir_aralst = []
        points_aralst = []
        for i, coord_mat in enumerate(coord_matlst):
            mask_mat = mask_matlst[i]
            dir_ara, points_ara = self.calc_dirpointsara(
                coord_mat, mask_mat,
            )
            dir_aralst.append(dir_ara)
            points_aralst.append(points_ara)

        path_ara = self.calc_pathara(
            np.concatenate(dir_aralst, axis=0),
            self.primaryaxis,
            fine_boo
        )
        return dir_aralst, points_aralst, path_ara


    def get_scanpat(
            self,
            dir_aralst,
    ):
        '''
        lidar azimuthal range is from [-pi, pi]. The function here accomodates
        for that

        Parameters
            dir_aralst (list): [rad] list of lidar init points without offset,
                               grid array for each grid, each array has dim
                               (N x N x np.prod(...), 2(theta, phi))
        Return
            ret (np.array): [deg, 2dp] lidar init points with offset
                            (N x N x np.prod(...) x no. grids, 2(phi, theta))
        '''
        theta_ara, phi_ara = np.concatenate(dir_aralst, axis=0).T
        phi_ara -= self.angoffset  # [-pi, pi] -> [-2pi, 0] or [0, 2pi]
        # shifting phi_ara back to [-pi, pi] for compatibiility with lidar
        phi_ara[phi_ara < -np.pi] += 2*np.pi
        phi_ara[phi_ara > np.pi] -= 2*np.pi

        ret = np.stack((phi_ara, theta_ara), axis=1)
        ret = np.round(np.rad2deg(ret), 2)
        return ret
