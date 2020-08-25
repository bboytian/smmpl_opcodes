'''
This script will serve to organise all codes and timings during operation.
Programs will utilise multiprocessing for parallelism.

Codes are scheduled here to side step window's task scheduler.
This allows us to put a single batchfile and a single bash wrapper for the code for the entire operationality of the code in the start up folder

note this code can only be run on the windows laptop itself, else the sigmampl program would open in the background
'''
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
_spcwait_dt = pd.Timedelta(CALCDURATION, 'd')


# main func
def main(
        spcwait_dt=_spcwait_dt,
):
    '''
    This code is written for readability, thus it appears to have some
    redundancy in the booleans.

    Parameters
        spcNsyncwait_dt (datetime.datetime): time between process runs for
                                             spcNsync
        fileman_dt (datetime.datetime): time between process runs for file_man
    '''
    # initialisation
    print((TIMEFMT + ' run {} cold start').format(
            dt.datetime.now(), __name__
    ))

    ## getting next times to start processes
    today = dt.datetime.combine(dt.date.today(), dt.time())
    tomorrow = today + dt.timedelta(1)
    mainlognext_dt = tomorrow
    spcnext_dt = tomorrow
    sigmamplbootnext_dt = sop.scan_init(False)

    ## updating logfile
    SETLOGFN(DIRCONFN(
        MPLDATADIR, DATEFMT.format(today),
        SKYSCANLOG.format(today)
    ))

    ## scanpat_calc for today
    scanpat_calc(
        starttime=today,
        endtime=today + pd.Timedelta(CALCDURATION + DAYSINADV, 'd'),
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

    print(f'letting SigmaMPL warm up for {SIGMAMPLWARMUP}s'
          ' before continuing with usual operations')
    time.sleep(SIGMAMPLWARMUP)

    print((TIMEFMT + ' end {} cold start\n').format(
        dt.datetime.now(), __name__
    ))


    # normal operations
    print((TIMEFMT + ' run {} usual operations').format(
        dt.datetime.now(), __name__
    ))
    while True:
        today = dt.datetime.combine(dt.date.today(), dt.time())
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
            mp.Process(
                target=scanpat_calc,
                kwargs={
                    'starttime': today,
                    'endtime': today + pd.Timedelta(CALCDURATION, 'd'),
                    'stdoutlog': DIRCONFN(
                        MPLDATADIR, DATEFMT.format(today), SPCLOG.format(today)
                    ),
                    'dailylogboo': True
                }
            ).start()
            spcnext_dt += spcwait_dt

        if now >= sigmamplbootnext_dt:
            mp.Process(
                target=sop.sigmampl_boot,
                kwargs={
                    'coldstart_boo': False,
                    'stdoutlog': DIRCONFN(
                        MPLDATADIR, DATEFMT.format(today),
                        SIGMAMPLBOOTLOG.format(today)
                    ),
                    'dailylogboo': True
                }
            ).start()
            sigmamplbootnext_dt = sop.scan_init(False)


        # trys again every so often
        time.sleep(SKYSCANWAIT)


# testing
if __name__ == '__main__':
    main()
