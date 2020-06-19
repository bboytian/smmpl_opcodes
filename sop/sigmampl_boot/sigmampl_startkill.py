'''
Functions to start and kill SigmaMPL program
'''
# imports
import datetime as dt
import os
import os.path as osp
import subprocess as sub
import time

from ...params import *

# start func
def sigmampl_start(delay=0):
    print('start {}@{:%Y%m%d%H%M}...'.format('SigmaMPL',dt.datetime.now()))
    # if delay > 0:
    #     print('delay start up by {}s'.format(delay))
    # time.sleep(delay)        
    # sub.Popen([MPLSIGMAPROGDIR, 'auto'], cwd=MPLSIGMADIR)
    
# kill func
def sigmampl_kill():
    print('kill {}@{:%Y%m%d%H%M}...'.format('SigmaMPL', dt.datetime.now()))
    # os.system('taskkill /f /t /im {}'.format(MPLSIGMAPROG))
    #
    # create data flag
    # now = dt.datetime.now()
    # with open(osp.join(MPLDATADIR, MPLFLAGFILE.format()))



if __name__ == '__main__':
    sigmampl_start()
    time.sleep(35)
    sigmampl_kill()
