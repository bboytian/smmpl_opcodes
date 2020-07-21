import numpy as np

from ...globalimports import *


if SFAPI == 'pysolar_API':
    from .pysolar_API import func as get_angles
elif SFAPI == 'pysolarfast_API':
    from .pysolarfast_API import func as get_angles
elif SFAPI == 'sunposcalc_API':
    from .sunposcalc_API import func as get_angles


class sunforecaster:

    def __init__(
            self,
            lt, lg,
            ele=0
    ):
        '''
        Parameters
            lt (float): latitude [deg]
            lg (float): longitude [deg]
            ele (float): elevation [m]
        '''
        self.lt, self.lg = lt, lg
        self.ele = ele

    def get_angles(self, timestamp):
        '''
        Return
            thetas, phis (float): [rad]
        '''
        return get_angles(
            timestamp,
            self.lt, self.lg,
            self.ele
        )

    def get_anglesvec(self, timestamp_ara):
        '''
        Return
             (thetas_ara, phis_ara)
        '''
        return np.vectorize(self.get_angles)(timestamp_ara)

# testing forecast
if __name__ == '__main__':
    '''
    plots out the sun path
    '''
    import datetime as dt
    import pandas as pd
    import matplotlib.pyplot as plt

    # getting time series
    starttime = pd.Timestamp('20200721').tz_localize(
        dt.timezone(dt.timedelta(hours=UTC))
    )
    endtime = pd.Timestamp('20200822').tz_localize(
        dt.timezone(dt.timedelta(hours=UTC))
    )

    ts_sr = pd.date_range(starttime, endtime, periods=1000)
    sf = sunforecaster(LATITUDE, LONGITUDE, ELEVATION)
    thetas_a, phis_a = sf.get_anglesvec(ts_sr)
    dir_a = np.stack([phis_a, thetas_a], axis=1)

    def _plot_func(dir_a):
        _conelen = 20
        fig3d = plt.figure(figsize=(10, 10), constrained_layout=True)
        ax3d = fig3d.add_subplot(111, projection='3d')
        ax3d.set_xlabel('South -- North')
        ax3d.set_ylabel('East -- West')

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

    _plot_func(dir_a)
