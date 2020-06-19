'''
visualisations decribed in SOLAR/EMA logbook 17-12-19 Upcoming MPL codes 
pointer d.ii.1-4

note that the measurement might not be exact because we are lacking
1. accurate measurement of elevation
2. temperature and pressure for refration correction
'''

# -------
# imports

import datetime as dt

import numpy as np
import pysolar.solar as pssl
from . import API_SunPositionCalculator as spc


# --------------
# main functions

# generates solar data
def solar_func(ret_strlst, noflat_boo
               , year, lt, lg, ele, disp_z
               , mon_start, mon_end, mon_step
               , day_start, day_end, day_step
               , hr_start, hr_end, hr_step
               , mn_start, mn_end, mn_step):
    '''
    ret_strlst:: tells the func what to return ,e.g. ['x_ara', 'y_ara']
    day_end:: if day_end == 'all', it goes through all the days for that given month
    
    return:: arrays given in ret_lststr

    adjustment notes:
    1. main API adjustments would be under 'API data retrieval' method
    2. if there are added variables to be returned, be sure to add them to the 'topping up' section to fill up the days to reach 31 days
    3. there is no option to iterate year as of now, this would increase the complexity of the array management of when_ara, mainly in the second plot (max angular drift across year)
    '''
    # list for no. of days per month
    if year%4 == 0:             # leap year
        numdays_lst = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:                       # not leap year
        numdays_lst = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]        

        
    # creating store variables    
    when_ara = np.array([[year, mon_step, day_step, hr_step, mn_step]]) #1st ent tb rm ltr
    theta_ara, phi_ara = np.array([]), np.array([])
    x_ara, y_ara, z_ara = np.array([]), np.array([]), np.array([])
    
    
    # iterating through time range
    for mon in range(mon_start, mon_end + 1, mon_step):
        ## changing no. of days to fit each month
        if day_end == 'all':
            day_e = numdays_lst[mon-1]
        else:
            day_e = day_end

        print('retrieving for month {}...'.format(mon))

        ## continuing with iteration 
        for day in range(day_start, day_e + 1, day_step):
            for hr in range(hr_start, hr_end + 1, hr_step):
                for mn in range(mn_start, mn_end + 1, mn_step):
                    when = dt.datetime(year, mon, day, hr, mn
                                       , tzinfo=dt.timezone(dt.timedelta(hours=8)))
                    when_ara = np.append(when_ara, [[year, mon, day, hr, mn]], axis=0)

                    
    # API data retrieval; pysolar
                    bearing, solhor = np.deg2rad(
                        pssl.get_position(lt, lg,
                                          when, elevation=ele)
                    )
    # API data retrieval; SunPositionCalculator
                    # solhor = np.deg2rad(spc.getSEA(lt, lg, when))
                    # bearing = np.deg2rad(spc.getAZ(lt, lg, when))

    # converting to spherical coordinates, origin in local coords
                    theta = np.pi/2 - solhor # solar zenith angle
                    phi = 2*np.pi - bearing
                    theta_ara = np.append(theta_ara, theta)
                    phi_ara = np.append(phi_ara, phi)

                    
    # converting to cartesian
                    x_ara = np.append(x_ara, disp_z * np.sin(theta) * np.cos(phi)) # NorthSouth
                    y_ara = np.append(y_ara, disp_z * np.sin(theta) * np.sin(phi)) # WestEast
                    z_ara = np.append(z_ara, disp_z * np.cos(theta))

                    
    # preparing data for return
                    
        ## topping up missing values to create rectangular matrix
        ## ; only if iterating through all days of the month
        if day_end == 'all' and noflat_boo:        
            fill_ara = np.empty([((hr_end - hr_start)//hr_step + 1) * \
                                 ((mn_end - mn_start)//mn_step + 1) * \
                                 (31 - day_e)
                                 , len(when_ara[0])])
            fill_ara.fill(np.nan)
            when_ara = np.append(when_ara, fill_ara, axis=0)

            fill_ara = np.empty([((hr_end - hr_start)//hr_step + 1) * \
                                 ((mn_end - mn_start)//mn_step + 1) * \
                                 (31 - day_e)])
            fill_ara.fill(np.nan)
            x_ara = np.append(x_ara, fill_ara)
            y_ara = np.append(y_ara, fill_ara)
            z_ara = np.append(z_ara, fill_ara)

    ## removing first entry from when ara; see 'creating store variables'
    when_ara = when_ara[1:]

    ## reshaping arrays
    local_dict = locals()
    ret_lststr = '['+ ', '.join(ret_strlst)  +']'
    exec('ret_lst = {}'.format(ret_lststr), {}, local_dict)
    ret_lst = local_dict['ret_lst']    
    if noflat_boo:              # reshapes into the shape of the iterations
        if day_end != 'all':
            day_e = day_end
        else:
            day_e = 31
        
        for i in range(len(ret_strlst)):
            if ret_strlst[i] == 'when_ara':
                ret_lst[i] = ret_lst[i].reshape((mon_end - mon_start) // mon_step + 1
                                                , (day_e - day_start) // day_step + 1
                                                , (hr_end - hr_start) // hr_step + 1
                                                , (mn_end - mn_start) // mn_step + 1
                                                , when_ara.shape[-1])
            else:
                ret_lst[i] = ret_lst[i].reshape((mon_end - mon_start) // mon_step + 1
                                                , (day_e - day_start) // day_step + 1
                                                , (hr_end - hr_start) // hr_step + 1
                                                , (mn_end - mn_start) // mn_step + 1)
                
    return ret_lst
    

