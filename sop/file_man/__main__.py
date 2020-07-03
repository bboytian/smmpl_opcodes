# imports
import datetime as dt
import sys

from .mpl2solaris_datasync import main as mpl2solaris_datasync
from .mpl_organiser import main as mpl_organiser

from ...globalimports import *


# main func
@announcer(newlineboo=True)
def main(logfile=None, tailend_boo=False):
    '''
    Parameters
        logfile (str): log file for rsync process to write to
        tailend_boo (boolean): decides whether or not to move the latest mpl file
                               should be True when wrapping up operations
    '''
    mpl_organiser(tailend_boo)
    mpl2solaris_datasync(logfile)     # only syncs today and yesterday's data

# testing
if __name__ == '__main__':
    main(False)
