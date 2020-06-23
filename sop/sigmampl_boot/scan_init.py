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

from ...params import *


# supp function
def _datestrfmt_funcfunc(start):
    def datestrfmt_func(datestr):
        return datestr[start:start+TIMELEN]
    return datestrfmt_func


# main function
def main(init_boo):
    '''
    Future
        - can optimise finding right scan pattern by just relying on the start
          date, and using np.argmax

    Parameters
        init_boo (boolean): determines whether to init scan pattern or return
    Return
        datetime.datetime object of the endtime of the current scan pattern
    '''
    if init_boo:
        print('start {}@{:%Y%m%d%H%M}'.\
              format(__name__, dt.datetime.now()))
    # finding the right scanpat file
    today = dt.datetime.now()
    yesterday = today - dt.timedelta(1)
    today_dir = osp.join(MPLDATADIR, DATEFMT.format(today))
    yesterday_dir = osp.join(MPLDATADIR, DATEFMT.format(yesterday))
    if init_boo:
        data_filelst = os.listdir(today_dir) + os.listdir(yesterday_dir)
    else:
        data_filelst = os.listdir(today_dir)
    data_filelst = list(filter(
        lambda x: SCANPATFILE[SCANPATDATEIND:] in x,
        data_filelst
    ))
    sdate_ara = list(map(_datestrfmt_funcfunc(SCANPATSDATEIND), data_filelst))
    edate_ara = list(map(_datestrfmt_funcfunc(SCANPATEDATEIND), data_filelst))
    sdate_ara = pd.to_datetime(sdate_ara)
    edate_ara = pd.to_datetime(edate_ara)
    boo_ara = (sdate_ara <= today) * (today < edate_ara)

    if init_boo:
        pass
        # try:
        #     scanpat_file = data_filelst[np.argwhere(boo_ara)[0][0]]
        # except IndexError:
        #     raise Exception(
        #         'scanpattern for {} to {} not calculated'.\
        #         format(DATEFMT.format(yesterday), DATEFMT.format(today))
        #     )
        # scanpat_dir = osp.join(today_dir, scanpat_file)
        # scanpat_dir = scanpat_dir.replace('\\', '/') #os.listdir creates '\'
        #                                              # in windows
        # # replacing line in mpl init file
        # ## single quote in last argument accomodates for spacing seen by gitbash
        # print(f'setting scan pattern to {scanpat_dir}')
        # comm = """sed -i 's~PATTERNFILE=.*~PATTERNFILE={}~' '{}'""".\
        #     format(scanpat_dir, MPLCONFIGFILE)
        # os.system(comm)

        # print(f'setting bin resolution mode to {BINRESMODE}')
        # comm = """sed -i 's~BinResolutionMode=.*"""\
        #     + """~BinResolutionMode={}~' '{}'""".\
        #     format(BENRESMODE, MPLCONFIGFILE)
        # os.system(comm)

        # print('enabling scanpattern usage')
        # comm = """sed -i 's~UseScanFile=.*"""\
        #     + """~UseScanFile={}~' '{}'""".\
        #     format(1, MPLCONFIGFILE)
        # os.system(comm)

        print('done {}@{:%Y%m%d%H%M}'.\
              format(__name__, dt.datetime.now()))
        
    else:
        try:
            return edate_ara[np.argwhere(boo_ara)[0][0]]
        except IndexError:
            raise Exception(
                'scanpattern for {} not calculated'.\
                format(DATEFMT.format(today))
            )        
    

# running
if __name__ == '__main__':
    main()
