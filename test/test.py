# imports
import multiprocessing as mp
import time

from .global_imports.smmpl_opcodes import *

# params



# decorator
def exceptioncatch(func):
    def wrapper_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print('hmm')
    return wrapper_func


# relv func
# @exceptioncatch
def _sub_f(msg):
    counter = 0
    while True:
        if counter > 5:
            break
        print(msg, counter)
        counter += 1
        time.sleep(1)

class _procwrapper(mp.Process):
    '''
    To be used in a way similar to multiprocessing.Process.
    It logs the print statements in the specified logfiles
    '''
    def __init__(self, target, args=(), kwargs={}):
        super().__init__(target=target, args=args, kwargs=kwargs)

    def run(self):
        '''
        This runs on self.start() in a new process
        '''
        if self._target:
            self._target(*self._args, **self._kwargs)


import signal

# main func
def main():
    try:
        signal.signal(signal.SIGINT, handler)
        a = _procwrapper(target=_sub_f, args=('hi',))
        a.start()
        time.sleep(10)

    except KeyboardInterrupt:
        print('main thread detected interrupt')
        print('waiting for processes to end')
        a.join()


def handler(a, b):  # define the handler
    # print("Signal Number:", a, " Frame: ", b)
    # print(dir(b))
    parframestr = b.f_back.__str__()
    parframestr = DIRPARSEFN(parframestr)
    parframestr = [x for x in parframestr if x][-1]
    if parframestr == 'run':
        pass
    elif parframestr == 'module':
        raise KeyboardInterrupt

# testing
if __name__ == '__main__':
    main()
