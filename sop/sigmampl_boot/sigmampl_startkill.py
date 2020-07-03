'''
Functions to start and kill SigmaMPL program
'''
# imports
import datetime as dt
import os
import subprocess as sub
import time

from ...globalimports import *


# start func
@announcer
def sigmampl_start(delay=0):
    if delay > 0:
        print('delay start up by {}s'.format(delay))
    time.sleep(delay)
    sigmampl_sub = sub.Popen([MPLSIGMAPROGDIR, 'auto'], cwd=MPLSIGMADIR,
                             stdout=sub.PIPE, stderr=sub.STDOUT)
    print(sigmampl_sub.stdout.decode('utf-8'))

# kill func
@announcer
def sigmampl_kill(logfile):
    # writing output to logfile
    os.system('taskkill /f /t /im {} > {} 2>&1'.format(MPLSIGMAPROG, logfile))


# testing
if __name__ == '__main__':
    sigmampl_start()
    time.sleep(35)
    sigmampl_kill()
