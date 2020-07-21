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

from ...globalimports import *


# main func
@announcer
def premea_fileman(coldstart_boo):
    '''
    For now, coldstart_boo=False does nothing. This is left as a filler in the
    event we need to configure something.

    if coldstart_boo, the system will check for any existing logfiles and
    mplfiles. If there are, the user can choose whether to delete the files.
    If the files are not deleted, the function will raise an exception to halt
    the program, for the user to move the files manually.
    Note that this requires an input which multiprocessing cannot handle, thus
    the function has to be called on the main thread

    Parameters
        coldstart_boo (boolean): Running procedure if program is starting for the
                                 first time
    '''
    if coldstart_boo:           # when first running operational measurements

        # finding any existing files
        mpllogfile_lst = list(filter(
            lambda x: MPLLOGFILE[MPLLOGTIMEIND:] in x or
            MPLLOGCURFILE in x,
            os.listdir(MPLSIGMALOGDIR)
        ))
        mpllogfile_lst = [DIRCONFN(MPLSIGMALOGDIR, mlf) for mlf in mpllogfile_lst]

        mplfile_lst = list(filter(
            lambda x: MPLFILE[MPLTIMEIND:] in x,
            os.listdir(MPLSIGMADATADIR)
        ))
        mplfile_lst = [DIRCONFN(MPLSIGMADATADIR, mf) for mf in mplfile_lst]

        # asking user
        if mpllogfile_lst or mplfile_lst:
            GETRESPONSEFN(
                f'There are {len(mpllogfile_lst)} mpllog files and'
                f' {len(mplfile_lst)} mpl files, shall we delete them?',
                True, True
            )

    else:            # when code has already been running operationaly
        pass


@announcer
def postmea_fileman():
    '''
    creates a flag file to show where the end of measurement data is

    Also moves the current logfile to create room for a new one
    '''
    now = dt.datetime.now()

    # creating end of measurement flag
    eomflag_file = DIRCONFN(
        MPLDATADIR, DATEFMT.format(now), MPLEOMFILE.format(now)
    )
    print(f'create end of measurement flag {eomflag_file}')
    with open(eomflag_file, 'w') as flag:
        pass

    # moving current log file
    loglatestfiledir = DIRCONFN(MPLSIGMALOGDIR, MPLLOGCURFILE)
    newloglatestfiledir = DIRCONFN(MPLDATADIR, DATEFMT.format(now),
                                   MPLLOGFILE.format(now))
    print('move current log file {} -> {}'.
          format(loglatestfiledir, newloglatestfiledir))
    shutil.move(loglatestfiledir, newloglatestfiledir)



# running
if __name__ == '__main__':
    pass
