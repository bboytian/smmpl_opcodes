# imports
import datetime as dt

import numpy as np
import pandas as pd

from .suncone import main as suncone
from .horisweep import main as horisweep
from ..global_imports import *
from ..scanpat_calc.sunforecaster import sunforecaster


# params

_qspatfunc_d = {
    'suncone': suncone,
    'horisweep': horisweep
}
_highsun_l = [
    'suncone'
]


# relevant func
def _prompthighsun_func():
    '''
    Prompts if it is not an optimal time for measurement, in this case when the
    sun is not high enough whether the movement of the sun in minimal
    '''
    sf = sunforecaster(LATITUDE, LONGITUDE, ELEVATION)

    # computing optimal time
    today = dt.datetime.combine(dt.date.today(), dt.time())
    starttime = LOCTIMEFN(pd.Timestamp(today), UTCINFO)
    endtime = starttime + dt.timedelta(1)
    time_sr = pd.date_range(starttime, endtime, freq='min')  # minute intervals

    thetas_a, _ = sf.get_anglesvec(time_sr)
    angdrift = np.min(thetas_a)
    langthres = angdrift - np.deg2rad(HIGHSUNTHRES)
    hangthres = angdrift + np.deg2rad(HIGHSUNTHRES)
    boo_a = (thetas_a > langthres) * (thetas_a < hangthres)

    time_sr = time_sr[boo_a]
    starttime, endtime = time_sr[0], time_sr[-1]

    # prompting
    print(f'sun angular drift approx {np.rad2deg(angdrift)} deg')
    print(f'optimal time of measurement {starttime} to {endtime}')
    now = LOCTIMEFN(pd.Timestamp(dt.datetime.now()), UTCINFO)

    if now < starttime or now > endtime:
        GETRESPONSEFN(
            f'current time {now} is outside of optimal time, '
            'shall we proceed with measurement?',
            True, True
        )


# main func
@announcer(newlineboo=False)
def main(qstype):
    '''
    Calls the appropriate quick scan function to be called.
    The arguments for the functions are adjusted in their respective scripts
    Scan patterns are written to data directory specified in ..params

    Parameters
        qstype (str): type of scan quick scan pattern

    Return
        [deg] array produced by _qspatfunc
    '''
    if qstype in _highsun_l:
        _prompthighsun_func()

    return _qspatfunc_d[qstype]()


# testing
if __name__ == '__main__':
    # main()
    _prompthighsun_func()
