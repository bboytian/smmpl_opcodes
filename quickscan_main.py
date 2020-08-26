# imports
import datetime as dt
import os
import os.path as osp
import time

import numpy as np

from .global_imports.smmpl_opcodes import *
from .quickscanpat_calc import quickscanpat_calc
from .sop import sigmampl_boot


# main func
def main():
    '''
    quick scan pattern parameters are adjusted in their respective scripts,
    i.e. quickscanpat_calc.<quickscantype>

    But quick scanpattern type, bin resolution and shot averaging time are
    controlled in .params

    Parameters
        numtimes (int): number of times we want to measure the same thing
        waittime (float): [s], waiting time between measurements

    Future
        - Handle file management when closing file
    '''
    # setting log file
    now = dt.datetime.now()
    mainlog = DIRCONFN(
        MPLDATADIR, DATEFMT.format(now), QUICKSCANLOG.format(now)
    )
    SETLOGFN(mainlog)
    today = dt.datetime.combine(dt.date.today(), dt.time())
    mainlognext_dt = today + dt.timedelta(1)  # start a new log the next day

    coldstart_boo = True
    for i in range(QUICKSCANTIMES):
        print(f'starting {QUICKSCANTYPE} quickscan {i}...')

        # updating logfile
        now = dt.datetime.now()

        if now >= mainlognext_dt:
            mainlog = DIRCONFN(
                MPLDATADIR, DATEFMT.format(now), QUICKSCANLOG.format(now)
            )
            SETLOGFN(mainlog)
            mainlognext_dt += dt.timedelta(1)


        # calculating scan pattern
        scanpat_a = quickscanpat_calc(QUICKSCANTYPE)

        # writing scan pattern to file
        now = dt.datetime.now()
        scanpatpar_dir = DIRCONFN(
            MPLDATADIR, DATEFMT.format(now)
        )
        if not osp.isdir(scanpatpar_dir):
            os.mkdir(scanpatpar_dir)
        scanpat_dir = DIRCONFN(
            scanpatpar_dir,
            QUICKSCANFILE.format(now)
        )
        print(f'writing quick scanpattern to: {scanpat_dir}')
        np.savetxt(scanpat_dir, scanpat_a,
                   fmt='%.2f', delimiter=', ', newline='\n\n')


        # beginning init and measurement
        sigmampl_boot(
            coldstart_boo=coldstart_boo, scanpat_dir=scanpat_dir,
            stdoutlog=mainlog
        )
        coldstart_boo = False

        # waiting between next measurement
        print(f'waittime: {QUICKSCANWAITTIME}min, next measurement time:'
              f'{dt.datetime.now() + dt.timedelta(minutes=QUICKSCANWAITTIME)}\n')
        time.sleep(QUICKSCANWAITTIME*60)


# testing
if __name__ == '__main__':
    main()
