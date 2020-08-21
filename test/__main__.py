# imports
import time
import re
import signal
import multiprocessing as mp

from .exceptions import *
from .test1 import main as test1
from .test2 import main as test2


# relevant class
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
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except ProcError:
            print('processes killed')


# relv func
def namefromframe(frame):
    lst = re.split('\W', str(frame))
    lst = [x for x in lst if x]
    framename = lst[-1]
    return framename


def handler(signum, frame):
    # print(namefromframe(frame), namefromframe(frame.f_back))
    parframename = namefromframe(frame.f_back)
    print(parframename)
    if parframename == 'module':
        raise MainError
    elif parframename == 'main':
        raise FuncError
    # elif parframename == 'run':
    #     # raise ProcError
    #     pass
    # else:
    #     print(f'error: {parframename}')
    #     print(namefromframe(frame))

# main func
def main():
    try:
        # _procwrapper(target=test1).start()
        test2()

        time.sleep(5)
    except MainError:
        print('interrupt detected')



# testing
if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    main()
