# -------
# imports

import numpy as np


# ---------
# main func


def plot(
        ax, proj,
        hem_vals,
        cone_vals,
        grid_valslst, 
        linestyle, linewidth, alpha, color,
):
    '''
    # plot settings
    alpha:: alpha of line
    color:: color of line

    return:: has no return
    '''
    # getting constants
    R = hem_vals[0]
    r, Thetas, thetas, phis = cone_vals[2:6]
    
    
    # determining projection
    if proj == '3d':
        def f():
            aimline_plts = [
                ax.plot(
                    [0, x_ara[i]], [0, y_ara[i]], [0, z_ara[i]],
                    linewidth=linewidth, linestyle=linestyle,
                    alpha=alpha, color=color
                ) for i in range(len(x_ara))
            ]
                
    elif proj == '2d':
        def f():
            aimline_plts = ax.plot(
                x_ara, y_ara, 'ko',
                markersize=markersize
            )

            
    # operation
    for grid_vals in grid_valslst:
        h = grid_vals[0]

        ## retaining points kept within hemisphere, and out of the sun cone
        markersize = grid_vals[2]
        points_ara = grid_vals[-1]
        pointsmag_ara = np.linalg.norm(points_ara, axis=-1)
        pointsnorm_ara = points_ara / pointsmag_ara[..., None]
        sundir_ara = np.array([
            np.sin(thetas) * np.cos(phis),
            np.sin(thetas) * np.sin(phis),
            np.cos(thetas)
        ])
        
        hem_mask = pointsmag_ara <= R
        cone_mask = np.arccos(np.dot(pointsnorm_ara, sundir_ara)) <= Thetas
        mask = np.subtract(hem_mask, cone_mask, dtype=int).astype(bool)
        x_ara = points_ara[..., 0][mask]
        y_ara = points_ara[..., 1][mask]
        z_ara = points_ara[..., 2][mask]

        ## plotting
        aimline_plts = f()

        
        vals = [np.array([x_ara, y_ara, z_ara]).T]
        return vals, aimline_plts
