# imports
import numpy as np

from ..global_imports.smmpl_opcodes import *

# params
_sphil = -56.71
_ephil = -47.98
_philspacing = 0.03
_elevation = 0

# main func
@announcer(newlineboo=False)
@logger
def main():
    '''
    Calculates a scan pattern setting a constant elevation

    Return
        dir_a (str): [deg] array containing direction for scan targets
                     shape: (M:=_npoints*len(offset_a), 2(phil, thetal))
    '''
    phil_a = np.arange(_sphil, _ephil, _philspacing)
    elevation_a = _elevation * np.ones_like(phil_a)
    dir_a = np.stack([phil_a, elevation_a], axis=1)

    return dir_a


# testing
if __name__ == '__main__':
    dir_a = main()
    print(dir_a)
