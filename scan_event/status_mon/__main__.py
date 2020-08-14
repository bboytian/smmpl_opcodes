# imports
import numpy as np
import pandas as pd

from ...global_imports.smmpl_opcodes import *

# params
_msgprepend = """
Status Monitor
Profile: {}
"""

_gt_d = {                        # greater than
    'Temp #0': TEMPZEROTHRES,
    'Temp #2': TEMPTWOTHRES,
    'Temp #3': TEMPTHREETHRES,
}
_geq_d = {                      # greater than or equal to
    'Background Average': BACKGROUNDONETHRES,
    'Background Average 2': BACKGROUNDTWOTHRES,
    'Energy Monitor': ENERGYHIGHTHRES,
}
_neq_d = {                       # equal to
    'Shots Sum': SHOTSSUMVAL,
    'Trigger Frequency': TRIGGERFREQVAL,
    'A/D Data Bad flag': BADDATAFLAGVAL,
}
_leq_d = {                      # lesser than or equal to
    'Energy Monitor': ENERGYLOWTHRES,
}
_lt_d = {
    'Sync Pulses Seen Per Second': SYNCPULSESSEENVAL,
}

_lastfile_td = pd.Timedelta(LASTFILETIMEDELTATHRES, 'm')

_numberround = 2


# supp func

def _rounder_f(ele):
    try:
        return np.round(ele, _numberround)
    except np.core._exceptions.UFuncTypeError:
        return ele

def _msgfmt_f(startstr, *fmts):
    '''defines the format of the messages'''
    fmts = list(map(lambda x: str(_rounder_f(x)), fmts))
    msg = ' '.join(fmts)
    leftoverlen = MSGLINELENGTH - len(msg)
    startstrlen = len(startstr)
    if len(startstr + msg) > MSGLINELENGTH:
        msg = startstr[:leftoverlen-2] + '..' + msg
    else:
        msg = startstr + ' ' * (leftoverlen - startstrlen) + msg
    msg = '<pre>' + msg + '</pre>\n'
    return msg


# main func
def main(mpld):
    '''
    preformmatted telegram parser cannot handle '<'. This is first identified with
    '&' which is replaced with '&lt' at the end of the function

    Parameters
        mpld (dict): dictionary of mpldata containing the most current profile
    Return
        msg (str): messages to be sent
    '''
    msg = ''

    profile_dt = mpld['Timestamp'][-1]

    # checking values
    for key in _geq_d:
        profval = mpld[key][-1]
        setval = _geq_d[key]
        if profval >= setval:
            msg += _msgfmt_f(key, ':', profval, '>=', setval)
    for key in _gt_d:
        profval = mpld[key][-1]
        setval = _gt_d[key]
        if profval > setval:
            msg += _msgfmt_f(key, ':', profval, ' >', setval)
    for key in _neq_d:
        profval = mpld[key][-1]
        setval = _neq_d[key]
        if profval != setval:
            msg += _msgfmt_f(key, ':', profval, '!=', setval)
    for key in _leq_d:
        profval = mpld[key][-1]
        setval = _leq_d[key]
        if profval <= setval:
            msg += _msgfmt_f(key, ':', profval, '&=', setval)
    for key in _lt_d:
        profval = mpld[key][-1]
        setval = _lt_d[key]
        if profval < setval:
            msg += _msgfmt_f(key, ':', profval, ' &', setval)

    # replacing value for preformmatted parsing
    msg = msg.replace('&', '&lt')

    # returning
    if msg:
        msg = _msgprepend.format(profile_dt) + msg
    return msg


# running
if __name__ == '__main__':
    from ..latestfile_read import main as latestfile_read
    from ..telegram_API import main as telegram_API

    mpl_d = latestfile_read()
    msg = main(mpl_d)
    feedback_l = telegram_API(msg)
