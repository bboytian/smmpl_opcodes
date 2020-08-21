# imports
import os
import signal
import win32api
import inspect

from . import main_scripting as mains
from .global_imports.smmpl_opcodes import *
from .scan_event import main as scan_event


# handles signals
def _handlerhook_f(dwCtrlType, hook_sigint=signal.SIGINT):
    if dwCtrlType == 0:         # CTRL_C_EVENT
        _handler_f(0, inspect.currentframe)
        return 1                # don't chain to the next handler
    else:
        return 0                # chain to the next handler

def _handler_f(signalnum, frame):
    '''called when signal.signal interrupt is sent'''
    print(frame, frame.f_back)
    framename, framefile = FRAMEPARSEFN(frame)
    parframename, parframefile = FRAMEPARSEFN(frame.f_back)  # parent frame

    # main thread func
    if framename == 'main' and parframename == 'module':
        # graceful closure are handled by the measurement protocols
        pass

    # functions within main thread func
    elif framename == 'main' and parframename == 'main':
        raise mains.MeasurementInterrupt

    # processes started in main thread func
    elif parframefile == 'run' and DIRPARSEFN(parframefile, -2) == 'scan_event':
        raise mains.ScaneventInterrupt

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
        normalopsboo: True  -> run mains.skyscan_main
                      False -> run mains.quickscan_main
    '''
    # nomination of measurement protocol
    if normalopsboo:
        measurement_protocol = mains.skyscan_main
    else:
        measurement_protocol = mains.quickscan_main

    print('press ^C')
    time.sleep(10)
    # realtime monitoring
    # print('starting scan_event...')
    # pscan_event = mains.mtproc_wrapper((mains.ScaneventInterrupt,), scan_event)
    # pscan_event.start()

    # running scanning protocol
    # print('running measurement protocol...')
    # measurement_protocol()


# running
if __name__ == '__main__':
    # signal.signal(signal.SIGINT, _handler_f)
    win32api.SetConsoleCtrlHandler(_handlerhook_f, 1)


    main(NORMALOPSBOO)
