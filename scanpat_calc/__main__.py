# imports
import datetime as dt
import os
import os.path as osp
import sys

import numpy as np
import pandas as pd

from .pathplanner import pathplanner
from .sunforecaster import sunforecaster
from .targetgenerator import targetgenerator
from .timeobj import timeobj

from ..global_imports.smmpl_opcodes import *


# static params
_finedeltatime = pd.Timedelta(FINEDELTATIME, 'm')  # discretisation of sunswath
                                                   # by cone intersections
_segdelta = pd.Timedelta(SEGDELTA, 'm') # determines time interval of sun swath
                                        # could be a func param in the future

## pathplanner
_angoffset = np.deg2rad(ANGOFFSET)     # [rad] ang offset of lidar from north
                                       # S-N is +X axis, E-W is +Y axis


# main func
@verbose
@announcer(newlineboo=True)
@logger
def main(
        write_boo=True,
        queue=None,
        verb_boo=True,

        starttime=None, endtime=None,
        utcinfo=UTCINFO,
        finedeltatime=_finedeltatime, segdelta=_segdelta,
        deltatime=None,         # for visualisation

        lt=LATITUDE, lg=LONGITUDE, ele=ELEVATION,

        primaryaxis=PRIMARYAXIS, angoffset=_angoffset,
):
    '''
    Parameters
        write_boo (boolean): True => operational mode, run the code for the day
                             False => do not save data, used for visualisation
                             ; fps, equivtime and  must be specified if False
        queue (multiprocessing.Queue): for storing data for visualisation
        verb_boo (boolean): verbose for scanpat_calc output

        start/endtime (datetime like): start and endtime of animation
        utcinfo: controlled in .global_imports.smmpl_opcodes.params
        finedeltatime (timedelta like): discretisation of sun swath
        segdelta (timedelta like): time duration considered when calculating
                                   sunswath
        deltatime (timedelta like): discretisation of animation, specifed only when
                                    animating

        lt, lg, ele: controlled in .global_imports.smmpl_opcodes.params

        primaryaxis, angoffset: controlled in .global_imports.smmpl_opcodes.params

    Return
        date_lst (lst): list of dates in DATEFMT str where scanpattern was
                        calculated and saved
    '''
    # determine timings
    if not starttime:
        starttime = pd.Timestamp(dt.date.today()) \
            + pd.Timedelta(CALCDURATION, 'd')
    if not endtime:
        endtime = starttime + pd.Timedelta(CALCDURATION, 'd')

    # timeobj
    to = timeobj(
        starttime,
        endtime,
        utcinfo,
        finedeltatime,
        segdelta,
        deltatime,
    )

    # sunforecaster
    sf = sunforecaster(
        lt, lg,
        ele
    )

    # pathplanner
    pp = pathplanner(
        primaryaxis,
        angoffset
    )

    # targetgenerator
    if write_boo:
        tg = targetgenerator(
            to, sf, pp,
        )
    else:
        tg = targetgenerator(
            to, sf, pp,
            queue=queue
        )


    # writing targetgenerator data to file
    date_lst = None
    if write_boo:

        toseg_ara = to.get_tosegara()
        date_lst = []
        for i, scanpat_ara in enumerate(tg.get_scanpataralst()):
            filename = toseg_ara[i]
            tosegst = to.get_tosegst(filename)
            toseget = to.get_toseget(filename)
            filename = SCANPATFILE.format(tosegst, toseget)

            date = DATEFMT.format(tosegst)
            date_lst.append(date)

            file_dir = DIRCONFN(MPLDATADIR, date)
            if not osp.isdir(file_dir):
                os.mkdir(file_dir)

            filename = DIRCONFN(file_dir, filename)
            np.savetxt(filename, scanpat_ara,
                       fmt='%.2f', delimiter=', ', newline='\n\n')
        date_lst = list(set(date_lst))
        for date in date_lst:
            print('wrote files to {}'.format(date))

    # returning
    return date_lst

# running
if __name__ == '__main__':
    main(                       # computes the scan pattern for stated time
        write_boo=False,
        starttime=pd.Timestamp('202007210000'),
        endtime=pd.Timestamp('202007220000'),
    )
