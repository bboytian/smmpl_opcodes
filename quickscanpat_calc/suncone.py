# imports
import datetime as dt

import numpy as np

# params
_npoints = 10                   # has to be even number
_minThetas = 0.05               # [deg]
_angularspacing = 0.05          # [deg]
_angularoffsets_a = [0]         # [deg]


# relevant functions
def _equalspacing_func():
    return np.arange(int(npoints/2)) * _angularspacing + _minThetas


# main func
def main(
        pointdistfunc=_equalspacing_func,
        angularoffsetsa=_angularoffsets_a
):
    '''
    Parameters
       pointdistfunc (func): function that distributes Thetas
    Return
        scanpat_dir (str): Directory of scanpat file
    '''
    Thetas_a = pointdistfunc()

    # computing directions to point towards based on time
    
    
    pass


# testing
if __name__ == '__main__':
    main()
