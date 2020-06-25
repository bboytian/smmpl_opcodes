# imports
from .suncone import main as suncone
from ..globalimports import *


# params

_qspatfunc_d = {
    'suncone':suncone
}

_qspatargs_d = {
    'suncone':[]
}


# main func
def main(qstype=QUICKSCANTYPE):
    '''
    Calls the appropriate quick scan function to be called.
    The arguments for the functions should be adjusted here.
    Scan patterns are written to directory specified in ..params, usually this
    directory

    Parameters for all the different quick scan functions are to be handled here

    Parameters
        qstype (str): type of scan quick scan pattern
    
    Return
        scanpat_dir (str): Directory of scanpat file
    '''

    scanpat_dir = _qspatfunc_d[qstype](*_qspatargs_d[qstype])

    return scanpat_dir


# testing
if __name__ == '__main__':
    main()
