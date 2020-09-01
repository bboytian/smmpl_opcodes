'''
Only run this script before measurement (NOT DURING), it does the following:

-
- Delete previous logfile, which could be due to program opening and closing or usage of program
'''
# imports
import datetime as dt
import os
import shutil
import sys

from ...global_imports.smmpl_opcodes import *


# main func
@announcer
def premea_fileman(coldstart_boo):
    '''
    This is left as a filler in the event we need to configure something before
    every measurement

    Parameters
        coldstart_boo (boolean): Running procedure if program is starting for the
                                 first time
    '''
    pass


@announcer
def postmea_fileman():
    '''
    moves the current logfile to create room for a new one
    '''
    now = dt.datetime.now()

    # moving current log file
    loglatestfiledir = DIRCONFN(MPLSIGMALOGDIR, MPLLOGCURFILE)
    newloglatestfiledir = DIRCONFN(MPLDATADIR, DATEFMT.format(now),
                                   MPLLOGFILE.format(now))
    print('move current log file {} -> {}'.
          format(loglatestfiledir, newloglatestfiledir))
    shutil.move(loglatestfiledir, newloglatestfiledir)



# testing
if __name__ == '__main__':
    premea_fileman(True)
