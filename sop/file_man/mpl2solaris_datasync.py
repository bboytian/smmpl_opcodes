# imports
import datetime as dt
import os
import subprocess as sub

from ...global_imports.smmpl_opcodes import *


# static params
_gitbash_mpldatadir = MPLDATADIR.replace('C:', '/cygdrive/c') # required for rsync

# main func
@announcer
def main(syncday_lst=None):
    '''
    code has to be run by gitbash, as rsync is in gitbash
    uses rsync to sync specified data folder with specified data folder
    in solaris
    By default syncs current day and previous day's data.

    Parameters
        syncday_lst (lst): list objects are strings of the format DATEFMT
    '''
    sync_boo = True
    if not syncday_lst:           # normal operations transfer
        today = dt.datetime.now()    # getting timings; sync today and yesterday
        syncday_lst = [
            DATEFMT.format(today),
            DATEFMT.format(today - dt.timedelta(1))
        ]
    elif syncday_lst == ['']:   # empty input from running sop.file_man independent
        sync_boo = False


    if sync_boo:
        # rsync
        cmd_l = [
            f'{DIRCONFN(WINDOWFILESDIR, RSYNCFILE)}',
            '-azzvi',
            f"-e '{DIRCONFN(WINDOWFILESDIR, SSHFILE)}' -o 'StrictHostKeyChecking=no' -i '{IDRSADIR}'",
            '{}/./{{{}}}'.format(_gitbash_mpldatadir, ','.join(syncday_lst)),
            '{}@{}:{}'.format(SOLARISUSER, SOLARISIP, SOLARISMPLDATADIR)
        ]
        cmd_subrun = sub.run(cmd_l, stdout=sub.PIPE, stderr=sub.STDOUT)
        print(cmd_subrun.stdout.decode('utf-8'))


# running
if __name__ == '__main__':
    main()
