# imports
from glob import glob
import os.path as osp

from ..file_readwrite import smmpl_reader
from ..global_imports.smmpl_opcodes import *


# main func
@verbose
@announcer(newlineboo=True)
def main():
    '''
    Reads the files from the data directory and SigmaMPL/DATA, from LASTDAYSNUM
    days ago
    There should only be one common file between the two directories; the current
    file.
    For all common files, it will always choose the one in SigmaMPL

    Return
        mpl_d (dict): containing latest mpl profile data if the file is found
                      if files are not found, it does not return anything
    '''
    # gather latest files from datadir and SigmaMPL folder
    date_l = glob(DIRCONFN(MPLDATADIR, '2*'))
    date_l.sort()
    date_l = date_l[-(LASTDAYSNUM+DAYSINADV):]

    mpl_l = FINDFILESFN(MPLFILE, date_l)
    sigmampl_l = FINDFILESFN(MPLFILE, MPLSIGMADATADIR)

    # choose the sigmampl_l common files
    mpl_l = [
        mpl for mpl in mpl_l
        if DIRCONFN(MPLSIGMADATADIR, osp.basename(mpl)) not in sigmampl_l
    ]
    mpl_l += sigmampl_l
    mpl_l = mpl_l[::-1]

    # reading file
    for mpl in mpl_l:
        # catching empty files
        mpl_d = smmpl_reader(
            mplfiledir=mpl,
            verbboo=True
        )
        if mpl_d:
            return mpl_d
    return mpl_l, sigmampl_l


# testing
if __name__ == '__main__':
    check_l = [
        'Shots Sum',
        'Trigger Frequency',        # for performance check
        'Energy Monitor',           # [nJ]
        'Temp #0',                  # Detector Temperature
        'Temp #1',                  # unknown
        'Temp #2',                  # Telescope Temperature
        'Temp #3',                  # Laser temperature
        'Temp #4',                  # unknown
        'Background Average',
        'Background Average 2',
        'A/D Data Bad flag',        # for performance check, 0 is good, 1 is bad
        'Sync Pulses Seen Per Second',
    ]
    mpl_d = main()
    for check in check_l:
        print(check, mpl_d[check])
