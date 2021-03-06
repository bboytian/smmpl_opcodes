# imports
import datetime as dt
import pandas as pd

from ..global_imports.smmpl_opcodes import *


# params
_msgprepend = """
nonewprofile_check
"""
_timedeltathres = pd.Timedelta(NONEWPROFTIMETHRES, 'm')


# main func
@verbose
@announcer(newlineboo=True)
def main(mpld):
    msg = ''

    now = LOCTIMEFN(dt.datetime.now(), UTCINFO)
    profile_dt = mpld['Timestamp'][-1]

    if now - profile_dt > _timedeltathres:
        msg = '<pre>' + 'No new profile since:' + '</pre>\n'\
            + '<pre>' + f'{profile_dt}' + '</pre>\n'\
            + '<pre>' + 'timedelta threshold:' + '</pre>\n'\
            + '<pre>' + f'{_timedeltathres}' + '</pre>\n'
        msg = _msgprepend + msg

    return msg


# testing
if __name__ == '__main__':
    pass
