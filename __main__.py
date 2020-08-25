# imports
import multiprocessing as mp
import time

from .quickscan_main import main as quickscan_main
from .scan_event import main as scan_event
from .skyscan_main import main as skyscan_main
from .sop import file_man

from .global_imports.smmpl_opcodes import *


# class wrapper
class _procwrapper(mp.Process):
    '''
    To be used in a way similar to multiprocessing.Process.
    It delays the running of the process
    '''
    def __init__(self, target, waittime, args=(), kwargs={}):
        print(
            (TIMEFMT + ' run {}.{}...'.
            format(dt.datetime.now(), target.__module__, target.__name__)
        )
        super().__init__(target=target, args=args, kwargs=kwargs)
        self.waittime = waittime

    def run(self):
        '''
        This runs on self.start() in a new process
        '''
        time.sleep(self.waittime)
        if self._target:
            self._target(*self._args, **self._kwargs)


# main func
def main(measurementprotocol):
    '''
    Parameters
        normalopsboo: True  -> run skyscan_main
                      False -> run quickscan_main
    '''

    # live data events monitoring
    mp.Process(
        target=scan_event, waittime=FIRSTMEASURETIME,
    ).start()

    # data organisation and sync
    mp.Process(
        target=file_man, waittime=FIRSTMEASURETIME,
    ).start()

    # measurement protocol
    if measurementprotocol == SKYSCANPROTOCOL:
        skyscan_main()
    if measurementprotocol == QUICKSCANPROTOCOL:
        quickscan_main()


# running
if __name__ == '__main__':
    main(MEASUREMENTPROTOCOL)
