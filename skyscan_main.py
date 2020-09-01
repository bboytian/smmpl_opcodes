# imports
import datetime as dt
import multiprocessing as mp
import os
import os.path as osp
import pandas as pd
import time

from . import sop
from .scanpat_calc import main as scanpat_calc
from .global_imports.smmpl_opcodes import *


# params
_spcstarttime = dt.time(SPCSTARTHOUR, SPCSTARTMIN)

# main func
def main():
    '''
    measurement protocol for reading the clouds
    '''
    # initialisation

    ## updating logfile
    todaydate = dt.date.today()
    today = dt.datetime.combine(todaydate, dt.time())
    SETLOGFN(DIRCONFN(
        MPLDATADIR, DATEFMT.format(today),
        SKYSCANLOG.format(today)
    ))

    print((TIMEFMT + ' run {} cold start').format(
            dt.datetime.now(), __name__
    ))

    ## scanpat_calc for today
    now = dt.datetime.now()
    starttime = dt.datetime.combine(todaydate, _spcstarttime)
    # compute scan pattern for previous day if time has already passed
    if now < starttime:
        starttime -= dt.timedelta(1)
    endtime = starttime + pd.Timedelta(CALCDURATION + DAYSINADV, 'd')
    scanpat_calc(
        starttime=starttime,
        endtime=endtime,
        stdoutlog=DIRCONFN(
            MPLDATADIR, DATEFMT.format(today), SPCLOG.format(today)
        ),
        dailylogboo=True
    )

    ## starting sigmaMPL program
    sop.sigmampl_boot(
        coldstart_boo=True,
        stdoutlog=DIRCONFN(
            MPLDATADIR, DATEFMT.format(today), SIGMAMPLBOOTLOG.format(today)
        ),
        dailylogboo=True
    )

    ## getting next times to start processes
    tomorrow = today + dt.timedelta(1)
    mainlognext_dt = tomorrow
    spcnext_dt = starttime + dt.timedelta(1)
    sigmamplbootnext_dt = sop.scan_init(False, verbboo=False)

    print((TIMEFMT + ' end {} cold start\n').format(
        dt.datetime.now(), __name__
    ))


    # normal operations
    print((TIMEFMT + ' run {} usual operations').format(
        dt.datetime.now(), __name__
    ))
    while True:
        todaydate = dt.date.today()
        today = dt.datetime.combine(todaydate, dt.time())
        now = dt.datetime.now()

        # main thread log update
        if now >= mainlognext_dt:
            SETLOGFN(DIRCONFN(
                MPLDATADIR, DATEFMT.format(today),
                SKYSCANLOG.format(today)
            ))
            mainlognext_dt += dt.timedelta(1)

        # processes
        if now >= spcnext_dt:
            print((TIMEFMT + ' run {}.{}').format(
                dt.datetime.now(),
                scanpat_calc.__module__, scanpat_calc.__name__
            ))
            starttime = dt.datetime.combine(todaydate, _spcstarttime) + \
                pd.Timedelta(DAYSINADV, 'd')
            stdoutlog = DIRCONFN(
                MPLDATADIR, DATEFMT.format(today), SPCLOG.format(today)
            )
            MPPROCWRAPCL(
                target=scanpat_calc,
                stdoutlog=stdoutlog,
                kwargs={
                    'starttime': starttime,
                    'endtime': starttime + pd.Timedelta(CALCDURATION, 'd'),
                    'stdoutlog': stdoutlog,
                    'dailylogboo': True
                }
            ).start()
            spcnext_dt += dt.timedelta(1)

        if now >= sigmamplbootnext_dt:
            print((TIMEFMT + ' run {}.{}').format(
                dt.datetime.now(),
                sop.sigmampl_boot.__module__, sop.sigmampl_boot.__name__
            ))
            stdoutlog = DIRCONFN(
                MPLDATADIR, DATEFMT.format(today), SIGMAMPLBOOTLOG.format(today)
            )
            MPPROCWRAPCL(
                target=sop.sigmampl_boot,
                kwargs={
                    'coldstart_boo': False,
                    'stdoutlog': stdoutlog,
                    'dailylogboo': True
                }
            ).start()
            sigmamplbootnext_dt = sop.scan_init(False, verbboo=False)


        # trys again every so often
        time.sleep(SKYSCANWAIT)


# testing
if __name__ == '__main__':
    main()
