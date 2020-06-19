# -------
# imports

import numpy as np


# ---------
# main func


def plot(
        ax, proj,
        r, Thetas,
        thetas, phis,
        alpha, color,
        grid_valslst,
        ints_linewidth
):
    '''
    # values
    r:: height of cone
    Thetas:: [rad] angle between solar direction and lidar SNR limit direction
    thetas, phis:: [rad] solar angle
    grid_valslst:: params from grids to plot projections

    # plot settings
    proj: plotting on 3d axes or 2d axes
    alpha:: alpha of cone
    color:: color of cone
    ints_linewidth:: linewidth of line of intersect surface
    
    return:: vals, [cone_plt, ints_plt], if prog=='2d', cone_plt = None
    '''
    rot_mat = np.matrix([       # rotation about y in thetas then about z in phi
        [np.cos(phis)*np.cos(thetas), -np.sin(phis), np.cos(phis)*np.sin(thetas)],
        [np.sin(phis)*np.cos(thetas), np.cos(phis), np.sin(phis)*np.sin(thetas)],
        [-np.sin(thetas), 0, np.cos(thetas)]

    ])    

    # Plotting surface
    if proj == '3d':
        
        ## generating upright cone
        znum = int(r)
        phinum = int(r)       
        z_mat, phi_mat = np.mgrid[0:r:znum*1j, 0:2*np.pi:phinum*1j]
        rho_mat = z_mat * np.tan(Thetas)
        x_ara = (rho_mat * np.cos(phi_mat)).flatten()
        y_ara = (rho_mat * np.sin(phi_mat)).flatten()
        z_ara = z_mat.flatten()
        vec_mat = np.matrix([x_ara, y_ara, z_ara])

        ## rotating cone
        grid_len = len(z_mat)
        x_mat, y_mat, z_mat = [ara.reshape(grid_len, grid_len) for ara in\
                              rot_mat * vec_mat]
        ## plotting
        cone_plt = ax.plot_surface(
            x_mat, y_mat, z_mat,
            linewidth=0, alpha=alpha, color=color
        )
    elif proj == '2d':
        cone_plt = None


    # Plotting intersect
    for grid_vals in grid_valslst:
        h, l = grid_vals[:2]

        ## generating cone slice
        phinum = 4*int(h)
        rhonum = int(h)

        phi_ara = np.linspace(0, 2*np.pi, phinum)
        z_ara = h / (np.cos(thetas)\
                     - np.tan(Thetas)*np.sin(thetas)*np.cos(phi_ara))
        rhoh = z_ara * np.tan(Thetas)
        x_ara = rhoh  * np.cos(phi_ara)
        y_ara = rhoh * np.sin(phi_ara)
        vec_mat = np.matrix([x_ara, y_ara, z_ara])

        ## rotating cone
        x_ara, y_ara, z_ara = np.array(rot_mat * vec_mat)

        if proj == '3d':
            points_lst = [x_ara, y_ara, z_ara]
        elif proj == '2d':
            points_lst = [x_ara, y_ara]

        ## filtering portions that are not in the planeA
        out_mask = (np.abs(x_ara) > l/2) + (np.abs(y_ara) > l/2)
        for ara in points_lst:
            np.putmask(ara, out_mask, np.nan)

        ## plotting
        ints_plt = ax.plot(
            *points_lst,
            linewidth=ints_linewidth, color=color
        )

        
    val_lst = [
        ax, proj,
        r, Thetas,
        thetas, phis,
        alpha, color,
        grid_valslst,
        ints_linewidth
    ]
    return val_lst, [cone_plt, ints_plt]
