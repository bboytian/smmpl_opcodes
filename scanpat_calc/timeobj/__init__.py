# imports
import datetime as dt

import numpy as np
import pandas as pd

from ...globalimports import *


# main class
class timeobj:

    def __init__(
            self,
            starttime, endtime,
            utcinfo, finedeltatime,
            segdelta,
            fps=2,
            equivtime=None,
    ):
        '''
        generates timeobjseg based on given boundaries, each timeobjseg is used
        for a single sunswath

        timestamps are saved in this class only, not timeobjseg

        timestamp is init to the first timestamp of the next timeobjseg each time
        we iterate to the next timeobj

        Future
            - changing calc_tosegara into a generator will prevent us from
              storing the values
            - having intelligent segmentation of time

        Parmaters
            starttime (pd.Timestamp): start time of visualisation
            endtime (pd.Timestamp): endtime of visualisation
            utcinfo (int): UTCINFO, +8 by default
            finedeltatime (timedelta like): discretisation of sunswath sunswath
                                            consists of cone intersections
            segdelta (pandas.Timedelta): determines time interval for sunswath
            fps (float): frames per second of animation
            equivtime (datetime like): equivalent show time of the visualisation
                                       ; assuming that fps is set appropriately
                                       ; if None, we are not in realtime

        Attributes
            realtime_boo (boolean): for visualiser to know when to wait
            ts (pd.Timestamp): timestamp
            toseg (timeobj.timeobjseg)
            toseg_ara (np.array obj): array of toseg
            toseg_araind (int): index of current toseg in toseg_ara
        '''
        # attributes for time stamps
        self.utcinfo = utcinfo
        self.starttime = LOCTIMEFN(starttime, UTCINFO)
        self.endtime = LOCTIMEFN(endtime, UTCINFO)
        self.Deltatime = self.endtime - self.starttime

        # accomodation for realtime visualisation
        if equivtime:
            self.realtime_boo = False
            self.equivtime = equivtime
        else:
            self.realtime_boo = True
            self.equivtime = self.endtime - self.starttime

        # attributes for time segment calculation
        self.segdelta = segdelta
        self.toseg_ara = None   # can be removed if changed to generator

        # attributes for timeobjseg
        self.finedeltatime = finedeltatime
        self.fps = fps


        # init
        self.ts = self.starttime
        self.calc_tosegara()
        self.toseg_araind = 0
        self.toseg = self.toseg_ara[self.toseg_araind]


    # methods for timestamps
    def next_ts(self):
        nexttoseg_boo = self.toseg.next_ts(self)
        return nexttoseg_boo

    def get_ts(self):
        return self.ts

    def get_timeara(self, fine_boo=False):
        '''
        Parameters
            fine_boo (boolean): if True, produces a time ara with pre-determined
                                time delta; which gives a smooth suncone swath
        Return
            array of pd.Timestamps
        '''
        return self.toseg.get_timeara(fine_boo)


    # methods for time segments

    from .calc_tosegara import calc_tosegara

    def get_tosegpos(self):
        return self.toseg_araind, len(self.toseg_ara)-1

    def next_toseg(self):
        self.toseg_araind += 1

        # handling end of calculation
        if self.toseg_araind < len(self.toseg_ara):
            self.toseg = self.toseg_ara[self.toseg_araind]
            self.ts = self.toseg.starttime  # changing timestamp to be the newest
            return False
        else:                   # end of iteration reached
            return True         # boolean to tell calculation to stop


    # etc methods

    def get_utcinfo(self):
        return self.utcinfo

    def get_realtimeboo(self):
        return self.realtime_boo

    def get_tosegst(self, *toseg_ara):
        if toseg_ara:
            return toseg_ara[0].starttime
        else:
            return self.toseg.starttime
    def get_toseget(self, *toseg_ara):
        if toseg_ara:
            return toseg_ara[0].endtime
        else:
            return self.toseg.endtime

    def get_tosegara(self):
        return self.toseg_ara
