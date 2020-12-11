# imports
import datetime as dt
import multiprocessing as mp

import pandas as pd
import numpy as np

from . import sunforecaster
from .sunpath_plot import main as sunpath_plot
from ...global_imports.smmpl_opcodes import *


# params
_plotduration = dt.timedelta(1)
_numpoints = 1000

_conelen = 1


# main func
def main(date=None, time=None, utcinfo=UTCINFO):
    '''
    Plots out sun path for the day, as well as the current sun angle

    Parameters
        date (datetime like): timezone aware datetime object, plots out the date of the
    '''
    # getting time series
    if date:
        starttime = date
    else:
        starttime = LOCTIMEFN(dt.datetime.combine(dt.datetime.today(), dt.time()),
                              utcinfo)
    endtime = starttime + _plotduration

    ts_sr = pd.date_range(starttime, endtime, periods=_numpoints)
    sf = sunforecaster(LATITUDE, LONGITUDE, ELEVATION)
    thetas_a, phis_a = sf.get_anglesvec(ts_sr)
    dir_a = np.stack([phis_a, thetas_a], axis=1)

    # getting current time position
    if time:
        pointtime = time
    else:
        pointtime = LOCTIMEFN(dt.datetime.now(), utcinfo)
    thetas, phis = sf.get_angles(pointtime)
    d_a = np.stack([[phis], [thetas]], axis=1)

    pplot_func = mp.Process(target=sunpath_plot, args=(_conelen, dir_a, d_a))
    pplot_func.start()

    print('sun direction in terms of map coordinates:')
    print(f'SOA: {np.rad2deg(thetas)}')
    print(f'azimuth: {np.rad2deg(phis)}')

    # transform from spherical coords to lidar coords
    dir_a = SPHERE2LIDARFN(thetas, phis, np.deg2rad(ANGOFFSET))
    phil, ele = dir_a[0][0], dir_a[0][1]
    ele = np.round(np.rad2deg(ele), 2)
    phil = np.round(np.rad2deg(phil), 2)
    print('sun direction in terms of lidar direction:')
    print(f'elevation: {ele}')
    print(f'azimuth: {phil}')


# running
if __name__ == '__main__':
    main()
