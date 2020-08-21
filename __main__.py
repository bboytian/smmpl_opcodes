# imports
import multiprocessing as mp
import signal
import sys

from . import exceptions
from .global_imports.smmpl_opcodes import *
from .quickscan_main import main as quickscan_main
from .scan_event import main as scan_event
from .skyscan_main import main as skyscan_main



# Process class
class _procwrapper(mp.Process):
    '''
    To be used in a way similar to multiprocessing.Process.
    terminates process base on specified exceptions
    '''
    def __init__(self, exception_t, target, args=(), kwargs={}):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self.exception_t = exception_t

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except self.exception_t as e:
            self.terminate()


# handles signals
def _handler_f(signalnum, frame):
    '''called when signal.signal interrupt is sent'''
    framename, framefile = FRAMEPARSEFN(frame)
    parframename, parframefile = FRAMEPARSEFN(frame.f_back)  # parent frame

    # main thread func
    if framename == 'main' and parframename == 'module':
        # graceful closure are handled by the measurement protocols
        pass

    # functions within main thread func
    elif framename == 'main' and parframename == 'main':
        raise exceptions.MeasurementInterrupt

    # processes started in main thread func
    elif parframefile == 'run' and DIRPARSEFN(parframefile, -2) == 'scan_event':
        raise exceptions.ScaneventInterrupt

    # for consecutive interrupts
    elif framename == 'poll' and parframename == 'wait':
        haltlogging(lambda: print('graceful program closure in progress...'))()

    # for all other grandchild processes
    elif parframename == 'run':
        pass

    else:
        haltlogging(lambda: print(
            'unknown frame:'
            f'\t frame: {str(frame)}'
            f'\t parent frame: {str(frame._fback)}'
        ))()


# main func
def main(normalopsboo):
    '''
    For graceful closure to begin, send a KeyboardInterrupt. This will activate
    the graceful closure within the measurement protocol function.
    if KeyboardInterrupt is sent within the graceful closure again, the measurement
    protocols are not tasked to handle that and will throw an error

    Parameters
        normalopsboo: True  -> run skyscan_main
                      False -> run quickscan_main
    '''
    # nomination processes
    if normalopsboo:
        measurement_protocol = skyscan_main
    else:
        measurement_protocol = quickscan_main

    # realtime monitoring
    print('starting scan_event...')
    _procwrapper((exceptions.ScaneventInterrupt,), scan_event).start()

    # running scanning protocol
    print('running measurement protocol...')
    measurement_protocol()


# running
if __name__ == '__main__':
    signal.signal(signal.SIGINT, _handler_f)
    main(NORMALOPSBOO)
