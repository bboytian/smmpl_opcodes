# imports
import datetime as dt
import sys
import time

import pandas as pd

from .mpl2solaris_datasync import main as mpl2solaris_datasync
from .mpl_organiser import main as mpl_organiser

from ...global_imports.smmpl_opcodes import *


# params
_filemanwait = pd.Timedelta(FILEMANWAIT, 'm').total_seconds()


# main func
@verbose
@announcer(newlineboo=True)
def main(tailend_boo, syncday_lst=None):
    '''
    Parameters
        tailend_boo (boolean): decides whether or not to move the latest mplfile
                               and mpllog file
    '''
    # setting log file
    today = dt.datetime.combine(dt.date.today(), dt.time())
    SETLOGFN(DIRCONFN(
        MPLDATADIR, DATEFMT.format(today),
        FILEMANLOG.format(today)
    ))
    mainlognext_dt = today + dt.timedelta(1)  # start a new log the next day

    while True:
        today = dt.datetime.combine(dt.date.today(), dt.time())

        # update logbook
        if today >= mainlognext_dt:
            SETLOGFN(DIRCONFN(
                MPLDATADIR, DATEFMT.format(today),
                FILEMANLOG.format(today)
            ))
            mainlognext_dt += dt.timedelta(1)

        mpl_organiser(tailend_boo)
        mpl2solaris_datasync(syncday_lst)  # only syncs today and yesterday's data

        time.sleep(_filemanwait)

# running
if __name__ == '__main__':
    main(False)
