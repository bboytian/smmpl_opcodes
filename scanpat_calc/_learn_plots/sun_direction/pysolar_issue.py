# imports
import datetime as dt

import matplotlib.pyplot as plt
# import matplotlib.basic_units as pbu
import numpy as np
import pysolar.solar as pssl


# params

lt, lg = 1.299119, 103.771232
ele = 0

year = 2019
mon_start, mon_end, mon_step = 1, 12, 1 # step !< 1
day_start, day_end, day_step = 1, 1, 1
hr_start, hr_end, hr_step = 0, 23, 1
mn_start, mn_end, mn_step = 0, 59, 1


# generating data
when_ara = np.array([[year, mon_step, day_step, hr_step, mn_step]]) #1st ent tb rm ltr
alt_ara = np.array([])

for mon in range(mon_start, mon_end + 1, mon_step):
    print('retrieving for month {}...'.format(mon))
    for day in range(day_start, day_end + 1, day_step):
        for hr in range(hr_start, hr_end + 1, hr_step):
            for mn in range(mn_start, mn_end + 1, mn_step):
                when = dt.datetime(year, mon, day, hr, mn
                                   , tzinfo=dt.timezone(dt.timedelta(hours=8)))
                when_ara = np.append(when_ara, [[year, mon, day, hr, mn]], axis=0)

                # TOGGLE BETWEEN FAST AND SLOW HERE
                # alt = np.deg2rad(pssl.get_altitude(lt, lg, when, elevation= ele))
                alt = np.deg2rad(pssl.get_altitude_fast(lt, lg, when))#, elevation= ele))    
                alt_ara = np.append(alt_ara, alt)

when_ara = when_ara[1:]
when_ara = when_ara.reshape((mon_end - mon_start) // mon_step + 1
                            , (day_end - day_start) // day_step + 1
                            , (hr_end - hr_start) // hr_step + 1
                            , (mn_end - mn_start) // mn_step + 1
                            , when_ara.shape[-1])
alt_ara = alt_ara.reshape((mon_end - mon_start) // mon_step + 1
                                , (day_end - day_start) // day_step + 1
                                , (hr_end - hr_start) // hr_step + 1
                                , (mn_end - mn_start) // mn_step + 1)


# adjusting data for plot
when_ara = when_ara.reshape(np.prod(when_ara.shape[:-3])
                            , np.prod(when_ara.shape[-3:-1])
                            , when_ara.shape[-1]) # when_ara axis=-1 include yr,...
when_ara = when_ara[..., -2] + when_ara[..., -1]/60
alt_ara = alt_ara.reshape(np.prod(alt_ara.shape[:-2])
                              , np.prod(alt_ara.shape[-2:]))
# taking first derivative
der1alt_ara = np.gradient(alt_ara, when_ara[0][1] - when_ara[0][0], axis=-1)


# plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax1 = ax.twinx()

for i in range(len(when_ara)):
    plot, = ax.plot(when_ara[i], alt_ara[i]
                    , label='month {}'.format(i+1), marker='o')

    ax1.plot(when_ara[i], der1alt_ara[i]
             , color=plot.get_color())

ax.legend(fontsize='x-small')
ax.set_xlabel('local time [24hr]')
ax.set_ylabel('alt [deg]')
ax1.set_ylabel(r'$\frac{d alt}{dt}$ [deg/hr]')

plt.show()
