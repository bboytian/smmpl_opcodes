# imports
import numpy as np

from ...global_imports.smmpl_opcodes import *


# params
_angleres = np.deg2rad(ANGLERES)      # degrees, angular resolution of path


# supp funcs

def ang_func(ang_ara):
    '''
    ang_ara:: np.array([pri_ara, sec_ara]).T
    adds extra points into the angle arrays to reflect independent motion of
    lidar axis
    '''
    pri_ara, sec_ara = ang_ara.T
    lst = [pri_ara, sec_ara]
    priout_ara, secout_ara = [np.zeros(len(ara)*3-2) for ara in ang_ara.T]
    priout_ara[0::3], secout_ara[0::3] = pri_ara, sec_ara
    priout_ara[1::3] = priout_ara[2::3] = pri_ara[1:]
    secout_ara[1::3] = sec_ara[:-1]
    secout_ara[2::3] = sec_ara[1:]
    return np.stack((priout_ara, secout_ara), axis=1)


def fineang_func(ang_ara):
    '''
    does the same as ang_func, but adds discretised steps btwn the axis
    checkpoints
    solution taken from:
    https://stackoverflow.com/questions/60059110/how-to-populate-the-spacings-between-elements-of-an-array-with-constant-step-an?noredirect=1#comment106232228_60059110

    Parameters
        ang_ara (np.array): np.array([pri_ara, sec_ara]).T
    Return
        same structure as ang_ara but with discretisation inbetween pri and sec
    '''
    signs = np.diff(ang_ara, axis=0, append=ang_ara[-1, None]).ravel()[:-1]

    d = np.abs((signs // _angleres).astype(int) + 1)

    repeats = np.tile(d, 2)

    values = np.repeat(ang_ara.ravel(order='F'), 2)[1:-1]

    res = np.repeat(values, repeats).reshape(-1, 2, order='F')

    numbers = np.arange(res.shape[0])

    offsets = np.zeros(d.size)
    offsets[1:] = np.cumsum(d[:-1])
    offsets = np.repeat(offsets, d)

    signs = np.repeat(signs, d)

    ramps = (numbers - offsets) * np.copysign(_angleres, signs)
    ramps = np.stack((ramps, ramps), axis=1)

    mask = np.zeros((d.size, 2))
    mask[::2, 0] = mask[1::2, 1] = 1
    mask = np.repeat(mask, d, axis=0)

    res += ramps * mask
    return res


# function
def calc_pathara(
        self,
        dir_ara,
        priaxis_str,
        fine_boo=False
):
    '''
    Parameters
        dir_ara (np.array): (M, 2(theta, phi)) M is total number of points
        priaxis_str (str): 'elevation' or 'azimuth'
        fine_boo (boolean): if True, returns a path_ara that is discretised in
                            angle by param
    Return
        path_ara, plotting angular array will be the path of the scanner
    '''
    theta_ara, phi_ara = dir_ara.T

    # accounting for lidar azimuth range of [-pi, pi]
    phi_ara = phi_ara + self.angoffset # (-pi, pi] + offset
    phi_ara[phi_ara>np.pi] = phi_ara[phi_ara>np.pi] - 2*np.pi

    # appending points based on movement of primary, then secondary axis
    if fine_boo:                # path_ara discretised by _angleres
        func = fineang_func
    else:                       # path jumps to next angle immediately
        func = ang_func

    ang_ara = np.stack((theta_ara, phi_ara), axis=1)
    if priaxis_str == 'elevation':
        angout_ara = func(np.stack((theta_ara, phi_ara), axis=1))
        thetaout_ara, phiout_ara = angout_ara.T
    elif priaxis_str == 'azimuth':
        angout_ara = func(np.stack((phi_ara, theta_ara), axis=1))
        phiout_ara, thetaout_ara = angout_ara.T
    else:
        raise ValueError('priaxis_str can only be "elevation" or "azimuth"')

    # removing the offset so that the coordinates of the points dont change
    phiout_ara = phiout_ara - self.angoffset
    phi_ara[phi_ara<=-np.pi] = phi_ara[phi_ara<=-np.pi] + 2*np.pi

    path_ara = np.stack((thetaout_ara, phiout_ara), axis=1)

    return path_ara
