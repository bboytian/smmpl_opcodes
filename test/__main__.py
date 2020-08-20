# imports
import time
import re
import signal
import multiprocessing as mp

from .test1 import main as test1

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
        except IndexError:
            pass


# relv func
def namefromframe(frame):
    lst = re.split('\W', str(frame))
    lst = [x for x in lst if x]
    framename = lst[-1]
    return framename


def handler(signum, frame):
    parframename = namefromframe(frame.f_back)
    if parframename == 'module':
        raise IndexError
    elif parframename == 'run':
        raise IndexError
    else:
        print(f'error: {parframename}')
        print(namefromframe(frame))


# main func
def main():
    try:
        # mp.Process(target=test1).start()
        _procwrapper(target=test1).start()

        time.sleep(5)
    except IndexError:
        print('interrupt detected')


# testing
if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    main()
