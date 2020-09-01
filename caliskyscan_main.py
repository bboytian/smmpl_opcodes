# imports
import datetime as dt
import time

from .global_imports.smmpl_opcodes import *
from .quickscan_main import main as quickscan_main
from .skyscan_main import main as skyscan_main


# main func
def main():
    '''
    measurement protocol for scanning the clouds, while conducting weekly
    horisweep for the sake of tracking the drift of the scanner head azimuthal
    calibration point

    It will skip the horisweep protocol if the code is started on the same day
    that the horisweep protocol is supposed to happen

    This measurment protocol does not have it's own logging system as it
    essentially calls other measurement protocols
    '''
    today = dt.date.today()

    # finding next calibration time
    daydelta = CALISKYSCANSTARTDAY - dt.datetime.now().weekday()
    if daydelta <= 0:           # here it chooses to skip the horisweep protocol
        daydelta += 7           # if code started on the same day
    nextcali_dt = LOCTIMEFN(
        dt.datetime.combine(
            today,
            dt.time(CALISKYSCANSTARTHOUR, CALISKYSCANSTARTMIN)
        ), UTCINFO
    ) + dt.timedelta(daydelta)

    # starting sky scan measurement
    pskyscan = MPPROCWRAPCL(
        target=skyscan_main,
        stdoutlog=DIRCONFN(
            MPLDATADIR, DATEFMT.format(today),
            SKYSCANLOG.format(today)
        )
    )
    pskyscan.start()

    # interrupt for calibration
    while True:
        now = LOCTIMEFN(dt.datetime.now(), UTCINFO)
        if now >= nextcali_dt:

            # stopping skyscan protocol
            pskyscan.terminate

            # starting horisweep protocol
            today = dt.date.today()
            phorisweep = MPPROCWRAPCL(
                target=quickscan_main,
                stdoutlog=DIRCONFN(
                    MPLDATADIR, DATEFMT.format(today),
                    QUICKSCANLOG.format(today)
                ),
                kwargs={
                    'quickscantype': 'horisweep',
                    'sphil': CALISKYSCANSAZIMUTH,
                    'ephil': CALISKYSCANEAZIMUTH ,
                    'philspacing': CALISKYSCANAZIMUITHSPACE,
                    'elevation': CALISKYSCANELEVATION
                }
            )
            phorisweep.start()

            # waiting for horisweep to end
            time.sleep(CALIHORISWEEPDURATION * 60)
            phorisweep.terminate()

            # starting skyscan protocol
            pskyscan = MPPROCWRAPCL(
                target=skyscan_main,
                stdoutlog=DIRCONFN(
                    MPLDATADIR, DATEFMT.format(today),
                    SKYSCANLOG.format(today)
                )
            )
            pskyscan.start()

            # iterating next interruption
            nextcali_dt += dt.timedelta(7)



# testing
if __name__ == '__main__':
    main()
