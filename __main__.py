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

    # live data events monitoring
    # print(f'starting scan_event with delay {FIRSTMEASURETIME}s...')
    # MPPROCWRAPCL(
    #     target=scan_event, waittime=FIRSTMEASURETIME,
    # ).start()

    # data organisation and sync
    print(f'starting sop.file_man with delay {FIRSTMEASURETIME}s...')
    MPPROCWRAPCL(
        target=file_man, waittime=FIRSTMEASURETIME, args=(False,)
    ).start()

    # measurement protocol
    print(f'starting measurement protocol: {measurementprotocol}...')
    if measurementprotocol == SKYSCANPROTOCOL:
        skyscan_main()
    if measurementprotocol == QUICKSCANPROTOCOL:
        quickscan_main()


# running
if __name__ == '__main__':
    main(MEASUREMENTPROTOCOL)
