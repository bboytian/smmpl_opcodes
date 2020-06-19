# -------
# imports

import os

import matplotlib.pyplot as plt
import matplotlib.basic_units as pbu
import mpl_toolkits.mplot3d.art3d as plt3
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import scipy.optimize as spop
import scipy.signal as spsg

from . import solarpath as slp


# ---------------
# all plot params

disp_z = 1 # plotting solar directions on a unit sphere
lt, lg = 1.299119, 103.771232
ele = 0

year = 2019


# --------------------------------
# plot; path of sun on unit sphere
boo = False

if boo:

    # plot params
    mon_start, mon_end, mon_step = 1, 12, 3 # step !< 1
    day_start, day_end, day_step = 1, 1, 1
    hr_start, hr_end, hr_step = 0, 23, 1
    mn_start, mn_end, mn_step = 0, 0, 1

    # generate data
    x_ara, y_ara, z_ara = slp.solar_func(['x_ara', 'y_ara', 'z_ara'], False
                                     , year, lt, lg, ele, disp_z
                                     , mon_start, mon_end, mon_step
                                     , day_start, day_end, day_step
                                     , hr_start, hr_end, hr_step
                                     , mn_start, mn_end, mn_step)

    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot3D(x_ara, y_ara, z_ara)
    # ax.plot3D([0], [0], [0], 'ro')    # origin

    ## adding color to the plot
    points = np.array([x_ara, y_ara, z_ara]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = plt3.Line3DCollection(segments, cmap=plt.get_cmap('winter'))
    lc.set_array(np.arange(0, len(x_ara), 1))
    lc.set_linewidth(1.1)
    ax.add_collection(lc)

    ax.set_zlim([0,1])
    ax.set_ylim([-1, 1])
    ax.set_ylabel('East - West')
    ax.set_xlabel('South - North')

    plt.show()



# -------------------------------------------------------
# plot; average angular drift of the sun accross the year
'''
peak angular drift of the sun each day, accross the year
angle towards the south/north is negative/positive
'''
boo = False
calc_boo = True
save_boo = False

if boo:

    if calc_boo:

        # plot params
        mon_start, mon_end, mon_step = 1, 12, 1 # step !< 1
        day_start, day_end, day_step = 1, 'all', 1
        hr_start, hr_end, hr_step = 12, 14, 1
        mn_start, mn_end, mn_step = 0, 59, 1

        ## time of least change; determined by change in gradient
        maxdelder1 = 0.05 # the real gauge of angle drifting
        mindelder2 = 0.08 # used to restrict consideration to specific time frame


        # generate daat
        x_ara, y_ara, z_ara, when_ara = slp.solar_func(['x_ara', 'y_ara', 'z_ara'
                                                          , 'when_ara']
                                                         , True
                                                         , year, lt, lg, ele, disp_z
                                                         , mon_start, mon_end, mon_step
                                                         , day_start, day_end, day_step
                                                         , hr_start, hr_end, hr_step
                                                         , mn_start, mn_end, mn_step)
        Theta_ara = np.pi/2 - np.arccos(x_ara)
        Theta_ara = np.rad2deg(Theta_ara)

        ## shaping when_ara for plotting
        when_ara = when_ara.reshape(*when_ara.shape[:-3] # (month, day, hr * mn, time_dim)
                                    , np.prod(when_ara.shape[-3:-1])
                                    , when_ara.shape[-1]) # when_ara axis=-1 include yr,...
        whenmask_ara = np.isnan(when_ara[..., 0, 0])      # (month, day)
        whenmonthcut_ara = np.argmax(whenmask_ara, axis=-1) # shape: (month)
        whenmonthcut_ara = np.array(list(map(lambda x: 31 if x == 0 else x
                                             , whenmonthcut_ara)))
        whenmonthcut_ara = whenmonthcut_ara[tuple([..., ] +\
                                    [None for i in when_ara.shape[1:]])] #(month, 1, 1, 1)
        
        ### adjusting to make decimal month
        when_ara = when_ara[..., 1] + \
                   (when_ara[..., 2]-1)/whenmonthcut_ara[..., 0] + \
                   when_ara[..., 3]/(whenmonthcut_ara[..., 0]*24) + \
                   when_ara[..., 4]/(whenmonthcut_ara[..., 0]*60*24) #(month, day, hr*mn)
        when_ara = when_ara.reshape(np.prod(when_ara.shape[:-1]) # shape: (mon*day, hr*mn)
                                    , when_ara.shape[-1])

        ## Extracting angular drift during optimal measurement time
        Theta_ara = Theta_ara.reshape(np.prod(Theta_ara.shape[:-2]) # (month*day, hr*mn)
                                      , np.prod(Theta_ara.shape[-2:]))
        Thetaind_ara = np.argmin(Theta_ara, axis=-1) # (month*day, )
        Thetaind_ara = np.append(np.arange(len(Thetaind_ara))[..., None] # (month*day, 2)
                                 , Thetaind_ara[..., None], axis=-1)     # 2D ind

        Thetamax_ara = Theta_ara[tuple(Thetaind_ara.T)] # shape:(mon*day)
        whenmax_ara = when_ara[tuple(Thetaind_ara.T)]   # shape:(mon*day)

        ### removing np.nan values
        whenmax_ara = whenmax_ara[~np.isnan(whenmax_ara)]
        Thetamax_ara = Thetamax_ara[~np.isnan(Thetamax_ara)]

        # saving for easier reading
        if save_boo:
            save_ara = np.array([whenmax_ara, Thetamax_ara])
            txt_file = '_visual/plots_peakangdriftdata.txt'
            np.savetxt(txt_file, save_ara)
            
    # plot
    fig, ax = plt.subplots()

    if not calc_boo:
        txt_file = '_visual/plots_peakangdriftdata.txt'    
        whenmax_ara, Thetamax_ara = np.loadtxt(txt_file)

    ## performing curve fit for analytical expression
    def cos_func(ara, a, b, c, d):
        return a*np.cos(b*ara + c) + d
    popt, pcov = spop.curve_fit(cos_func, whenmax_ara, Thetamax_ara, p0=[-23, 0.5, 1, 0])
    pcov = np.sqrt(np.diag(pcov))
    pcovsf_int = np.abs(np.floor(np.log10(pcov)).astype(np.int_))
    for i in range(len(popt)):
        popt[i] = round(popt[i], pcovsf_int[i])
        pcov[i] = round(pcov[i], pcovsf_int[i])
    coeff_lst = [popt[0], pcov[0], popt[1], pcov[1], popt[2], pcov[2], popt[3], pcov[3]]
    analy_str = r'$({}\pm{}) \cos \left[({}\pm{})x + ({} \pm {})\right] + ({}\pm{})$'.\
        format(*coeff_lst)
    Thetamaxfit_ara = cos_func(whenmax_ara, *popt)
        
    ax.plot(whenmax_ara, Thetamax_ara)
    ax.plot(whenmax_ara, Thetamaxfit_ara, label=analy_str)
    ax.axhline(y=0, linewidth=1, color='k')
    
    ax.set_xlim([1, 13])
    ax.set_ylabel('South -- North')
    ax.set_xlabel('Month')
    plt.legend(loc = 1, fontsize='small')
    plt.show()

    
# ----------------------------------------------------
# plot; drift of sun from the EW plane accross the day
'''
angle towards the south/north is negative/positive
'''
boo = True

if boo:

    # plot params
    mon_start, mon_end, mon_step = 1, 12, 1 # step !< 1
    day_start, day_end, day_step = 1, 1, 1
    hr_start, hr_end, hr_step = 0, 23, 1
    mn_start, mn_end, mn_step = 0, 59, 1

    ## time of least change; determined by change in gradient
    maxdelder1 = 0.05 # the real gauge of angle drifting
    mindelder2 = 0.08 # used to restrict consideration to specific time frame


    # generate data
    x_ara, y_ara, z_ara, when_ara = slp.solar_func(['x_ara', 'y_ara', 'z_ara'
                                                      , 'when_ara']
                                                     , True
                                                     , year, lt, lg, ele, disp_z
                                                     , mon_start, mon_end, mon_step
                                                     , day_start, day_end, day_step
                                                     , hr_start, hr_end, hr_step
                                                     , mn_start, mn_end, mn_step)
    Theta_ara = np.pi/2 - np.arccos(x_ara)
    Theta_ara = np.rad2deg(Theta_ara)

    when_ara = when_ara.reshape(np.prod(when_ara.shape[:-3])
                                , np.prod(when_ara.shape[-3:-1])
                                , when_ara.shape[-1]) # when_ara axis=-1 include yr,...
    when_ara = when_ara[..., -2] + when_ara[..., -1]/60
    Theta_ara = Theta_ara.reshape(np.prod(Theta_ara.shape[:-2])
                                  , np.prod(Theta_ara.shape[-2:]))

    ## smoothening Theta_ara for derivative
    # Theta_ara = spsg.savgol_filter(Theta_ara, 51, 5, axis=-1)

    der1Theta_ara = np.gradient(Theta_ara, when_ara[0][1] - when_ara[0][0], axis=-1)
    der2Theta_ara = np.gradient(der1Theta_ara, when_ara[0][1] - when_ara[0][0], axis=-1)

    ## determine optimal time of measurement according to defined thresholds
    der2Theta_mask = der2Theta_ara > mindelder2
    der1Theta_mask = np.abs(der1Theta_ara) < maxdelder1
    Theta_mask = der1Theta_mask * der2Theta_mask

    startind_ara = np.argmax(Theta_mask, axis=-1)[..., None]
    startind_ara = np.append(np.arange(len(startind_ara))[..., None]
                             , startind_ara, axis=-1)
    startwhen_ara = when_ara[tuple(startind_ara.T)]

    endind_ara = np.argmax(Theta_mask[..., ::-1], axis=-1)[..., None]
    endind_ara = np.append(np.arange(len(endind_ara))[..., None], endind_ara, axis=-1)
    endwhen_ara = when_ara[..., ::-1][tuple(endind_ara.T)]

    
    # plot
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(121)
    ax1 = ax.twinx()
    
    for i in range(len(when_ara)):
        plot, = ax.plot(when_ara[i], Theta_ara[i], yunits=pbu.degrees
                        , label='month {}'.format(i+1), marker='o')
        ax.plot(when_ara[i], np.abs(Theta_ara[i]-Theta_ara[i][0]), yunits=pbu.degrees
                , color=plot.get_color())
        
        ax1.plot(when_ara[i], der1Theta_ara[i], yunits=pbu.degrees
                 , color=plot.get_color())
        ax1.plot(when_ara[i], der2Theta_ara[i], yunits=pbu.degrees
                 , color=plot.get_color())

    ax.legend(fontsize='x-small')
    ax.set_xlabel('local time [24hr]')
    ax.set_ylabel('Theta [deg]')
    ax1.set_ylabel(r'$\frac{dTheta}{dt}$ [deg/hr]')


    ax = fig.add_subplot(122)

    for i in range(len(startind_ara)):
        ax.axvspan(startwhen_ara[i], endwhen_ara[i]
                   , ymin=i/len(startind_ara), ymax=(i+1)/len(startind_ara), alpha=0.4)
    ax.axvspan(startwhen_ara.max(), endwhen_ara.min(), alpha=0.4)
    
    ax.set_ylim([0, len(startwhen_ara)+1])
    ax.set_ylabel('month')
    ax.set_xlabel('local time [24hr]')
    
    plt.show()
    

# ---------------------------------
# plot: rate of change of direction
'''
We determine the rate of change of solar direction by taking the magnitude of the first derivative of the solar direction (on unit sphere; determined by all plots params)

We also plot the cylindrical rate of change of solar direction, which is purely the EW component of the rate of change of solar direction

to check for deviation between the two
'''
boo = False

if boo:

    # plot params
    mon_start, mon_end, mon_step = 1, 6, 1 # step !< 1
    day_start, day_end, day_step = 1, 1, 1
    hr_start, hr_end, hr_step = 0, 23, 1
    mn_start, mn_end, mn_step = 0, 59, 5

    # generate data
    x_ara, y_ara, z_ara, when_ara = slp.solar_func(['x_ara', 'y_ara', 'z_ara', 'when_ara']
                                                     , True
                                                     , year, lt, lg, ele, disp_z
                                                     , mon_start, mon_end, mon_step
                                                     , day_start, day_end, day_step
                                                     , hr_start, hr_end, hr_step
                                                     , mn_start, mn_end, mn_step)
    when_ara = when_ara.reshape(np.prod(when_ara.shape[:-3])
                                , np.prod(when_ara.shape[-3:-1])
                                , when_ara.shape[-1]) # when_ara axis=-1 include yr,...
    when_ara = when_ara[..., -2] + when_ara[..., -1]/60
    dir_ara = np.append(np.append(x_ara[..., None], y_ara[..., None], axis=-1)
                        , z_ara[..., None], axis=-1)
    dir_ara = dir_ara.reshape(np.prod(dir_ara.shape[:-3]), np.prod(dir_ara.shape[-3:-1]), 3)
    dircy_ara = dir_ara[..., 1:] # removing the x component to approx cylindrical movement
    
    ## smoothening dir_ara for first derivative
    # dir_ara = spsg.savgol_filter(dir_ara, 51, 5, axis=-2)
    
    ## Taking first derivative
    der1dir_ara = np.gradient(dir_ara, when_ara[0][1] - when_ara[0][0], axis=-2)
    der1magdir_ara = np.linalg.norm(np.abs(der1dir_ara), axis=-1)
    
    der1dircy_ara = np.gradient(dircy_ara, when_ara[0][1] - when_ara[0][0], axis=-2)
    der1magdircy_ara = np.linalg.norm(np.abs(der1dircy_ara), axis=-1)
    
    
    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for i in range(len(when_ara)):
        plot, = plt.plot(when_ara[i], der1magdir_ara[i], label='month={}'.format(i+1))
        plt.plot(when_ara[i], der1magdircy_ara[i]
                 , 'o', label='cylindrical month={}'.format(i+1), color=plot.get_color())        

    plt.legend(fontsize='x-small')
    plt.show()
