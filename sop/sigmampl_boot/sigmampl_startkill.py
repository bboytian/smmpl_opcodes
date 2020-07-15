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
    print(sigmampl_sub.stdout.read().decode('utf-8'))

# kill func
@announcer
def sigmampl_kill():
    sigmampl_sub = sub.Popen([f'taskkill /f /t /im {MPLSIGMAPROG}'],
                             stdout=sub.PIPE, stderr=sub.STDOUT)
    # print(sigmampl_sub.stdout.decode('utf-8'))
    print(sigmampl_sub.stdout.read().decode('utf-8'))



# testing
if __name__ == '__main__':
    # sigmampl_start()
    # time.sleep(35)
    sigmampl_kill()
