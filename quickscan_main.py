# imports
import datetime as dt
import os
import os.path as osp

import numpy as np

from .globalimports import *
from .quickscanpat_calc import quickscanpat_calc
from .sop import sigmampl_boot


# main func
def main():
    '''
    quick scan pattern parameters are adjusted in their respective scripts,
    i.e. quickscanpat_calc.<quickscantype>

    But quick scanpattern type, bin resolution and shot averaging time are
    controlled in .params

    Future
        - Handle file management when closing file
    '''

    # calculating scan pattern
    scanpat_a = quickscanpat_calc(QUICKSCANTYPE)

    # writing scan pattern to file
    now = dt.datetime.now()
    scanpatpar_dir = DIRCONFN(
        SOLARISMPLDATADIR, DATEFMT.format(now)
    )
    if not osp.isdir(scanpatpar_dir):
        os.mkdir(scanpatpar_dir)
    scanpat_dir = DIRCONFN(
        scanpatpar_dir,
        QUICKSCANFILE.format(QUICKSCANTYPE, now)
    )
    print(f'writing quick scanpattern to: {scanpat_dir}')
    np.savetxt(scanpat_dir, scanpat_a,
               fmt='%.2f', delimiter=', ', newline='\n\n')


    # beginning init and measurement
    sigmampl_boot(coldstart_boo=True, scanpat_dir=scanpat_dir)

    
# testing
if __name__ == '__main__':
    main()
