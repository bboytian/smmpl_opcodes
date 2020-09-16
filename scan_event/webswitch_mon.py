# imports
import datetime as dt

import numpy as np
import requests

from ..file_readwrite import webswitch_reader
from ..global_imports.smmpl_opcodes import *

# params
_previouswin_starttime = None

_msgprepend = """
webswitch_mon
Log Entry: {}
"""
_numberround = 2

_geq_d = {                      # greater than or equal to
    'Enclosure Humidity': WEBSWITCHHUMIDTHRES,
    'Enclosure Temp': WEBSWITCHHIGHTEMPTHRES
}
_leq_d = {                      # lesser than or equal to
    'Enclosure Temp': WEBSWITCHLOWTEMPTHRES
}

_key_d = {
    'Enclosure Temp': 's1_ta',
    'Enclosure Humidity': 's2_ta'
}

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
@verbose
@announcer(newlineboo=True)
def main(*args):
    '''
    searches any threshold spikes in the last WEBSWITCHMONWINDOW minutes,
    returns the extreme values in each window.

    Only returns a message if the last notification time is not in the same time
    window
    '''
    global _previouswin_starttime

    msg = ''

    # retrieving latest data from webswitch
    html = requests.get(WEBSWITCHLOGURL, auth=(WEBSWITCHUSER, WEBSWITCHPASS))

    # parsing data within the window
    now = LOCTIMEFN(dt.datetime.now(), UTCINFO)
    starttime = now - dt.timedelta(minutes=WEBSWITCHMONWINDOW)
    webswitch_d = webswitch_reader(
        text=html.text,
        starttime=starttime
    )

    if webswitch_d:
        # doing threshold checks
        for key in _geq_d:
            profval_a = webswitch_d[_key_d[key]]
            setval = _geq_d[key]
            if (profval_a >= setval).any():
                msg += _msgfmt_f(key, ':', profval_a.max(), '>=', setval)
        for key in _leq_d:
            profval_a = webswitch_d[_key_d[key]]
            setval = _leq_d[key]
            if (profval_a <= setval).any():
                msg += _msgfmt_f(key, ':', profval_a.min(), '&=', setval)

        # replacing value for preformmatted parsing
        msg = msg.replace('&', '&lt')

        # returning
        if msg:
            try:
                if now > _previouswin_starttime + dt.timedelta(WEBSWITCHMONWINDOW):
                    msg = _msgprepend.format(now) + msg
                    _previouswin_starttime = now
                else:
                    msg = ''
            except TypeError:      # if it's the first time it is notifying
                msg = _msgprepend.format(now) + msg
                _previouswin_starttime = now

    return msg


# testing
if __name__ == '__main__':
    import time

    print(main())
    time.sleep(10)
    print(main())                      # should not return
