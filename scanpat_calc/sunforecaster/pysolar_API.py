import datetime as dt

import numpy as np
import pandas as pd
import pysolar.solar as pssl


def func(
        timestamp,
        lt, lg,
        elevation=0
):
    '''
    pd.Timestamp is convert to dt.Datetime for compatibility with pysolar

    Parameters
        timestamp (pd.Timestamp): timestamp of the angle we want to retrieve

    Return
        thetas, phis [rad]
    '''
    timestamp = timestamp.to_pydatetime(warn=False)

    # API data retrieval; pysolar
    bearing, solhor = np.deg2rad(
        pssl.get_position(
            lt, lg,
            timestamp, elevation=elevation)
    )

    # converting to spherical coordinates, origin in local coords
    thetas = np.pi/2 - solhor # solar zenith angle
    phis = 2*np.pi - bearing

    return thetas, phis
