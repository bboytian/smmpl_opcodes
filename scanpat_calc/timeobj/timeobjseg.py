# imports
import pandas as pd


# child class
class timeobjseg:

    def __init__(
            self,
            starttime,
            endtime,
            finedeltatime,
            deltatime
    ):
        # Attributes
        self.starttime = starttime
        self.endtime = endtime
        self.Deltatime = endtime - starttime

        self.deltatime = deltatime
        self.finedeltatime = finedeltatime


    # methods for timestamps within time segments
    def get_timeara(self, fine_boo):
        '''
        Parameters
            fine_boo (boolean): if True, produces a time ara with pre-determined
                                time delta; which gives a smooth suncone swath
        Return
            array of pd.Timestamps
        '''
        if fine_boo:            # used for sun swath
            frames = int(self.Deltatime / self.finedeltatime)
            if frames <= 1:
                err_str = '''
                finedeltatime >= starttime - endtime
                sunswath computed not representative of sun's path
                '''
                raise ValueError(err_str)
        else:                   # used for animation
            frames = self.frames

        time_ara = pd.date_range(self.starttime, self.endtime, periods=frames)
        return time_ara

    def next_ts(self, timeobj):
        timeobj.ts += self.deltatime

        # handling end of timeobjseg
        if timeobj.ts < self.endtime:
            return False
        else:                   # end of iteration reached
            return True         # boolean to move to next timeobjseg
