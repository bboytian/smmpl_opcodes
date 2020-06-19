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
    timestamp:: pd.Timestamp
    '''

    timestamp = timestamp.to_pydatetime(warn=False)    
    
    # API data retrieval; pysolar
    solhor = np.deg2rad(
        pssl.get_altitude_fast(
            lt, lg,
            timestamp
        )
    )
    bearing = np.deg2rad(
        pssl.get_azimuth_fast(
            lt, lg,
            timestamp
        )
    )

    # converting to spherical coordinates, origin in local coords
    thetas = np.pi/2 - solhor # solar zenith angle
    phis = 2*np.pi - bearing

    return thetas, phis
