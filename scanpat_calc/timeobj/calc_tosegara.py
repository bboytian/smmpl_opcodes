# imports
import numpy as np
import pandas as pd

from .timeobjseg import timeobjseg as toseg


# function
def calc_tosegara(self):
    '''
    creates an array of timeobjs, which are segments for the sun swath
    current implementation divides timeobj into equal segments
    '''
    segnum = int(self.Deltatime / self.segdelta)
    if segnum == 0:
        self.toseg_ara = [self]
    else:
        self.toseg_ara = range(segnum)
        self.toseg_ara = np.array(list(map(
            lambda x: toseg(
                self.starttime + x*self.segdelta,
                self.starttime + (x+1)*self.segdelta,
                self.finedeltatime,
                self.deltatime
            ),
            self.toseg_ara
        )))

        # if the last entry is a partial segment
        if (self.Deltatime % self.segdelta)/self.segdelta != 0:
            # editing the last entry so that it does not surpass endtime
            starttime = self.starttime + (segnum)*self.segdelta
            self.toseg_ara = np.append(self.toseg_ara, toseg(
                starttime,
                self.endtime,
                self.finedeltatime,
                self.deltatime
            ))
