# imports
import multiprocessing as mp
import time

from .quickscan_main import main as quickscan_main
from .scan_event import main as scan_event
from .skyscan_main import main as skyscan_main
from .sop import file_man

from .global_imports.smmpl_opcodes import *


# main func
def main(measurementprotocol):
    '''
    Parameters
        normalopsboo: True  -> run skyscan_main
                      False -> run quickscan_main
    '''
    # measurement protocol
    if measurementprotocol == SKYSCANPROTOCOL:
        meaprotocol = skyscan_main
    if measurementprotocol == QUICKSCANPROTOCOL:
        meaprotocol = quickscan_main

    mp.Process(
        target=meaprotocol,
    ).start()


    # waittime before monitoring and data sync begins
    time.sleep(FIRSTMEASURETIME)

    # live data events monitoring
    mp.Process(
        target=scan_event,
    ).start()

    # data organisation and sync
    mp.Process(
        target=file_man
    ).start()


# running
if __name__ == '__main__':
    main(MEASUREMENTPROTOCOL)
