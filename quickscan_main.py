# imports
import datetime as dt
import os.path as osp

import numpy as np

from .globalimports import *
from .quickscanpat_calc import quickscanpat_calc


# main func
def main():
    '''
    quick scan pattern parameters are adjusted in their respective scripts,
    i.e. quickscanpat_calc.<quickscantype>

    But quick scanpattern type, bin resolution and shot averaging time are
    controlled in .params
    '''

    # calculating scan pattern
    scanpat_a = quickscanpat_calc(QUICKSCANTYPE)

    # writing scan pattern to file
    now = dt.datetime.now()
    scanpatpar_dir = osp.join(
        SOLARISMPLDATADIR, DATEFMT.format(now)
    )
    if not osp.isdir(scanpatpar_dir):
        os.mkdir(scanpatpar_dir)
    scanpat_dir = osp.join(
        scanpatpar_dir,
        QUICKSCANFILE.format(QUICKSCANTYPE, now)
    )
    print(f'writing quick scanpattern to: {scanpat_dir}')
    np.savetxt(scanpat_dir, scanpat_a,
               fmt='%.2f', delimiter=', ', newline='\n\n')


    '''CALL ON SOP FUNCTION TO START THE SIGMAMPL PROGRAM'''
    # # intialising system; modifying mpl.ini in SigmaMPL folder
    # ## single quote in last argument accomodates spacing seen by gitbash
    # print(f'setting scan pattern to {scanpat_dir}')
    # comm = """{} -i 's~PATTERNFILE=.*~PATTERNFILE={}~' '{}'""".\
    #     format(
    #         dc_gfunc(WINDOWFILESDIR, SEDFILE), scanpat_dir, MPLCONFIGFILE
    #     )
    # os.system(comm)

    # print(f'setting shot averaging time to {AVERAGINGTIME}')
    # comm = """{} -i 's~AveragingTimeInSeconds=.*""".\
    #     format(dc_gfunc(WINDOWFILESDIR, SEDFILE))\
    #     + """~AveragingTimeInSeconds={}~' '{}'""".\
    #     format(AVERAGINGTIME, MPLCONFIGFILE)
    # os.system(comm)

    # print(f'setting bin resolution mode to {BINRESMODE}')
    # comm = """{} -i 's~BinResolutionMode=.*""".\
    #     format(dc_gfunc(WINDOWFILESDIR, SEDFILE))\
    #     + """~BinResolutionMode={}~' '{}'""".\
    #     format(BINRESMODE, MPLCONFIGFILE)
    # os.system(comm)

    # print('enabling scanpattern usage')
    # comm = """{} -i 's~UseScanFile=.*""".\
    #     format(dc_gfunc(WINDOWFILESDIR, SEDFILE))\
    #     + """~UseScanFile={}~' '{}'""".\
    #     format(1, MPLCONFIGFILE)
    # os.system(comm)

# testing
if __name__ == '__main__':
    main()
