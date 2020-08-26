# imports
import os
import multiprocessing as mp

from . import _sigmampl_kill, _postmea_fileman, \
        _mpl2solaris_datasync, _mpl_organiser
from ..global_imports.smmpl_opcodes import *


# main func
@verbose
@announcer(newlineboo=True)
@logger
def main(syncdaylst):
    print('killing SigmaMPL program...')
    _sigmampl_kill()  # always run to kill any exisiting windows
    _postmea_fileman()       # organising files

    print('cleaning up data and syncing...')
    _mpl_organiser(True)
    _mpl2solaris_datasync(syncdaylst)


if __name__ == '__main__':
    import pandas as pd

    syncday_lst = input(
        'list dates you want to sync in DATEFMT, delimited by a single spacing\n'
    )
    syncday_lst = syncday_lst.split(' ')

    try:
        for syncday in syncday_lst:
            if len(syncday) != len(DATEFMT.format(dt.datetime.now())):
                raise ValueError
            pd.Timestamp(syncday)
    except ValueError:
        if syncday_lst != ['']:
            raise ValueError('invalid input')

    if syncday_lst == ['']:  # follows the default sync in .mpl2solaris_datasync
        syncday_lst = None

    main(syncday_lst)
