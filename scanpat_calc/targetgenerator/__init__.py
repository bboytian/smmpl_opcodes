# imports
import copy as cp
import datetime as dt
import time

from .plotshapes import plotshapes


# class
class targetgenerator:

    def __init__(
            self,
            timeobj, sunforecaster, pathplanner,
            queue=None,
    ):
        '''
        Parameters
            timeobj: defined in root folder
            sunforecaster: defined in root folder
            pathplanner: defined in root folder

            queue (multiprocessing.Queue): for sotring data for visualisation
        '''
        # Attributes
        self.to = timeobj
        self.pp = pathplanner
        self.ps = plotshapes(
            timeobj,
            sunforecaster,
            pathplanner
        )

        self.queue = queue
        self.scanpat_aralst = []

        # storing init value
        self.store()

        # iterating through timeobjseg
        while True:

            # time keeping
            print('seg: {}/{}, starttime {}, endtime: {}'.format(
                *self.to.get_tosegpos(),
                self.to.get_tosegst(),
                self.to.get_toseget()
            ))

            # iterate timeobjseg
            tosegstop_boo = self.to.next_toseg()
            if tosegstop_boo:
                break

            self.update()
            self.store()


    def update(self):

        self.ps.gen()


    def store(self):
        # storing data in queue or to variable
        if self.queue:
            self.queue.put(cp.deepcopy(self.ps))
        else:
            self.scanpat_aralst.append(
                self.pp.get_scanpat(self.ps.targ_aimpath.dir_aralst)
            )


    def get_scanpataralst(self):
        return self.scanpat_aralst
