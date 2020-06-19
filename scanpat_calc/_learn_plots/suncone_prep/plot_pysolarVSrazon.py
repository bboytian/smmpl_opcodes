import datetime as dt

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from ... import sunforecaster as sf


file_dir = '/home/tianli/SOLAR_EMA_project/data/20200323/202003230623razon.csv'

razon_df = pd.read_csv(file_dir, header=3)

razonlt_flt = razon_df['Latitude (Degrees )'][0]
razonlg_flt = razon_df['Longitude (Degrees)'][0]
razonele_flt = 70.8 + 1.6       # [m], by trimble and est height of platform

razondate_sr = razon_df['Date Local (yyyy-mm-dd)']
razontime_sr = razon_df['Time Local ( hh:mm ) ']
razonazi_ara = razon_df['SolarAzimuth (Degrees)'].to_numpy()
razonzen_ara = razon_df['SolarZenith (Degrees)'].to_numpy()

ts_sr = pd.to_datetime(razondate_sr + razontime_sr)
ts_sr = ts_sr.dt.tz_localize(dt.timezone(dt.timedelta(hours=8)))

_sf = sf.sunforecaster(razonlt_flt, razonlg_flt, razonele_flt)
pysolarthetas_ara, pysolarphis_ara = _sf.get_anglesvec(ts_sr)
pysolarthetas_ara = np.rad2deg(pysolarthetas_ara)
pysolarphis_ara = np.rad2deg(pysolarphis_ara)

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

color = 'tab:red'
ax1.set_ylabel('angles [deg]', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax1.plot_date(ts_sr, 360-razonazi_ara, '-', label='razon_azi')
ax1.plot_date(ts_sr, razonzen_ara, '-', label='razon_zen')
ax1.plot_date(ts_sr, pysolarphis_ara, '-', label='pysolar_azi')
ax1.plot_date(ts_sr, pysolarthetas_ara, '-', label='pysolar_zen')

color = 'tab:blue'
ax2.set_ylabel('angle diff', color=color)  # we already handled the x-label with ax1

ax2.plot_date(ts_sr, 360-razonazi_ara - pysolarphis_ara,
              '-', label='azi razon-pysolar', color='C4')
ax2.plot_date(ts_sr, razonzen_ara - pysolarthetas_ara,
              '-', label='zen razon-pysolar', color='C5')

ax1.set_xlabel('local time')
plt.tight_layout()
ax1.legend(loc=2)
ax2.legend(loc=1)
plt.show()
