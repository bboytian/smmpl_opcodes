# imports
import multiprocessing as mp

from .global_imports.smmpl_opcodes import *
from .quickscan_main import main as quickscan_main
from .scan_event import main as scan_event
from .skyscan_main import main as skyscan_main


# main func
def main(normalopsboo):
    '''
    Parameters
        normalopsboo: True  -> run skyscan_main
                      False -> run quickscan_main
    '''
    # nomination processes
    if normalopsboo:
        poperation = mp.Process(target=skyscan_main)
    else:
        poperation = mp.Process(target=quickscan_main)

    pscanevent = mp.Process(target=scan_event)

    # running processes
    poperation.start()
    pscanevent.start()


# running
if __name__ == '__main__':
    main(NORMALOPSBOO)
