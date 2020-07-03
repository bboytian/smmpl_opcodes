# imports
import datetime as dt
import multiprocessing as mp
from warnings import warn

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..globalimports import *
from ..scanpat_calc.sunforecaster import sunforecaster
from ..scan_vis.plotshapes import cone as cone


# params
## timings
_initlag_dt = pd.Timedelta(1, 'm')  # account for initialisation time and movement
                                    # time of scanner to the first point
_measurelag_dt = pd.Timedelta(0, 's')  # accounts for movement time between
                                       # measurement times

## point calculation
_npoints = 10                   # has to be even number
_minThetas = 0.05               # [rad], sum of this and _angular spacing must > 0
_angularspacing = 0.2          # [rad]
_angularoffsets_a = [0]         # [rad]
_west2east_boo = True           # first array direction

## plot settings
_scale = 1.3
_curlyl = 30
_conelen = 20


# relevant functions
def _equalspacing_func():
    '''
    Points are arranged in intended chronological measurement order, with
    directions decided on by _west2east_boo

    Return
        Thetas_a (np.array): array of angular spacings
        west_ba (np.array): boolean array, which specifies whether the point is on
                            the right side of the sun
    '''
    Thetas_a = np.arange(int(_npoints/2)) * _angularspacing + _minThetas
    west_ba = np.ones(len(Thetas_a), dtype=bool)
    Thetas_a = np.append(Thetas_a[::-1], Thetas_a)
    west_ba = np.append(west_ba, ~west_ba)
    return Thetas_a, west_ba


def _calcdir_func(thetas, phis, Thetas):
    '''
    Return
        w/erl_a (np.array): 3-vector containing components of direction array.
                            'w/e' relate to which one point is more west/east.
                            Magnitude of direction vector is given by 'u'
    '''
    u = 1

    # computing sun point
    rsz = u * np.cos(thetas)
    rsy = u * np.sin(thetas) * np.sin(phis)
    rlx = rsx = u * np.sin(thetas) * np.cos(phis)  # considered to be static

    
    # computing lidar points
    a = (rsz**2) + (rsy**2)
    if rsy != 0:
        bOm2rsz = (np.cos(Thetas) * (u**2) - (rsx**2))

        b = -2 * bOm2rsz * rsz
        c = (bOm2rsz**2) - (rsy**2) * (rsy**2 + rsz**2)

        prlz = (-b + np.sqrt((b**2) - 4*a*c))/2/a
        mrlz = (-b - np.sqrt((b**2) - 4*a*c))/2/a

        prly = (bOm2rsz - rsz*prlz)/rsy
        mrly = (bOm2rsz - rsz*mrlz)/rsy
    else:
        bOm2rsy = (np.cos(Thetas) * (u**2) - (rsx**2))

        b = -2 * bOm2rsy * rsy
        c = (bOm2rsy**2) - (rsz**2) * (rsz**2 + rsy**2)

        prly = (-b + np.sqrt((b**2) - 4*a*c))/2/a
        mrly = (-b - np.sqrt((b**2) - 4*a*c))/2/a

        prlz = (bOm2rsy - rsy*prly)/rsz
        mrlz = (bOm2rsy - rsy*mrly)/rsz

    # finding out which point is more east, which is more west
    if prly > mrly:
        wrl = np.array([rlx, prly, prlz])
        erl = np.array([rlx, mrly, mrlz])
    elif mrly > prly:
        erl = np.array([rlx, prly, prlz])
        wrl = np.array([rlx, mrly, mrlz])
    else:
        warn("'_minThetas + _angularspacing' or 'u' is so small that east and west points are not distinguishable")
        
    return wrl, erl


