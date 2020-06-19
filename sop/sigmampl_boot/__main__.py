# imports
import datetime as dt

from .sigmampl_startkill import *
from .scan_init import main as scan_init
from .prepostmea_fileman import premea_fileman, postmea_fileman


# main func
def main(coldstart_boo=False, tailend_boo=False):
    '''
    Parameters
        coldstart_boo (boolean): determines whether measurement is testing for 
                                 the first time, or testing operationally
        tailend_boo (boolean): decides whether or not to move the latest mpl file
                               should be True when wrapping up operations
    '''
    print('\nrun {}@{:%Y%m%d%H%M}'.format(__name__, dt.datetime.now()))
    
    sigmampl_kill()             # always run to kill any exisiting windows
    if not coldstart_boo:
        postmea_fileman()
    premea_fileman(coldstart_boo)
    if not tailend_boo:
        scan_init(init_boo=True)
        sigmampl_start()

    print('end {}@{:%Y%m%d%H%M}'.format(__name__, dt.datetime.now()))

# testing
if __name__ == '__main__':
    main(True)
