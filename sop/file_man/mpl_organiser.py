# imports
import datetime as dt
import os
import os.path as osp
import shutil

from ...globalimports import *


# main function
@announcer
def main(tailend_boo):
    '''
    organises the following files:
    - useful MPLLog.txt file from sigma/Log; excluding the one that is
                                             currently being written on
    - .mpl files from sigma/DATA

    shutil.copy is assumed to not interrupt with sigmaMPL writing to the .mpl
    file

    current log file being written to is not copied over, unless we are on the
    tailend. Duing which it is moved, and renamed from MPLLOGCURFILE ->
    MPLLOGFILE

    this means that scan_vis with scan_event live update cannot be run via
    SOLARIS server, but has to be run on the local computer

    Parameters
        tailend_boo (boolean): decides whether or not to move the latest mpl file
                               should be True when wrapping up operations
    '''
    # getting file lst(absolute path), and date lst
    mplfile_lst = list(filter(
        lambda x:MPLFILE[MPLTIMEIND:] in x,
        os.listdir(MPLSIGMADATADIR)
    ))
    mplfile_lst.sort()
    try:
        mpllatestfile = mplfile_lst.pop()  # to be copied safely
    except IndexError:
        mpllatestfile = None
    mpldate_lst = [mf[:MPLDATEIND] for mf in mplfile_lst]

    mpllogfile_lst = list(filter(
        lambda x: MPLLOGFILE[MPLLOGTIMEIND:] in x,
        os.listdir(MPLSIGMALOGDIR)
    ))
    mpllogdate_lst = [mlf[:MPLLOGDATEIND] for mlf in mpllogfile_lst]

    filename_lst = mplfile_lst + mpllogfile_lst
    filedir_lst = [DIRCONFN(MPLSIGMADATADIR, mf) for mf in mplfile_lst]\
        + [DIRCONFN(MPLSIGMALOGDIR, mlf) for mlf in mpllogfile_lst]
    date_lst = mpldate_lst + mpllogdate_lst

    # making non existent directories; required for shutil move
    d_lst = list(set(date_lst))
    for date in d_lst:
        datadate_dir = DIRCONFN(MPLDATADIR, date)
        if not osp.exists(datadate_dir):
            os.mkdir(datadate_dir)

    # moving files; preserving nomenclature
    for i, filedir in enumerate(filedir_lst):
        newfiledir = DIRCONFN(MPLDATADIR, date_lst[i], filename_lst[i])
        print('moving {} -> {}'.format(filedir, newfiledir))
        shutil.move(filedir, newfiledir)

    # copying the latest .mpl file in case software is still writing
    if mpllatestfile:
        mpllatestfiledir = DIRCONFN(MPLSIGMADATADIR, mpllatestfile)
        newmpllatestfiledir = DIRCONFN(MPLDATADIR, mpllatestfile[:MPLDATEIND],
                                       mpllatestfile)
    loglatesttime = dt.datetime.now()
    loglatestfiledir = DIRCONFN(MPLSIGMALOGDIR, MPLLOGCURFILE)
    newloglatestfiledir = DIRCONFN(MPLDATADIR, DATEFMT.format(loglatesttime),
                                   MPLLOGFILE.format(loglatesttime))

    if tailend_boo:
        if mpllatestfile:
            print('move current .mpl file {} -> {}'.
                  format(mpllatestfiledir, newmpllatestfiledir))
            shutil.move(mpllatestfiledir, newmpllatestfiledir)

        print('move current log file {} -> {}'.
              format(loglatestfiledir, newloglatestfiledir))
        shutil.move(loglatestfiledir, newloglatestfiledir)

    else:
        if mpllatestfile:
            print('copying current .mpl file {} -> {}'
                  .format(mpllatestfiledir, newmpllatestfiledir))
            shutil.copy(mpllatestfiledir, newmpllatestfiledir)


# testing
if __name__ == '__main__':
    main(False)
