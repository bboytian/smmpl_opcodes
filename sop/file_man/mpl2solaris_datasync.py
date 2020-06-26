# imports
import datetime as dt
import os

from ...globalimports import *


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
    # getting timings; sync today and yesterday
    if not syncday_lst:
        today = dt.datetime.now()
        syncday_lst = [
            DATEFMT.format(today),
            DATEFMT.format(today - dt.timedelta(1))
        ]

    # rsync
    # verbose from ssh to be removed
    cmd_str = '''{} -azzvi -e "'{}' -v -o 'StrictHostKeyChecking=no' -i '{}'"'''\
        .format(
            dc_gfunc(WINDOWFILESDIR, RSYNCFILE),
            dc_gfunc(WINDOWFILESDIR, SSHFILE), IDRSADIR
        )\
        + ''' -R {}/./{{{}}} {}@{}:{}'''\
        .format(
            _gitbash_mpldatadir, ','.join(syncday_lst),
            SOLARISUSER, SOLARISIP, SOLARISMPLDATADIR
        )
    os.system(cmd_str)


# running
if __name__ == '__main__':
    main()
