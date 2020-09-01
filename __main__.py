# imports
import multiprocessing as mp
import time

from .caliskyscan_main import main as caliskyscan_main
from .quickscan_main import main as quickscan_main
from .scan_event import main as scan_event
from .skyscan_main import main as skyscan_main
from .sop import file_man, file_check

from .global_imports.smmpl_opcodes import *


# main func
def main(measurementprotocol):
    '''
    Parameters
        normalopsboo: True  -> run skyscan_main
                      False -> run quickscan_main
    '''

    # live data events monitoring
    if SCANEVENTBOO:
        print(f'starting scan_event with delay {FIRSTMEASURETIME}s...')
        MPPROCWRAPCL(
            target=scan_event, waittime=FIRSTMEASURETIME,
            stdoutlog=DIRCONFN(
                MPLDATADIR, DATEFMT.format(today),
                SCANEVENTLOG.format(today)
            )
        ).start()

    # data organisation and sync
    if FILEMANBOO:
        print(f'starting sop.file_man with delay {FIRSTMEASURETIME}s...')
        MPPROCWRAPCL(
            target=file_man, args=(False,), waittime=FIRSTMEASURETIME,
            stdoutlog=DIRCONFN(
                MPLDATADIR, DATEFMT.format(today),
                FILEMANLOG.format(today)
            )
        ).start()

    # checking for files; will prompt if there are files
    file_check()

    # measurement protocol
    print(f'starting measurement protocol: {measurementprotocol}...')
    if measurementprotocol == SKYSCANPROTOCOL:
        skyscan_main()
    elif measurementprotocol == QUICKSCANPROTOCOL:
        quickscan_main()
    elif measurementprotocol == CALISKYSCANPROTOCOL:
        caliskyscan_main()


# running
if __name__ == '__main__':
    main(MEASUREMENTPROTOCOL)
