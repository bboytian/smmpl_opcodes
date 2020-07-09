# imports
import datetime as dt

from .sigmampl_startkill import sigmampl_start, sigmampl_kill
from .scan_init import main as scan_init
from .prepostmea_fileman import premea_fileman, postmea_fileman

from ...globalimports import *

# main func
@announcer(newlineboo=True)
def main(coldstart_boo=False, tailend_boo=False):
    '''
    Parameters
        coldstart_boo (boolean): determines whether measurement is testing for
                                 the first time, or testing operationally
        tailend_boo (boolean): decides whether or not to move the latest mpl file
                               should be True when wrapping up operations
    '''
    sigmampl_kill()  # always run to kill any exisiting windows
    if not coldstart_boo:
        postmea_fileman()
    premea_fileman(coldstart_boo)
    if not tailend_boo:
        scan_init(init_boo=True)
        sigmampl_start()


# testing
if __name__ == '__main__':
    main(True)
