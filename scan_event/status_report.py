# imports
import datetime as dt

from ..global_imports.smmpl_opcodes import *


# params
_msgprepend = """
status_report
Date: {}
"""

# mutable store values
_nextday = LOCTIMEFN(
    dt.datetime.combine(dt.date.today, dt.time()) + dt.timedelta(1),
    UTCINFO
)


# main func
@verbose
@announcer(newlineboo=True)
def main(mpld):
    '''
    Uses the lateset profile from mpld to determine if it is a new day.
    If it is a new day it will report the statistics of the previous day
    '''
    msg = ''

    # checking if should run
    profile_dt = mpld['Timestamp'][-1]
    if profile_dt > _nextday:
        now = dt.datetime.now()
        msg += _msgprepend.format(now)

        global _nextday
        _nextday += dt.timedelta(1)

        # reading previous day's files


            # retrieving previous day's stats



    return msg



# testing
if __name__ == '__main__':
    main()
