# imports
import datetime as dt

from .sigmampl_startkill import sigmampl_start, sigmampl_kill
from .scan_init import main as scan_init
from .prepostmea_fileman import premea_fileman, postmea_fileman

from ...global_imports.smmpl_opcodes import *

# main func
@verbose
@announcer(newlineboo=True)
@logger
def main(coldstart_boo=False, scanpat_dir=None):
    '''
    Parameters
        coldstart_boo (boolean): determines whether measurement is testing for
                                 the first time, or testing operationally
        scanpat_dir (str): if provided, initialises using this scanpattern file
    '''
    sigmampl_kill()  # always run to kill any exisiting windows
    if not coldstart_boo:
        postmea_fileman()
    premea_fileman(coldstart_boo)
    scan_init(init_boo=True, scanpat_dir=scanpat_dir)
    sigmampl_start()


# testing
if __name__ == '__main__':
    today = dt.datetime.combine(dt.date.today(), dt.time())
    main(
        True,
        stdoutlog=DIRCONFN(
            MPLDATADIR, DATEFMT.format(today), SIGMAMPLBOOTLOG.format(today)
        ),
        dailylogboo=True
    )
