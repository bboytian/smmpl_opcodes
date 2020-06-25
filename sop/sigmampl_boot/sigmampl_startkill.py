'''
Functions to start and kill SigmaMPL program
'''
# imports
import datetime as dt
import os
import os.path as osp
import subprocess as sub
import time

from ...globalimports import *


# start func
@announcer
def sigmampl_start(delay=0):
    pass
    # if delay > 0:
    #     print('delay start up by {}s'.format(delay))
    # time.sleep(delay)
    # sub.Popen([MPLSIGMAPROGDIR, 'auto'], cwd=MPLSIGMADIR)

# kill func
@announcer
def sigmampl_kill():
    pass
    # os.system('taskkill /f /t /im {}'.format(MPLSIGMAPROG))
    #
    # create data flag
    # now = dt.datetime.now()
    # with open(dc_gfunc(MPLDATADIR, MPLFLAGFILE.format()))


# testing
if __name__ == '__main__':
    sigmampl_start()
    time.sleep(35)
    sigmampl_kill()
