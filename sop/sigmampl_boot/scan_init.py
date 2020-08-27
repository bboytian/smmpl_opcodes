'''
This script serves to initialise the mpl config file before every measurement.
It is to be run on boot of the scanning mini mpl windows laptop

It does the follwing:
1. change the scan pattern

Notes
- this script is written specifically for windows 10 machines, due to directories
being involved
'''
# imports
import datetime as dt
import os
import os.path as osp

import numpy as np
import pandas as pd

from ...global_imports.smmpl_opcodes import *


# supp function
def _datestrfmt_funcfunc(start):
    def datestrfmt_func(datestr):
        return datestr[start:start+TIMELEN]
    return datestrfmt_func


# main function
@verbose
@announcer
def main(init_boo, static_boo=False, scanpat_dir=None):
    '''
     Parameters
        init_boo (boolean): determines whether to init scan pattern or return
        static_boo (boolean): initialises the scanner to a static angle,
                              not saving the data
        scanpat_dir (str): if provided, initialises using this scanpattern file
    Return
        datetime.datetime object of the endtime of the current scan pattern
    '''
    if not scanpat_dir:
        # finding the right scanpat file
        today = dt.datetime.now()
        yesterday = today - dt.timedelta(1)
        today_dir = DIRCONFN(MPLDATADIR, DATEFMT.format(today))
        yesterday_dir = DIRCONFN(MPLDATADIR, DATEFMT.format(yesterday))

        data_filelst = []
        try:
            data_filelst += os.listdir(yesterday_dir)
        except FileNotFoundError:
            pass
        data_filelst = os.listdir(today_dir) + data_filelst
        data_filelst = list(filter(
            lambda x: SCANPATFILE[SCANPATDATEIND:] in x,
            data_filelst
        ))

        sdate_ara = list(map(_datestrfmt_funcfunc(SCANPATSDATEIND), data_filelst))
        edate_ara = list(map(_datestrfmt_funcfunc(SCANPATEDATEIND), data_filelst))
        sdate_ara = pd.to_datetime(sdate_ara)
        edate_ara = pd.to_datetime(edate_ara)
        boo_ara = (sdate_ara <= today) * (today < edate_ara)

        # getting scanpat file
        try:
            scanpat_file = data_filelst[np.argwhere(boo_ara)[0][0]]
        except IndexError:
            raise Exception(
                'scanpattern for {} to {} not calculated'.
                format(DATEFMT.format(yesterday), DATEFMT.format(today))
            )
        scanpat_dir = DIRCONFN(today_dir, scanpat_file)
        if not osp.exists(scanpat_dir):
            scanpat_dir = DIRCONFN(yesterday_dir, scanpat_file)

        scanpat_dir = scanpat_dir.replace('\\', '/')  # os.listdir creates '\'
                                                  # in windows

    if init_boo:                # configuring mpl.ini file
        if static_boo:          # init for static angle position
            # writing static scanpattern file
            np.savetxt(STATICSCANPATFILE, [[STATICAZIMUTH, STATICELEVATION]],
                       fmt='%.2f', delimiter=', ', newline='\n\n')

            print(f'setting scan pattern to {STATICSCANPATFILE}')
            comm = """{} -i 's~PATTERNFILE=.*~PATTERNFILE={}~' '{}'""".\
                format(
                    DIRCONFN(WINDOWFILESDIR, SEDFILE), STATICSCANPATFILE,
                    MPLCONFIGFILE
                )
            os.system(comm)

        else:                   # init for measurement
            print(f'setting scan pattern to {scanpat_dir}')
            comm = """{} -i 's~PATTERNFILE=.*~PATTERNFILE={}~' '{}'""".\
                format(
                    DIRCONFN(WINDOWFILESDIR, SEDFILE), scanpat_dir, MPLCONFIGFILE
                )
            os.system(comm)

        print(f'setting shot averaging time to {AVERAGINGTIME}')
        comm = """{} -i 's~AveragingTimeInSeconds=.*""".\
            format(DIRCONFN(WINDOWFILESDIR, SEDFILE))\
            + """~AveragingTimeInSeconds={}~' '{}'""".\
            format(AVERAGINGTIME, MPLCONFIGFILE)
        os.system(comm)

        print(f'setting bin resolution mode to {BINRESMODE}')
        comm = """{} -i 's~BinResolutionMode=.*""".\
            format(DIRCONFN(WINDOWFILESDIR, SEDFILE))\
            + """~BinResolutionMode={}~' '{}'""".\
            format(BINRESMODE, MPLCONFIGFILE)
        os.system(comm)

        print(f'scanpattern usage set to {ENABLESCANPATBOO}')
        comm = """{} -i 's~UseScanFile=.*""".\
            format(DIRCONFN(WINDOWFILESDIR, SEDFILE))\
            + """~UseScanFile={}~' '{}'""".\
            format(ENABLESCANPATBOO, MPLCONFIGFILE)
        os.system(comm)

        print(f'control scanner set to {ENABLESCANNER}')
        comm = """{} -i -e ':a' -e 'N' -e '$!ba' """.\
            format(DIRCONFN(WINDOWFILESDIR, SEDFILE))\
            + """-e 's~\[SCANNER\]\\nCONTROL=.*\\nTYPE~"""\
            + """\[SCANNER\]\\nCONTROL={}\\nTYPE~' '{}'""".\
            format(ENABLESCANNER, MPLCONFIGFILE)
        os.system(comm)

    else:                       # to find out next init date
        try:
            return edate_ara[np.argwhere(boo_ara)[0][0]]
        except IndexError:
            raise Exception(
                'scanpattern for {} not calculated'.
                format(DATEFMT.format(today))
            )


# running
if __name__ == '__main__':
    main(True)
