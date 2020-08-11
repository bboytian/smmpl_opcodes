# imports
import os
import os.path as osp

import numpy as np

from ..file_readwrite.mpl_reader import smmpl_reader
from ...global_imports import *

# params
_tempfilename = 'tempdatafile'


# main func
def main():
    '''
    Reads the files from the data directory and SigmaMPL/DATA, from the last
    eom.flag onwards.
    There should only be one common file between the two directories; the current
    file.
    For all common files, it will always choose the one in SigmaMPL

    It searches the last LASTDAYSNUM dates for the appropriate _eom.flag, and finds
    the appropriate data
    '''
    # gather latest files from datadir and SigmaMPL folder
    date_l = np.array(list(filter(
        lambda x: x[0] == '2', os.listdir(MPLDATADIR)
    )))
    date_l.sort()
    date_l = date_l[-LASTDAYSNUM:]
    eom_l = FINDFILESFN(MPLEOMFILE, date_l)
    eom_l = LOCTIMEFN(DIRPARSEFN(eom_l, MPLEOMTIMEFIELD), UTCINFO)  # time array

    mpl_l = FINDFILESFN(MPLFILE, date_l)
    mpl_l.sort()
    sigmampl_l = FINDFILESFN(MPLFILE, MPLSIGMADATADIR)
    sigmampl_l.sort()

    ## choose the sigmampl_l common files
    mpl_l = [
        mpl for mpl in mpl_l
        if DIRCONFN(MPLSIGMADATADIR, osp.basename(mpl)) not in sigmampl_l
    ]
    mpl_l += sigmampl_l

    # read files and create a temp file to pass to file_readwrite
    tmpfile_dir = DIRCONFN(osp.abspath(__file__), _tempfilename)
    with open(tmpfile_dir, 'b')
    '''choose the right mode here'''


    # return



# testing
if __name__ == '__main__':
    main()
