# imports
import datetime as dt
import sys

from .mpl2solaris_datasync import main as mpl2solaris_datasync
from .mpl_organiser import main as mpl_organiser

from ...globalimports import *


# main func
@announcer(newlineboo=True, syncday_lst=None)
def main(tailend_boo, ):
    '''
    Parameters
        tailend_boo (boolean): decides whether or not to move the latest mplfile
                               and mpllog file
    '''
    mpl_organiser(tailend_boo)
    mpl2solaris_datasync(syncday_lst)     # only syncs today and yesterday's data


# testing
if __name__ == '__main__':
    import pandas as pd
         
    syncday_lst = input('list dates you want to sync in DATEFMT, delimited by a single spacing')

    try:
        for syncday in syncday_lst:
            if len(syncday) != len(DATEFMT.format(dt.datetime.now())):
                raise ValueError
            pd.Timestamp(syncday)
    except ValueError:
        raise ValueError('invalid input')

    main(
        tailend_boo=True,
        syncday_lst=syncday_lst
    )
