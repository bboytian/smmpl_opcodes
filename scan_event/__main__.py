# imports
import datetime as dt
import os
import os.path as osp
import time

from .status_mon import main as status_mon
from .telegram_API import main as telegram_API
from .latestfile_read import main as latestfile_read
from ..global_imports.smmpl_opcodes import *



# params
_msgprepend = f'''Notification from {__name__}
'''

_operations_l = [
    status_mon,
    # nonewprofile_check,
]


# main func
def main():
    '''
    Performs a scannner status probe every SCANEVENTWAIT time interval.
    Has it's own daily logfile, while each operation has it's own log file

    The operations on the latest data profile are extensible by including more
    functions in the _operations_l
    '''
    # setting log file
    today = dt.datetime.combine(dt.date.today(), dt.time())
    logpardir = DIRCONFN(MPLDATADIR, DATEFMT).format(today)
    if not osp.exists(logpardir):
        os.mkdir(logpardir)
    logdir = DIRCONFN(logpardir, PSLOGFILE).format(today, SCANEVENTLOG)
    SETLOGFN(logdir)
    mainlognext_dt = today + dt.timedelta(1)  # start a new log the next day

    # initialising mutable parameters
    netmsg = ''
    statusmomsg = ''
    timestamp = dt.datetime.now()
    msgsent_boo = False

    while True:
        today = dt.datetime.combine(dt.date.today(), dt.time())
        now = dt.datetime.now()

        # update logbook
        if today >= mainlognext_dt:
            logpardir = DIRCONFN(MPLDATADIR, DATEFMT).format(today)
            if not osp.exists(logpardir):
                os.mkdir(logpardir)
            logdir = DIRCONFN(logpardir, PSLOGFILE).format(today, SCANEVENTLOG)
            SETLOGFN(logdir)
            mainlognext_dt += dt.timedelta(1)

        # retrieve latest dataset
        mpl_d = latestfile_read()
        if not mpl_d:
            print(TIMEFMT.format(now) + ' ERROR: not able to find latest file')
            msg = _msgprepend + 'Error: unable to find latest file'
            telegram_API(msg)
            continue

        # checking if this is a new profile
        newtimestamp = mpl_d['Timestamp'][-1]
        if newtimestamp > timestamp:
            timestamp = newtimestamp
            msgsent_boo = False

        # performing operations
            netmsg = ''.join([op(mpl_d) for op in _operations_l])

        # check if need to send message
        if netmsg and not msgsent_boo:
            print(TIMEFMT.format(now) + ' sending notification')
            print('message:')
            print('\n'.join(['\t' + line for line in netmsg.split('\n')]))

            feedback_l = telegram_API(_msgprepend + netmsg)

            print('telegram feedback')
            for feedback in feedback_l:
                for key, val in feedback.items():
                    print(f'\t{key}: {val}')
            msgsent_boo = True
            netmsg = ''


        # sleep
        time.sleep(SCANEVENTWAIT)




# running
if __name__ == '__main__':
    main()
