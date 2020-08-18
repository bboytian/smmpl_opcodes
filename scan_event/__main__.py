# imports
import datetime as dt
import os
import os.path as osp
import time

import pandas as pd

from .status_mon import main as status_mon
from .telegram_API import main as telegram_API
from .latestfile_read import main as latestfile_read
from .nonewprofile_check import main as nonewprofile_check
from ..global_imports.smmpl_opcodes import *



# params
_msgprepend = f'''Notification from {__name__}
'''

_operations_l = [
    status_mon,
    nonewprofile_check,
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
    msgsent_boo = False
    netmsg_hash = 0

    while True:
        today = dt.datetime.combine(dt.date.today(), dt.time())
        now = LOCTIMEFN(dt.datetime.now(), UTCINFO)

        # update logbook
        if today >= mainlognext_dt:
            logpardir = DIRCONFN(MPLDATADIR, DATEFMT).format(today)
            if not osp.exists(logpardir):
                os.mkdir(logpardir)
            logdir = DIRCONFN(logpardir, PSLOGFILE).format(today, SCANEVENTLOG)
            SETLOGFN(logdir)
            mainlognext_dt += dt.timedelta(1)

        # retrieve latest dataset
        mpl_d = latestfile_read(verbboo=True)
        if not mpl_d:
            print(TIMEFMT.format(now) + ' ERROR: not able to find latest file')
            msg = _msgprepend + 'Error: unable to find latest file'
            telegram_API(msg)
            continue

        # performing operations
        netmsg = ''.join([op(mpl_d) for op in _operations_l])
        newnetmsg_hash = hash(netmsg)

        # checking if we have a new message to send
        if newnetmsg_hash != netmsg_hash:
            netmsg_hash = newnetmsg_hash

        # sending message
            if netmsg:
                print(TIMEFMT.format(now) + ' sending notification')
                print('message:')
                print('\n'.join(['\t' + line for line in netmsg.split('\n')]))

                feedback_l = telegram_API(_msgprepend + netmsg)

                print('telegram feedback')
                for feedback in feedback_l:
                    for key, val in feedback.items():
                        print(f'\t{key}: {val}')


        # sleep
        time.sleep(SCANEVENTWAIT)




# running
if __name__ == '__main__':
    main()
