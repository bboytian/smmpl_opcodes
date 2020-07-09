# imports
import datetime as dt
import sys

from .mpl2solaris_datasync import main as mpl2solaris_datasync
from .mpl_organiser import main as mpl_organiser

from ...globalimports import *


# main func
@announcer(newlineboo=True)
def main(tailend_boo=False):
    '''
    Parameters
        tailend_boo (boolean): decides whether or not to move the latest mpl file
                               should be True when wrapping up operations
    '''
    mpl_organiser(tailend_boo)
    mpl2solaris_datasync()     # only syncs today and yesterday's data


# testing
if __name__ == '__main__':
    main(False)
