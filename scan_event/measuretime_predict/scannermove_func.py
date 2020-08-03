# imports
import numpy as np

from ...globalimports import *


# main func
def main(dir_a, thetaspeed, phispeed):
    '''
    returns the timestamp of each point w.r.t first point in units of seconds
    Assumes that the scanner starts at the first point, just finished measurement
    '''
    deldir_a = dir_a[1:] - dir_a[:-1]
    deldir_a[deldir_a<0] = deldir_a[deldir_a<0] * -1

    ret_l = [0]
    for deldir in deldir_a:
        ret_l.append(
            thetaspeed*deldir[1] + phispeed*deldir[0]
            + AVERAGINGTIME
        )

    return ret_l



# testing
if __name__ == '__main__':
    main()
