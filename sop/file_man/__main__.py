# imports
import datetime as dt
import sys

from .mpl2solaris_datasync import main as mpl2solaris_datasync
from .mpl_organiser import main as mpl_organiser


# main func
def main(tailend_boo=False):
    '''
    Parameters
        tailend_boo (boolean): decides whether or not to move the latest mpl file
                               should be True when wrapping up operations
    '''
    print('\nrun {}@{:%Y%m%d%H%M}'.format(__name__, dt.datetime.now()))
    
    mpl_organiser(tailend_boo)
    mpl2solaris_datasync()     # only syncs today and yesterday's data

    print('end {}@{:%Y%m%d%H%M}'.format(__name__, dt.datetime.now()))

# testing
if __name__ == '__main__':
    main(False)
