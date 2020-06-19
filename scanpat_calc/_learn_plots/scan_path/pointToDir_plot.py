# -------
# imports

import os

import matplotlib.animation as pan
import matplotlib.gridspec as pgd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from . import plotshapes as ps
# from .plotshapes.aimlines import func as aimlines_func
# from .plotshapes.cone import func as cone_func
# from .plotshapes.grid import func as grid_func
# from .plotshapes.hemisphere import func as hem_func

# from ..sun_direction import solarpath as slp


# ------
# params

# variables [km]
R = 15                      
L0 = 6
Lp = 1

H = np.sqrt(R**2 - (L0**2)/2)

# plot params
curlyL = 2 * R

hem_alpha = 0.2
hemints_linewidth=3

cone_alpha = 0.2
coneints_linewidth = 3

grid_markersize = 10
grid_linewidth = 0.5
grid_alpha = 0.4
grid_linealpha=0.6

aimline_linewidth = 1
aimline_alpha = 0.2
aimline_linestyle = '-'
aimline_color = 'k'

# init params
initthetas, initphis = np.pi/12, 0
initThetas = 0.05


# -----
# setup

def setup_func(ax, proj):
    
    # grids; has to come first
    grid_lst = [                  # [grid_valslst, grid_pltlst]
        ps.grid.plot(           
            ax, proj,
            h=14, l=L0*1.5,
            Lp=Lp, n=1, disp_str='grid',
            markersize=grid_markersize, linewidth=grid_linewidth,
            alpha=grid_alpha, linealpha=grid_linealpha,
            color='C2'
        ), 
        # grid_func(           
        #     ax, proj,
        #     h=10, l=20,
        #     Lp=Lp, n=1, disp_str='grid',
        #     markersize=grid_markersize, linewidth=grid_linewidth,
        #     alpha=grid_alpha, linealpha=grid_linealpha,
        #     color='C3'
        # ),
    ]
    grid_valslst = list(map(lambda x:x[0], grid_lst))

    
    # other objects
    lidarhem_vals, _ = ps.hemisphere.plot(
        ax, proj,
        r=R,
        alpha=hem_alpha, color='C0',
        grid_valslst=grid_valslst,
        ints_linewidth=hemints_linewidth
    )
    suncone_vals, suncone_plts = ps.cone.plot(
        ax, proj,
        r=H*2, Thetas=initThetas,
        thetas=initthetas, phis=initphis,
        alpha=cone_alpha, color='C1',
        grid_valslst=grid_valslst,
        ints_linewidth=coneints_linewidth
    )
    targlines_vals, targlines_plts = ps.aimlines.plot(
        ax, proj,
        hem_vals=lidarhem_vals,
        cone_vals=suncone_vals,
        grid_valslst=grid_valslst,
        linestyle=aimline_linestyle, linewidth=aimline_linewidth,
        alpha=aimline_alpha, color=aimline_color
    )

    
    # returning plot objects to be updated
    dic = {}
    dic['cone_lst'] = ['suncone']
    dic['aimlines_lst'] = ['targlines']
    
    ## For plot updating
    dic['suncone'] = [suncone_vals, suncone_plts]
    dic['targlines'] = [targlines_vals, targlines_plts]
    
    return dic


# -----------
# Init Figure
'''
0. animation of scan in both 3D plots; have to optimise the initialisation

1. API option for suncone update; triggering might have to use pydispatcher

2. path planning; mainly for the projection on XY plane plot, for static sun

3. path planning with moving sun
'''

fig = plt.figure(figsize=(20, 10), constrained_layout=True)
gs = pgd.GridSpec(1, 2, figure=fig)


# spatial visualisation plot
ax = fig.add_subplot(gs[:, :1], projection='3d')
scale = 1.3
ax.pbaspect = [scale, scale, scale]
ax.set_xlabel('South -- North')
ax.set_ylabel('East -- West')
ax.set_xlim([-curlyL/2, curlyL/2])
ax.set_ylim([-curlyL/2, curlyL/2])
ax.set_zlim([0, curlyL])

proj3d_dic = setup_func(ax, '3d')


# grid projection visualisation plot
ax1 = fig.add_subplot(gs[:, 1:])
ax1.set_xlabel('South -- North')
ax1.set_ylabel('East -- West')
ax1.margins(0)

proj2d_dic = setup_func(ax1, '2d')


# ----------------
# animation update; hardcoded for Init Figure

thetas, phis = initthetas, initphis
frames = 100
def update_func(scapegoat):
    '''
    scapegoat:: placed there to fill in the positional argument
    
    thetas, phis, frames:: global variables which are adjusted via 
                           inputting in fargs in pan.FuncAnimation
    '''
    global thetas, phis, counter, frames
    thetas = thetas
    phis += 2*np.pi / frames

    for proj_dic in [proj3d_dic, proj2d_dic]:

    # updating cones
        for cone in proj_dic['cone_lst']:
            cone_vals = proj_dic[cone][0]
            [cone_plt, ints_plt] = proj_dic[cone][1]

            try:                    # when dealing with '2d' projection
                cone_plt.remove()
            except AttributeError:
                pass
            ints_plt[0].remove()

            proj_dic[cone][0], proj_dic[cone][1] = ps.cone.plot(
                *cone_vals[:4],
                thetas, phis,
                *cone_vals[6:]
            )

    # updating aimlines
    '''finish here'''
    


# -------
# animate

animation = pan.FuncAnimation(
    fig, update_func,
    frames=frames, interval=1
)

plt.show()
