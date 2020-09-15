# imports
import datetime as dt
import time

import requests

from ...global_imports.smmpl_opcodes import *


# params
_starttime = dt.datetime.combine(dt.date.today(),
                                 dt.time(hour=WEBSWITCHLOGSTARTHOUR,
                                         minute=WEBSWITCHLOGSTARTMIN))


# main func
def main():
    nextclear_dt = _starttime + dt.timedelta(WEBSWITCHCLEARPERIOD)
    nextsave_dt = _starttime

    while True:
        now = dt.datetime.now()

        try:

            # saving webswitch log file
            if now >= nextsave_dt:
                # getting html text
                html = requests.get(WEBSWITCHLOGURL,
                                    auth=(WEBSWITCHUSER, WEBSWITCHPASS))

                # saving webswitch log file
                with open(
                        DIRCONFN(MPLDATADIR, DATEFMT.format(now),
                                 WEBSWITCHLOGFILE.format(now)),
                        'w'
                ) as webswitchlog_file:
                    webswitchlog_file.writelines(html.text)

                # iterating next time
                nextsave_dt += dt.timedelta(minutes=WEBSWITCHSAVEPERIOD)

            # clearing log file
            if now >= nextclear_dt:
                # posting html
                html = requests.get(WEBSWITCHCLEARLOGURL,
                                    auth=(WEBSWITCHUSER, WEBSWITCHPASS))
                # iterating next time
                nextclear_dt += dt.timedelta(days=WEBSWITCHCLEARPERIOD)

        except (
                requests.exceptions.ConnectionError
        ):
            continue

        time.sleep(60 * WEBSWITCHWAIT)


# testing
if __name__ == '__main__':
    main()
