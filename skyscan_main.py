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
import sys
import time

from . import sop
from . import scanpat_calc as spc
from .params import *


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
        super().__init__(target=target, args=args, kwargs=kwargs)        
        self.logfile = logfile
    def run(self):
        '''
        This runs on self.start() in a new process
        '''
        sys.stdout = open(self.logfile, 'a+')
        sys.stderr = open(self.logfile, 'a+')

        if self._target:
            self._target(*self._args, **self._kwargs)

        sys.stdout.close()
        sys.stderr.close()


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

    Future
        AFTER TESTING, CHANGE COPY IN MPL_ORGANISER TO MOVE

    Parameters
        spcNsyncwait_dt (datetime.datetime): time between process runs for 
                                             spcNsync
        fileman_dt (datetime.datetime): time between process runs for file_man
    '''
    try:
        # initialisation        
        print('\nrun {} cold start@{:%Y%m%d%H%M}'.\
              format(__name__, dt.datetime.now()))
        ## updating logfiles
        logpardir = osp.join(MPLDATADIR, DATEFMT).format(dt.datetime.now())
        if not osp.exists(logpardir):
            os.mkdir(logpardir)
        logdir = osp.join(logpardir, PSLOGFILE)
        spcNsync_logdir = logdir.format(dt.datetime.now(), 'spcNsync')
        fileman_logdir = logdir.format(dt.datetime.now(), 'fileman')
        sigmamplboot_logdir = logdir.format(dt.datetime.now(), 'sigmamplboot')        

        ## scanpat_calc for today
        print('run spcNsync@{:%Y%m%d%H%M}...'.format(dt.datetime.now()))    
        pspcNsync = _procwrapper(
            spcNsync_logdir, _spcNsync_func,
            kwargs={'coldstart_boo':True}
        )
        pspcNsync.start()
        pspcNsync.join()

        ## sigmampl_boot
        print('run sigmampl_boot@{:%Y%m%d%H%M}...'.format(dt.datetime.now()))        
        psigmamplboot = _procwrapper(
            sigmamplboot_logdir, sop.sigmampl_boot,
            kwargs={'coldstart_boo':True}
        ).start()

        ## getting next times to start processes
        print('init next time dates@{:%Y%m%d%H%M}...'.format(dt.datetime.now()))
        sigmamplbootnext_dt = sop.scan_init(False)
        spcNsyncnext_dt = dt.datetime.today()
        filemannext_dt = dt.datetime.now()

        print('end {} cold start@{:%Y%m%d%H%M}'.\
              format(__name__, dt.datetime.now()))        
        

        # normal operations
        print('\nrun {} usual operations@{:%Y%m%d%H%M}...'.\
              format(__name__, dt.datetime.now()))
        while True:
            now = dt.datetime.now()

            # updating logfiles
            logpardir = osp.join(MPLDATADIR, DATEFMT).format(now)
            if not osp.exists(logpardir):
                os.mkdir(logpardir)
            logdir = osp.join(logpardir, PSLOGFILE)
            spcNsync_logdir = logdir.format(now, 'spcNsync')
            fileman_logdir = logdir.format(now, 'fileman')
            sigmamplboot_logdir = logdir.format(now, 'sigmamplboot')

            # processes
            if now >= spcNsyncnext_dt:
                print('run spcNsync@{:%Y%m%d%H%M}...'.format(now))
                pspcNsync = _procwrapper(
                    spcNsync_logdir, _spcNsync_func,
                    kwargs={'coldstart_boo':False}
                )
                pspcNsync.start()
                spcNsyncnext_dt += spcNsyncwait_dt

            if now >= filemannext_dt:
                print('run file_man@{:%Y%m%d%H%M}...'.format(now))
                pfileman = _procwrapper(
                    fileman_logdir, sop.file_man,
                    kwargs={'tailend_boo':False}
                )
                pfileman.start()
                filemannext_dt += filemanwait_dt

            if now >= sigmamplbootnext_dt:
                print('run sigmampl_boot@{:%Y%m%d%H%M}...'.format(now))
                psigmamplboot = _procwrapper(
                    sigmamplboot_logdir, sop.sigmampl_boot,
                    kwargs={'coldstart_boo':False,
                            'tailend_boo':False}
                )
                psigmamplboot.start()
                sigmamplbootnext_dt = sop.scan_init(False)


            # trys again every so often
            time.sleep(WAITCHECK)            


    # handles closure
    except KeyboardInterrupt:
        print('\n{} program stop detected @{:%Y%m%d%H%M}'.\
              format(__name__, dt.datetime.now()))

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
            kwargs={'coldstart_boo':False,
                    'tailend_boo':True}
        )
        psigmamplboot.start()
        print('ending with final file transfers...')
        pfileman = _procwrapper(
            fileman_logdir, sop.file_man,
            kwargs={'tailend_boo':True}
        )
        pfileman.start()

        psigmamplboot.join()        
        pfileman.join()
        
        print('{} program ended'.format(__name__))


# testing
if __name__ == '__main__':
    main()

