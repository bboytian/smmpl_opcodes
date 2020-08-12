# imports
import datetime as dt
from glob import glob
import os
import os.path as osp

import numpy as np

from ...file_readwrite.mpl_reader import smmpl_reader
from ...global_imports.smmpl_opcodes import *

# params
_tempfilename = 'tempdatafile'


# main func
@verbose
@announcer(newlineboo=True)
def main():
    '''
    Reads the files from the data directory and SigmaMPL/DATA, from the last
    eom.flag onwards.
    There should only be one common file between the two directories; the current
    file.
    For all common files, it will always choose the one in SigmaMPL

    It searches the last LASTDAYSNUM dates for the appropriate _eom.flag, and finds
    the appropriate data

    Return
        mpl_d (dict): containing latest mpl profile data if the file is found
                      if files are not found, it does not return anything
    '''
    # gather latest files from datadir and SigmaMPL folder
    date_l = glob(DIRCONFN(MPLDATADIR, '2*'))
    date_l.sort()
    date_l = date_l[-LASTDAYSNUM:]
    eom_l = FINDFILESFN(MPLEOMFILE, date_l)
    eomtime_a = LOCTIMEFN(DIRPARSEFN(eom_l, MPLEOMTIMEFIELD), UTCINFO)  # time array

    mpl_l = FINDFILESFN(MPLFILE, date_l)
    sigmampl_l = FINDFILESFN(MPLFILE, MPLSIGMADATADIR)

    ## choose the sigmampl_l common files
    mpl_l = [
        mpl for mpl in mpl_l
        if DIRCONFN(MPLSIGMADATADIR, osp.basename(mpl)) not in sigmampl_l
    ]
    mpl_l += sigmampl_l

    ## finding the right scan pattern to read
    mplsize_a = np.array(list(map(osp.getsize, mpl_l)))
    mpltime_a = LOCTIMEFN(DIRPARSEFN(mpl_l, MPLTIMEFIELD), UTCINFO)  # time array
    eomtime_a = np.append(eomtime_a, LOCTIMEFN(dt.datetime.now(), UTCINFO))
    for i in range(-1, -len(eomtime_a)+1, -1):
        seomtime = eomtime_a[i-1]
        eeomtime = eomtime_a[i]
        timeboo_a = (mpltime_a >= seomtime) * (mpltime_a < eeomtime)
        mplspsize = np.sum(mplsize_a[timeboo_a])
        if not mplspsize:
            continue
        else:
            read_a = np.array(mpl_l)[timeboo_a]
            break

    # read files and create a temp file to pass to file_readwrite
    filefound_boo = True
    tmpfile_dir = DIRCONFN(osp.dirname(osp.abspath(__file__)), _tempfilename)
    with open(tmpfile_dir, 'wb') as tmp_file:
        try:
            print('reading latest files from:')
            for read in read_a:
                print(f'\t{read}')
                with open(read, 'rb') as read_file:
                    tmp_file.write(read_file.read())
        except NameError:
            print('latest files not found')
            filefound_boo = False

    # deleting temp file
    try:
        os.remove(tmpfile_dir)
    except FileNotFoundError:
        pass

    # return
    if filefound_boo:
        mpl_d = smmpl_reader(
            LIDARNAME, mplfiledir=tmpfile_dir,
            slicetup=slice(-1, None, None),
            verbboo=False
        )
        return mpl_d

# testing
if __name__ == '__main__':
    pass
