# imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from .scannermove_func import main as scannermove_func
from ..file_readwrite.mpl_reader import smmpl_reader
from ...globalimports import *


# params; chosen sample
_samplest = pd.Timestamp('202007211700')
_sampleet = _samplest + pd.Timedelta(30, 'm')

# main func
def main(dira):
    '''
    Computes the measurement time of the lidar for a given scan pattern,
    excludes the scan init time. The coefficients are retrieved from a fitting
    function
    we are required to provide sample data to the fitter. Make sure that the
    sample data excludes the scanner initialisation

    Parameters
        dira (np.ndarray): [rad], (numpoints, 2(phil, thetal))
                           direction array for which we want to compute the time
    '''
    # finding sample
    mpl_d = smmpl_reader(LIDARNAME, starttime=_samplest, endtime=_sampleet)
    ## splitting up the timestamps into segments which have a break inbetween them
    _initduration = pd.Timedelta(2, 'm')
    ts_a = mpl_d['Timestamp']
    delts_a = ts_a[1:] - ts_a[:-1]
    deltsboo_a = delts_a >= _initduration
    ind_a = np.concatenate([np.argwhere(deltsboo_a).flatten(), np.array([-1])],
                           axis=0)
    tsseg_l = []
    for i, ind in enumerate(ind_a):
        if i == len(ind_a):
            break
        elif i == 0:
            tsseg = ts_a[0:ind]
        else:
            tsseg = ts_a[ind+1:ind_a[i+1]]
        tsseg_l.append(tsseg)
    tssego_l = tsseg_l.copy()

    tsseg_l = [tsseg[1:] - tsseg[:-1] for tsseg in tsseg_l]
    tsseg_l = [np.append([np.timedelta64(0, 's')], tsseg) for tsseg in tsseg_l]

    sampletsts_a = tssego_l[0]  # actual timestamp
    samplets_a = tsseg_l[0]     # relative timestamp in seconds
    sampledir_a = SPHERE2LIDARFN(np.deg2rad(mpl_d['Elevation Angle']),
                                 np.deg2rad(mpl_d['Azimuth Angle']),
                                 np.deg2rad(ANGOFFSET))
    sampledir_a = sampledir_a[(ts_a >= sampletsts_a[0]) *
                              (ts_a <= sampletsts_a[-1])]


    # performing fit
    popt, pcov = curve_fit(scannermove_func, sampledir_a, samplets_a,
                           p0=[0.5, 0.5])
    print(popt)

    # plotting
    plt.plot(scannermove_func(sampledir_a, *popt), samplets_a)
    plt.show()



# testing
if __name__ == '__main__':

    main(None)
