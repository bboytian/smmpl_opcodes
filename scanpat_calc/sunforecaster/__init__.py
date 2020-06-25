import numpy as np

from ...globalimports import *


if SFAPI == 'pysolar_API':
    from .pysolar_API import func as get_angles
elif SFAPI == 'pysolarfast_API':
    from .pysolarfast_API import func as get_angles
elif SFAPI == 'sunposcalc_API':
    from .sunposcalc_API import func as get_angles


class sunforecaster:

    def __init__(
            self,
            lt, lg,
            ele=0
    ):
        '''
        Parameters
            lt (float): latitude [deg]
            lg (float): longitude [deg]
            ele (float): elevation [m]
        '''
        self.lt, self.lg = lt, lg
        self.ele = ele

        
    def get_angles(self, timestamp):
        '''
        Return
            thetas, phis (float): [rad]
        '''
        return get_angles(
            timestamp,
            self.lt, self.lg,
            self.ele
        )

    def get_anglesvec(self, timestamp_ara):
        '''
        Return
             (thetas_ara, phis_ara)
        '''
        return np.vectorize(self.get_angles)(timestamp_ara)
