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
from . import scanpat_calc as spc
from .global_imports.smmpl_opcodes import *


# params
_spcNsyncwait_dt = pd.Timedelta(CALCDURATION, 'd')
_filemanwait_dt = pd.Timedelta(FILEMANWAIT, 'm')


# Process class
class _procwrapper(mp.Process):
    '''
    To be used in a way similar to multiprocessing.Process.
    It logs the print statements in the specified logfiles
    '''
    def __init__(self, logfile, target, args=(), kwargs={}):
        print(
            (TIMEFMT + ' run {}.{}...'.
            format(dt.datetime.now(), target.__module__, target.__name__)
        )
        super().__init__(target=target, args=args, kwargs=kwargs)
        self.logfile = logfile

    def run(self):
        '''
        This runs on self.start() in a new process
        '''
        SETLOGFN(self.logfile)
        if self._target:
            self._target(*self._args, **self._kwargs)
        SETLOGFN()


# secondary processes target
def _spcNsync_func(coldstart_boo=False, starttime=None):
    '''
    performs scanpattern calculation, and syncs it to server

    scan pattern is calculated one day before

    Parameters
        coldstart_boo (boolean): choses whether or not to perform scanpattern
                                 calculation from one day before now till
                                 CALCDURATION later
    '''
    if coldstart_boo:
        starttime = pd.Timestamp(dt.date.today() - dt.timedelta(DAYSINADV))
        date_lst = spc.scanpat_calc(
            starttime=starttime,
            endtime=starttime + pd.Timedelta(CALCDURATION+DAYSINADV, 'd')
        )
    else:
        date_lst = spc.scanpat_calc()
    sop.mpl2solaris_datasync(date_lst)


# main func
def main(
        spcNsyncwait_dt=_spcNsyncwait_dt,
        filemanwait_dt=_filemanwait_dt,
):
    '''
    This code is written for readability, thus it appears to have some
    redundancy in the booleans.

    Parameters
        spcNsyncwait_dt (datetime.datetime): time between process runs for
                                             spcNsync
        fileman_dt (datetime.datetime): time between process runs for file_man
    '''
    try:
        # initialisation

        ## updating logfiles
        logpardir = DIRCONFN(MPLDATADIR, DATEFMT).format(dt.datetime.now())
        if not osp.exists(logpardir):
            os.mkdir(logpardir)
        logdir = DIRCONFN(logpardir, PSLOGFILE)
        spcNsync_logdir = logdir.format(dt.datetime.now(), SPCNSYNCLOG)
        fileman_logdir = logdir.format(dt.datetime.now(), FILEMANLOG)
        sigmamplboot_logdir = logdir.format(dt.datetime.now(), SIGMAMPLBOOTLOG)
        main_logdir = logdir.format(dt.datetime.now(), SKYSCANLOG)

        ## start
        SETLOGFN(main_logdir)
        print(
            (TIMEFMT + ' run {} cold start'.
            format(dt.datetime.now(), __name__)
        )

        ## scanpat_calc for today
        pspcNsync = _procwrapper(
            spcNsync_logdir, _spcNsync_func,
            kwargs={'coldstart_boo':True}
        )
        pspcNsync.start()
        pspcNsync.join()

        ## sigmampl_boot
        SETLOGFN(sigmamplboot_logdir)
        sop.sigmampl_boot(coldstart_boo=True)
        SETLOGFN(main_logdir)  # giving stdout back to main log

        print(f'letting SigmaMPL warm up for {SIGMAMPLWARMUP}s before continuing with usual operations')
        time.sleep(SIGMAMPLWARMUP)

        ## getting next times to start processes
        today = dt.datetime.combine(dt.date.today(), dt.time())
        sigmamplbootnext_dt = sop.scan_init(False)
        spcNsyncnext_dt = today
        filemannext_dt = dt.datetime.now()
        mainlognext_dt = today + dt.timedelta(1)  # start a new log the
                                                            # next day

        print(
            (TIMEFMT + ' end {} cold start\n'.
            format(dt.datetime.now(), __name__)
        )

        # normal operations
        print(
            (TIMEFMT + ' run {} usual operations'.
            format(dt.datetime.now(), __name__)
        )
        while True:
            now = dt.datetime.now()

            # updating logfiles
            logpardir = DIRCONFN(MPLDATADIR, DATEFMT).format(now)
            if not osp.exists(logpardir):
                os.mkdir(logpardir)
            logdir = DIRCONFN(logpardir, PSLOGFILE)
            spcNsync_logdir = logdir.format(now, SPCNSYNCLOG)
            fileman_logdir = logdir.format(now, FILEMANLOG)
            sigmamplboot_logdir = logdir.format(now, SIGMAMPLBOOTLOG)
            main_logdir = logdir.format(now, SKYSCANLOG)

            # main thread log update
            if now >= mainlognext_dt:
                SETLOGFN(main_logdir)
                mainlognext_dt += dt.timedelta(1)

            # processes
            if now >= spcNsyncnext_dt:
                pspcNsync = _procwrapper(
                    spcNsync_logdir, _spcNsync_func,
                    kwargs={'coldstart_boo': False}
                )
                pspcNsync.start()
                spcNsyncnext_dt += spcNsyncwait_dt

            if now >= filemannext_dt:
                pfileman = _procwrapper(
                    fileman_logdir, sop.file_man,
                    kwargs={'tailend_boo': False}
                )
                pfileman.start()
                filemannext_dt += filemanwait_dt

            if now >= sigmamplbootnext_dt:
                psigmamplboot = _procwrapper(
                    sigmamplboot_logdir, sop.sigmampl_boot,
                    kwargs={
                        'coldstart_boo': False,
                        'tailend_boo': False
                    }
                )
                psigmamplboot.start()
                sigmamplbootnext_dt = sop.scan_init(False)


            # trys again every so often
            time.sleep(WAITCHECK)


    # handles closure
    except KeyboardInterrupt:
        print(
            ('\n' + TIMEFMT + ' {} program stop detected').
            format(dt.datetime.now(), __name__)
        )
        print('waiting for child processes to stop..')
        try:
            pspcNsync.join()
            psigmamplboot.join()
        except (NameError, AttributeError) as err:
            pass
        try:
            pfileman.join()
        except (NameError, AttributeError) as err:
            pass

        print('killing SigmaMPL program...')
        psigmamplboot = _procwrapper(
            sigmamplboot_logdir, sop.sigmampl_boot,
            kwargs={
                'coldstart_boo': False,
                'tailend_boo': True
            }
        )
        psigmamplboot.start()
        print('ending with final file transfers...')
        pfileman = _procwrapper(
            fileman_logdir, sop.file_man,
            kwargs={'tailend_boo': True}
        )
        pfileman.start()

        psigmamplboot.join()
        pfileman.join()

        print(
            (TIMEFMT + ' {} terminated').
            format(dt.datetime.now(), __name__)
        )

        # setting the main thread log file back to default
        SETLOGFN()


# testing
if __name__ == '__main__':
    main()
