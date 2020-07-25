# imports
import time
import datetime as dt
import os.path as osp

from .telegram_API import main as telegram_API
from ..globalimports import *

# mutable params
_msgsent_boo = True
_timestamp = None

_nextlogtime = None
_logfilename = 'statusmon'


# main func
def main():
    '''
    Performs a status check every STATUSMONWAIT time interval.
    Has it's own daily logfile

    All status checks are in the status_check module, the thresholds for each
    status check is hept in their respective file.
    '''
    while True:
        today = dt.datetime.combine(dt.date.today(), dt.time())

        # update logbook
        if today >= _nextlogtime:
            logpardir = DIRCONFN(MPLDATADIR, DATEFMT).format(today)
            if not osp.exists(logpardir):
                os.mkdir(logpardir)
            logdir = DIRCONFN(logpardir, PSLOGFILE).format(today, _logfilename)
            SETLOGFN(logdir)
            _nextlogtime = today + dt.timedelta(1)  # start new logfile tmr

        # retrieve latest dataset
        ## retreiving directories to look for data files
        now = dt.datetime.now()
        datadirs_l = [DIRCONFN(MPLDATADIR, DATEFMT.format(date))
                      for date in [now, now - dt.timedelta(1)]]
        datampl_l = FINDFILESFN(MPLFILE, datadirs_l)
        datampl_l.sort()
        sigmampl_l = FINDFILESFN(MPLFILE, MPLSIGMADATADIR)
        sigmampl_l.sort()
        try:
            lastdatampl = datampl_l[-1]
        except IndexError:
            raise IndexError(f'{datadirs_l}')
        try:
            lastsigampl = sigmampl_l[-1]
        except IndexError:
            lastmpl = datadirs_l[-1]
        '''CONTINUE IMPLEMENTING HERE THE VARIOUS CASES'''


        newtimestamp =

        # check statuses
        msg =
        sendmsg_boo =

        # check if need to send message
        if sendmsg_boo and not _msgsent_boo:
            telegram_API(msg)


        # sleep
        time.sleep(STATUSMONWAIT)




# running
if __name__ == '__main__':
    main()
