import numpy as np

# ---------
# relv func

def npoint_func(
        disp_str,
        Lp, n,
        x_mat, y_mat,
):
    '''
    disptype_str:: 
        grid => n must be square rootable
    '''
    xcoord_ara  = x_mat[:-1, :-1].flatten() + Lp/2
    ycoord_ara =  y_mat[:-1, :-1].flatten() + Lp/2
    coord_ara = np.append(xcoord_ara[..., None], ycoord_ara[..., None], axis=-1)
    
    if n == 1:
        return xcoord_ara, ycoord_ara

    else:
    
        if disp_str == 'grid':
            def f(coord):
                sqrtn = int(np.sqrt(n))
                xLbound = coord[0] + Lp*(1/(sqrtn+1) - 1/2)
                xRbound = coord[0] + Lp*(1/2 - 1/(sqrtn+1)) 
                yLbound = coord[1] + Lp*(1/(sqrtn+1) - 1/2)
                yRbound = coord[1] + Lp*(1/2 - 1/(sqrtn+1))           
                x_mat, y_mat = np.mgrid[xLbound : xRbound : sqrtn*1j,
                                        yLbound : yRbound : sqrtn*1j]
                return x_mat.flatten(), y_mat.flatten()

            newcoord_ara = np.apply_along_axis(f, -1, coord_ara)
            newx_ara = newcoord_ara[..., 0, :].flatten()
            newy_ara = newcoord_ara[..., 1, :].flatten()

        return newx_ara, newy_ara

# ---------
# main func

def plot(
        ax, proj,
        h, l,
        Lp, n, disp_str, 
        markersize, linewidth, alpha, linealpha, color,
):
    '''
    # values
    h:: height of plane
    l:: length of grid
    Lp:: pixel size
    n: no.s of scan points within each grid, has to be square rootable
    disp_str:: dispersion type of 

    # plot settings
    proj: plotting on 3d axes or 2d axes
    linewidth:: linewidth of grid
    alpha:: alpha of plane; alpha of gridlines = 1
    linealpha:: alpha of grid lines
    color:: color of all plots

    return:: points, all plots in a list
    '''

    # computation of grid points
    xp_mat, yp_mat = np.mgrid[-l/2:l/2:2j, -l/2:l/2:2j]  
    
    xg_mat, yg_mat = np.mgrid[-l/2 : l/2 : (l/Lp + 1)*1j, # for 3d grid lines
                            -l/2 : l/2 : (l/Lp + 1)*1j]
    zg_mat = h*np.ones_like(xg_mat)
    x_ara, y_ara = npoint_func(
        disp_str,
        Lp, n,
        xg_mat, yg_mat)
    z_ara = h*np.ones_like(x_ara)
    
    # plots
    if proj == '3d':

        # plotting plane
        xp_ara = xp_mat.flatten()
        yp_ara = yp_mat.flatten()    
        zp_ara = h*np.ones_like(xp_ara)          
        plane_plt = ax.plot_trisurf(
            xp_ara, yp_ara, zp_ara,
            linewidth=0, alpha=alpha, color=color
        )

        # plotting grid        
        grid_plt = ax.plot_wireframe(
            xg_mat, yg_mat, zg_mat,
            linewidth=linewidth, alpha=linealpha, color=color
        )

        # plotting scan target points
        scat_plt = ax.scatter(
            x_ara, y_ara, zs=z_ara,
            s=markersize, color=color
        )


    if proj == '2d':

        # plotting plane
        xp_ara, yp_ara = xp_mat.T[0], yp_mat[0]
        plane_plt = ax.fill_between(
            xp_ara, yp_ara[0], yp_ara[1],
            alpha=alpha, color=color)

        # plotting grid
        grid_plt = None
        xg_ara, yg_ara = xg_mat.T[0], yg_mat[0] # for 2d grid lines        
        for xg in xg_ara:
            ax.axvline(xg, linewidth=linewidth, alpha=linealpha, color=color)
        for yg in yg_ara:
            ax.axhline(yg, linewidth=linewidth, alpha=linealpha, color=color)
            
        # plotting scan target points
        scat_plt = ax.plot(
            x_ara, y_ara, 'o',
            markersize=markersize, color=color
        )
        

    vals = [h, l,
            markersize,
            np.array([x_ara, y_ara, z_ara]).T 
    ]
    return vals, [plane_plt, grid_plt, scat_plt]
        