def _plot_func(dir_a):
    fig3d = plt.figure(figsize=(10, 10), constrained_layout=True)
    ax3d = fig3d.add_subplot(111, projection='3d')
    ax3d.pbaspect = [_scale, _scale, _scale]
    ax3d.set_xlabel('South -- North')
    ax3d.set_ylabel('East -- West')
    ax3d.set_xlim([-_curlyl/2, _curlyl/2])
    ax3d.set_ylim([-_curlyl/2, _curlyl/2])
    ax3d.set_zlim([0, _curlyl])

    # plotting points in order of lines
    rx_a = _conelen * np.sin(dir_a[:, 1]) * np.cos(dir_a[:, 0])
    ry_a = _conelen * np.sin(dir_a[:, 1]) * np.sin(dir_a[:, 0])
    rz_a = _conelen * np.cos(dir_a[:, 1])
    ax3d.plot(rx_a, ry_a, rz_a)
    ax3d.scatter(rx_a, ry_a, rz_a)

    # plotting aimlines
    ind_a = range(0, len(rx_a)+1, 2)
    rx_a = np.insert(rx_a, ind_a, 0)
    ry_a = np.insert(ry_a, ind_a, 0)
    rz_a = np.insert(rz_a, ind_a, 0)
    ax3d.plot(rx_a, ry_a, rz_a, color='k', alpha=0.2)

    plt.show()



# main func
def main(
        plot_boo,
        pointdist_func=_equalspacing_func
):
    '''
    Assumes negligible movement time between measurements.
    It unravels in a S-shape the points if there are multiple elements in
    _angularoffsets_a. The direction of the first array is decided by
    _west2east_boo

    Parameters
        plot_boo (boolean): Decides whether or not to plot the figure, starts
                            another process
        pointsdist_func (func): function to compute the spacing Thetas of lidar
                                points, should be defined here or in the same
                                package

    Return
        dir_a (str): [rad] array containing scan pattern angles
                     shape: (M:=_npoints*len(offset_a), 2(phil, thetal))
    '''
    # angular spacing array
    Thetas_a, west_ba = pointdist_func()

    # initialising sun forecaster
    sf = sunforecaster(LATITUDE, LONGITUDE, ELEVATION)

    # getting starttime
    pointtime = dt.datetime.now()
    pointtime = pd.Timestamp(pointtime).tz_localize(
        dt.timezone(dt.timedelta(hours=UTC))
    )
    pointtime += _initlag_dt

    # computing directions to point towards based on time
    west2east_boo = _west2east_boo
    dir_a = np.empty((0, 2))    # unit spherical coordinates, (M, 2)
    for angularoffsets in _angularoffsets_a:

        seg_a = np.empty((0, 3))  # cartesian coordinates, (M, 3)
        for i, Thetas in enumerate(Thetas_a):
            west_boo = west_ba[i]

            # computing directions for given sun angle
            thetas, phis = sf.get_angles(pointtime)
            wrl, erl = _calcdir_func(thetas, phis, Thetas)

            # appending to segment
            if west_boo:
                seg_a = np.append(seg_a, [wrl], axis=0)
            else:
                seg_a = np.append(seg_a, [erl], axis=0)

            # iterate time
            pointtime += pd.Timedelta(AVERAGINGTIME, 's') + _measurelag_dt

        # converting to spherical coordinate
        seg_a = np.stack([      # spherical coordinates, (M, 2)
            np.arctan2(seg_a[:, 1], seg_a[:, 0]),  # phil
            np.arccos(seg_a[:, 2])                 # thetal
        ], axis=1)

        # adding offset to thetal
        seg_a[:, 1] += angularoffsets

        # flipping array
        if not west2east_boo:
            seg_a = seg_a[::-1]

        # toggling flip for 's' shape unravelling
        west2east_boo = not west2east_boo

        # appending
        dir_a = np.append(dir_a, seg_a, axis=0)


    # plotting if specified for confirmation
    if plot_boo:
        pplot_func = mp.Process(target=_plot_func, args=(dir_a,))
        pplot_func.start()
        
    return np.rad2deg(dir_a)



# testing
if __name__ == '__main__':
    dir_a = main(True)
