from .exceptions import *
from .mtproc_wrapper import mtproc_wrapper
from .quickscan_main import main as quickscan_main
from .skyscan_main import main as skyscan_main

# realtime monitoring
from ..scan_event import main as scan_event
print('starting scan_event...')
mtproc_wrapper((ScaneventInterrupt,), scan_event).start()
