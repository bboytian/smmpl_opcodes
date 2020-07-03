# imports
import datetime as dt
import os
import subprocess as sub

from ...globalimports import *


# static params
_gitbash_mpldatadir = MPLDATADIR.replace('C:', '/cygdrive/c') # required for rsync

# main func
@announcer
def main(logfile, syncday_lst=None):
    '''
    code has to be run by gitbash, as rsync is in gitbash
    uses rsync to sync specified data folder with specified data folder
    in solaris
    By default syncs current day and previous day's data.

    Parameters
        syncday_lst (lst): list objects are strings of the format DATEFMT
    '''
    # getting timings; sync today and yesterday
    if not syncday_lst:
        today = dt.datetime.now()
        syncday_lst = [
            DATEFMT.format(today),
            DATEFMT.format(today - dt.timedelta(1))
        ]

    # rsync
    cmd_l = [
        f'{DIRCONFN(WINDOWFILESDIR, RSYNCFILE)}',
        '-azzvi',
        f"-e '{DIRCONFN(WINDOWFILESDIR, SSHFILE)}' -o 'StrictHostKeyChecking=no' -i 'C:/Users/mpluser/.ssh/id_rsa'",
        '{}/./{{{}}}'.format(_gitbash_mpldatadir, ','.join(syncday_lst)),
        '{}@{}:{}'.format(SOLARISUSER, SOLARISIP, SOLARISMPLDATADIR)
    ]
    cmd_subrun = sub.run(cmd_l, stdout=sub.PIPE, stderr=sub.STDOUT)
    print(cmd_subrun.stdout.decode('utf-8'))


# running
if __name__ == '__main__':
    main()
