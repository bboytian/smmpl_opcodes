'''
Functions to start and kill SigmaMPL program
'''
# imports
import datetime as dt
import os
import subprocess as sub
import time

from ...global_imports.smmpl_opcodes import *


# params
_starttimeout = 1              # [s]



# start func
@announcer
def sigmampl_start(delay=0):
    if delay > 0:
        print('delay start up by {}s'.format(delay))
    time.sleep(delay)
    sigmampl_sub = sub.Popen([MPLSIGMAPROGDIR, 'auto'], cwd=MPLSIGMADIR,
                             stdout=sub.PIPE, stderr=sub.STDOUT)
    try:
        print(sigmampl_sub.communicate(timeout=_starttimeout)[0])
    except sub.TimeoutExpired:  # no error messages from startup, returns control
                                # to main function
        pass


# kill func
@announcer
def sigmampl_kill():
    sigmampl_sub = sub.Popen(['taskkill', '/f', '/t', '/im', f'{MPLSIGMAPROG}'],
                             stdout=sub.PIPE, stderr=sub.STDOUT)
    print(sigmampl_sub.communicate()[0])



# testing
if __name__ == '__main__':
    sigmampl_start()
    time.sleep(5)
    sigmampl_kill()
