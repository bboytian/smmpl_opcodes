# imports
import time
import datetime as dt
import os.path as osp

from .telegram_API import main as telegram_API
from ..latestfile_read import main as latestfile_read
from ...global_imports.smmpl_opcodes import *



# params
## dynamic
_msg = ''
_msgsent_boo = True
_nextlogtime = dt.datetime.combine(dt.date.today(), dt.time())\
    + dt.timedelta(1)
_timestamp = LOCTIMEFN(_nextlogtime - dt.timedelta(2), UTCINFO)  # start of yest.

## static
_logfilename = 'statusmon'


# main func
def main():
    '''
    Performs a status check every STATUSMONWAIT time interval.
    Has it's own daily logfile

    All status checks are in the status_check module, the thresholds for each
    status check is hept in their respective file.

    depending on how _timestamp is set, only latest mpl profiles areter _timestamp
    onwards will be considered for status checks
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
        mpl_d = latestfile_read()
        if not mpl_d:
            telegram_API('latest mpl profile not found')
            continue

        # checking if this is a new profile
        newtimestamp = mpl_d['Timestamp'][-1]
        if newtimestamp > _timestamp:
            _timestamp = newtimestamp
            _msgsent_boo = False

        # check statuses
            _msg = status_check(mpl_d)

        # check if need to send message
        if msg and not _msgsent_boo:
            telegram_API(msg)
            _msgsent_boo = True
            _msg = ''


        # sleep
        time.sleep(STATUSMONWAIT)




# running
if __name__ == '__main__':
    main()
