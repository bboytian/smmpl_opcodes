# imports
import datetime as dt
import multiprocessing as mp

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from . import sunforecaster
from ...global_imports.smmpl_opcodes import *


# supp funcs
def _plot_func(*dir_aa):
    _conelen = 20
    fig3d = plt.figure(figsize=(10, 10), constrained_layout=True)
    ax3d = fig3d.add_subplot(111, projection='3d')
    ax3d.set_xlabel('South -- North')
    ax3d.set_ylabel('East -- West')

    for dir_a in dir_aa:

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
        ax3d.plot(rx_a, ry_a, rz_a, alpha=0.2)

    plt.show()


# main func
def main():
    '''
    Plots out sun path for the day, as well as the current sun angle
    '''
    # getting time series
    starttime = LOCTIMEFN(dt.datetime.combine(dt.datetime.today(), dt.time()),
                          UTCINFO)
    endtime = starttime + dt.timedelta(1)

    ts_sr = pd.date_range(starttime, endtime, periods=1000)
    sf = sunforecaster(LATITUDE, LONGITUDE, ELEVATION)
    thetas_a, phis_a = sf.get_anglesvec(ts_sr)
    dir_a = np.stack([phis_a, thetas_a], axis=1)

    # getting current time position
    pointtime = LOCTIMEFN(dt.datetime.now(), UTCINFO)
    thetas, phis = sf.get_angles(pointtime)
    d_a = np.stack([[phis], [thetas]], axis=1)

    pplot_func = mp.Process(target=_plot_func, args=(dir_a, d_a))
    pplot_func.start()

    # transform from spherical coords to lidar coords
    dir_a = SPHERE2LIDARFN(thetas, phis, np.deg2rad(ANGOFFSET))
    phil, ele = dir_a[0][0], dir_a[0][1]
    ele = np.round(np.rad2deg(ele), 2)
    phil = np.round(np.rad2deg(phil), 2)
    print('sun direction in terms of lidar direction:')
    print(f'elevation: {np.rad2deg(ele)}')
    print(f'azimuth: {np.rad2deg(phil)}')


# running
if __name__ == '__main__':
    main()
