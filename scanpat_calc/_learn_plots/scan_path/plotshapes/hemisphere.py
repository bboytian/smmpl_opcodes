# -------
# imports

import numpy as np


# ---------
# main func

def plot(
        ax, proj,
        r,
        alpha, color,
        grid_valslst,
        ints_linewidth,
):
    '''
    # values
    r:: radius of hemisphere
    grid_valslst:: params from grids to plot projections

    # plot settings
    proj: plotting on 3d axes or 2d axes
    alpha:: alpha of hemipshere
    color:: color of hemisphere
    ints_linewidth:: line of intersect between hemisphere and plane
    '''

    # plotting surface    
    if proj == '3d':
        thetanum = int(r)
        phinum = 4*thetanum
        theta_mat, phi_mat = np.mgrid[0:np.pi/2:thetanum*1j, 0:2*np.pi:phinum*1j]
        x_ara = (r * np.sin(theta_mat) * np.cos(phi_mat)).flatten()
        y_ara = (r * np.sin(theta_mat) * np.sin(phi_mat)).flatten()
        z_ara = (r * np.cos(theta_mat)).flatten()

        hem_plt = ax.plot_trisurf(
            x_ara, y_ara, z_ara,
            linewidth=0, alpha=alpha, color=color
        )
    elif proj == '2d':
        hem_plt = None

        
    # plotting intersect
    for grid_vals in grid_valslst:
        h, l = grid_vals[:2]

        phinum = 5*int(h)        
        phi_ara = np.linspace(0, 2*np.pi, phinum)
        x_ara = np.sqrt(r**2 - h**2) * np.cos(phi_ara)
        y_ara = np.sqrt(r**2 - h**2) * np.sin(phi_ara)
        z_ara = h * np.ones_like(x_ara)

        if proj == '3d':
            points_lst = [x_ara, y_ara, z_ara]
        elif proj == '2d':
            points_lst = [x_ara, y_ara]
            
        ## filtering segments of the ring that are not in the plane
        out_mask = (np.abs(x_ara) > l/2) + (np.abs(y_ara) > l/2)
        for ara in points_lst:
            np.putmask(ara, out_mask, np.nan)

        ## plotting
        ints_plt = ax.plot(
            *points_lst,
            linewidth=ints_linewidth, color=color
        )
                
    return [r], [hem_plt, ints_plt]
