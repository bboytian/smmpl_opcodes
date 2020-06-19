# imports
import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pysolar.solar as pssl


# params
lt, lg = 1.299119, 103.771232
ele = 0

# getting time array
start = pd.Timestamp('2020-02-10')
end = pd.Timestamp('2020-02-11')
when_ara = pd.date_range(start, end, freq='min', tz='Asia/Singapore')

# calculating altitude
alt_ara = np.array([
    np.deg2rad(pssl.get_altitude(lt, lg, when, elevation=ele))\
    for when in when_ara
])

# taking first derivative
der1alt_ara = np.gradient(alt_ara, when_ara[1].value - when_ara[0].value)

# plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax1 = ax.twinx()

ax.plot_date(when_ara, alt_ara, '-', color='C0')
ax1.plot_date(when_ara, der1alt_ara, '-', color='C1')

ax.legend(fontsize='x-small')
ax.set_xlabel('local time [24hr]')
ax.set_ylabel('alt [deg]')
ax1.set_ylabel(r'$\frac{d alt}{dt}$ [a.u.]')

plt.show()
