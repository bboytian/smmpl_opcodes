# imports
import datetime as dt

import numpy as np
import pandas as pd

from ..file_readwrite.mpl_reader import smmpl_reader
from ..global_imports.smmpl_opcodes import *


# params
_msgprepend = """
status_report
Date: {}
Number Of Profiles: {}
"""
_numberround = 2
_key_l = [
    'Temp #0',
    'Temp #2',
    'Temp #3',
    'Background Average',
    'Background Average 2',
    'Energy Monitor',
    'Shots Sum',
    'Trigger Frequency',
    'A/D Data Bad flag',
    'Sync Pulses Seen Per Second',
]


# mutable store values
_nextday = LOCTIMEFN(
    dt.datetime.combine(dt.date.today(), dt.time()) + dt.timedelta(1),
    UTCINFO
)


# supp func
def _rounder_f(ele):
    try:
        return np.round(ele, _numberround)
    except np.core._exceptions.UFuncTypeError:
        return ele

def _msgfmt_f(key, *vals):
    '''defines the format of the messages'''
    vals = list(map(lambda x: str(_rounder_f(x)), vals))

    keyline = key
    keylinelen = len(keyline)
    leftoverlen = keylinelen - (MSGLINELENGTH + 1)
    if keylinelen > MSGLINELENGTH:
        keyline = keyline[:leftoverlen-3] + '..'
    keyline += ':'

    avgline = f'  avg = {vals[0]} +/- {vals[-1]}'
    maxline = f'  max = {vals[1]}'
    minline = f'  min = {vals[2]}'

    msg = [keyline, avgline, maxline, minline]
    msg = list(map(lambda x: f'<pre>{x}</pre>\n', msg))
    msg = ''.join(msg)
    return msg


# main func
@verbose
@announcer(newlineboo=True)
def main(mpld):
    '''
    Uses the lateset profile from mpld to determine if it is a new day.
    If it is a new day it will report the statistics of the previous day
    '''
    global _nextday

    msg = ''

    # checking if should run
    profile_dt = mpld['Timestamp'][-1]
    if profile_dt > _nextday:

        # reading previous day files from data dir
        readday = _nextday - dt.timedelta(1)
        readdir = DIRCONFN(MPLDATADIR, DATEFMT.format(readday))
        mpl_l = FINDFILESFN(MPLFILE, readdir)

        # supplementing with files still in SigmaMPL folder
        sigma_l = FINDFILESFN(MPLFILE, MPLSIGMADATADIR)
        sigma_l = [
            sigma for sigma in sigma_l
            if pd.Timestamp(LOCTIMEFN(
                    DIRPARSEFN(
                        sigma, MPLTIMEFIELD
                    ), UTCINFO
            )).date == readday
        ]
        mpl_l += sigma_l

        # retrieving stats, reading data file by file
        numprofiles = 0
        avg_d = {key: 'empty' for key in _key_l}
        max_d = {key: 'empty' for key in _key_l}
        min_d = {key: 'empty' for key in _key_l}
        stdev_d = {key: 'empty' for key in _key_l}
        for mpl in mpl_l:
            mpl_d = smmpl_reader(mplfiledir=mpl, verbboo=True)
            if not mpl_d:       # for empty dictionaries
                continue

            for key in _key_l:
                key_ta = mpl_d[key]

                lenval = len(key_ta)
                avgval = key_ta.mean()
                maxval = key_ta.max()
                minval = key_ta.min()
                stdevval = key_ta.std()

                numprofiles += lenval

                try:
                    avg_d[key] = (
                        (numprofiles - lenval)*avg_d[key]
                        + lenval*avgval
                    ) / numprofiles
                    if maxval > max_d[key]:
                        max_d[key] = maxval
                    if minval < min_d[key]:
                        min_d[key] = minval
                    stdev_d[key] = np.sqrt(stdev_d[key]**2 + stdevval**2)

                except TypeError:
                    avg_d[key] = avgval
                    max_d[key] = maxval
                    min_d[key] = minval
                    stdev_d[key] = stdevval

        # generating message
        now = dt.datetime.now()
        msg += _msgprepend.format(now, numprofiles)
        for key in _key_l:
            msg += _msgfmt_f(
                key,
                avg_d[key],
                max_d[key],
                min_d[key],
                stdev_d[key],
            )

        # iterating day
        _nextday += dt.timedelta(1)

    return msg


# testing
if __name__ == '__main__':
    fakempl_d = {'Timestamp': [LOCTIMEFN(dt.datetime.now(), 8)]}
    msg = main(fakempl_d)
    print(msg)
