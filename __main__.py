# imports
from .global_imports import *
from .quickscan_main import main as quickscan_main
from .skyscan_main import main as skyscan_main


# main func
def main(normalopsboo):
    '''
    Parameters
        normalopsboo: True  -> run skyscan_main
                      False -> run quickscan_main
    '''
    if normalopsboo:
        skyscan_main()
    else:
        quickscan_main()


# running
if __name__ == '__main__':
    main(NORMALOPSBOO)
