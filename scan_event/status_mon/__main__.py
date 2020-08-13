# imports
import time
import datetime as dt
import os
import os.path as osp

from ...global_imports.smmpl_opcodes import *


# main func
def main(mpld):
    '''
    In the future, each individual status check could be made into it's own script

    Parameters
        mpld (dict): dictionary of mpldata containing the most current profile
    Return
        msg (str): messages to be sent
    '''
    msg = ''

    # temperature check
    temp0 = mpl_d['Temp #0'][-1]
    if temp0 >= TEMPZEROTHRES:
        pass

    # bad flag check

    # no new file check


# running
if __name__ == '__main__':
    main()
