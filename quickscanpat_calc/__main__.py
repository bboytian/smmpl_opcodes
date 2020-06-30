# imports
from .suncone import main as suncone
from ..globalimports import *


# params

_qspatfunc_d = {
    'suncone':suncone
}


# main func
@announcer(newlineboo)
def main(qstype):
    '''
    Calls the appropriate quick scan function to be called.
    The arguments for the functions are adjusted in their respective scripts
    Scan patterns are written to directory specified in ..params, usually this
    directory

    Parameters
        qstype (str): type of scan quick scan pattern
    
    Return
        scanpat_a (np.array): array produced by quick scan pattern calculation
    '''
    scanpat_a = _qspatfunc_d[qstype]()
    return scanpat_a


# testing
if __name__ == '__main__':
    main()
