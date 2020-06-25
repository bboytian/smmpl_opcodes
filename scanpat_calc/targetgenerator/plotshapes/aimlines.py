# imports
import numpy as np

from ....globalimports import *


# class
class aimlines:

    def __init__(
            self,
            grid_lst,
            hem, cone,
            closeprox_thres
    ):
    
        '''
        in the comments Np/s is the number of pixels per width of the 
        primary/secondary grid
        likewise p/s... represents the elipsis in the shape of the 
        primary/secondary grid

        a comment block is left there in case we want to remove points that 
        have the maximum number of proximity points; can be removed in the future
        if strategy is good

        Future
            - add in filter that prevents removing points due to uncertainty in 
              lidar scanner arm

        Parameters
            grid_lst (list): list of grid objects, to get target points
            hem (targenerator.hemisphere)
            cone (targetgenerator.cone)
            closeprox_thres (float): [km] threshold distance between points of 
                                     different grids can substitute each other
        Methods
            gen: generates masks for each grid's points, i.e. coord_matlst
        '''
        # Attributes
        self.closeprox_thres = closeprox_thres
        
        ## static
        self.grid_lst = grid_lst
        self.hem_masklst = hem.grid_masklst
        ## changing
        self.cone = cone
        self.swath_masklst = None

        ## for future calc
        self.coord_matlst = None
        self.mask_matlst = None
        self.dir_matlst = None
        self.keep_masklst = None


        # init
        self.gen()

    
    # main meth
    def gen(self):

        # updating changed variables
        self.swath_masklst = self.cone.grid_masklst                    

        # operation
        self.coord_matlst, self.mask_matlst = [], []
        self.dir_matlst = []
        self.keep_masklst = []
        for i, gridi in enumerate(self.grid_lst):

            # retrieving masks
            hem_mask = self.hem_masklst[i]
            swath_mask = self.swath_masklst[i]

            # retrieving points from other grids
            coord_mat = gridi.coord_mat
            x_mat, y_mat = coord_mat[..., 0], coord_mat[..., 1]
            z_mat = coord_mat[..., 2]
            r_mat = np.linalg.norm(coord_mat, axis=-1)
            dir_mat = np.stack((
                r_mat,
                np.arccos(z_mat/r_mat),
                np.arctan2(y_mat, x_mat),
            ), axis=-1)

            # retrieving data from current grid
            h, l, Lp, n = gridi.h, gridi.l, gridi.Lp, gridi.n
            sec_mat = coord_mat[..., :2] # (Ns, Ns, s..., 2)
            secsdot_enum = tuple(i for i in range(2,len(sec_mat[..., 0].shape)))
            proxsdot_enum = tuple(i + 1 for i in secsdot_enum)
            
            # mask for considering points from other grids
            keep_mask = np.ones_like(sec_mat[...,0]).astype(bool)#(Ns, Ns, s...)
            keepshape = keep_mask.shape
            keepgridshape = keepshape[:2]
            for j, gridj in enumerate(self.grid_lst[:i]):

                # retrieve grid points for more impt grid
                pridir_mat = self.dir_matlst[j]
                pri_mask = self.mask_matlst[j]
                theta_ara = pridir_mat[..., 1][pri_mask].flatten()
                phi_ara = pridir_mat[..., 2][pri_mask].flatten()
                r_ara = h * np.tan(theta_ara)
                x_ara = r_ara * np.cos(phi_ara)
                y_ara = r_ara * np.sin(phi_ara)
                pri_ara = np.stack((x_ara, y_ara), axis=-1)

                # resample more important grid                
                rspri_mat = resample_func(pri_ara, l, Lp)

                # determine proximity for more important
                ## expanding dimensions for subtraction
                brsec_mat = broadcast_func(sec_mat, rspri_mat.shape[2:-1], 2)
                rspri_mat = broadcast_func(rspri_mat, sec_mat.shape[2:-1], 3)
                ## calc prox; (Ns, Ns, prod(p...), s...)
                prox_mat = np.linalg.norm(brsec_mat-rspri_mat, axis=-1)
                
                # choosing which points to keep in current grid
                prox_mat = prox_mat < self.closeprox_thres#(Ns,Ns,prod(p..),s..)
                pproxcount_mat = np.sum(#(Ns, Ns, s...)
                    prox_mat, axis=2    # represents how many points frm pri_mat
                )                       # are close to those in sec_mat

                '''removes points that have the max no. of proximity points'''
                # pproxcountmax_mat = np.max(pproxcount_mat, axis=secsdot_enum)
                # pproxcountmax_mat = broadcast_func(pproxcountmax_mat,
                #                                    pproxcount_mat.shape[2:], 2)
                # keepj_mask = ~( # times by pproxcount_mat to account for filler
                #     pproxcount_mat * (pproxcount_mat=pproxcountmax_mat)
                # ).astype(bool)

                '''remove points that have any proximity points'''
                keepj_mask = ~(pproxcount_mat.astype(bool))
                keepjcount_mat = np.sum(keepj_mask, axis=secsdot_enum)#(Ns,Ns)
                sproxcount_mat = np.sum( # (Ns, Ns)
                    prox_mat.any(axis=proxsdot_enum),
                    axis=2    # represents how many points frm sec_mat
                )             # are close to those in pri_mat
                addtruecount_mat = (n - keepjcount_mat - sproxcount_mat)
                addtruecount_mat[addtruecount_mat < 0] = 0
                for ii in np.ndindex(*keepgridshape):
                    keepj_mask[ii] = addtrue_func(keepj_mask[ii],
                                                  addtruecount_mat[ii])

                # apply previous keep mask to keep_mask
                keep_mask = (keepj_mask * keep_mask).astype(bool)
                
            ### combine mask and apply
            mask_mat = (hem_mask * swath_mask * keep_mask).astype(bool)

            # storing
            self.coord_matlst.append(coord_mat)
            self.mask_matlst.append(mask_mat)
            self.dir_matlst.append(dir_mat)
            self.keep_masklst.append(keep_mask)


# supp methods for gen()
def resample_func(pri_ara, sec_l, sec_Lp):
    '''
    resamples the points in pri_mat to the grid shape of sec_mat

    Parameters
        pri_mat (np.array): primary flattened array to be resampled 
                            ; (Np x Np x prod(p...), 2(x, y))
        sec_l (float): grid size of grid to deduct points from
        sec_Lp (float): pixel size of grid to deuct points from
    Return
        inpoints_mat (np.array): array of similar shape to secondary grid
                                 unequal no. of points in each pixel, filled by
                                 FILLERNUM
                                 ; (Ns, Ns, prod(p...) + filler, 2(x, y))
    '''
    Ns = int(np.ceil(sec_l/sec_Lp))
    prilen = len(pri_ara)
    inpoints_mat = [] # (Ns x Ns, prilen, 2)
    for i, j in np.ndindex(Ns, Ns):
        inpixel_mask = (
            (pri_ara[..., 0] >= (i - Ns/2)*sec_Lp)  \
            * (pri_ara[..., 0] <= (i+1 - Ns/2)*sec_Lp) \
            * (pri_ara[..., 1] >= (j - Ns/2)*sec_Lp) \
            * (pri_ara[..., 1] <= (j+1 - Ns/2)*sec_Lp)
        ).astype(bool)
        inpoints_ara = np.stack(
            (pri_ara[:, 0][inpixel_mask], pri_ara[:, 1][inpixel_mask]),
            axis=-1
        )
        inpoints_ara = np.append( # (prilen, 2)
            inpoints_ara, FILLERNUM*np.ones((prilen-len(inpoints_ara), 2)),
            axis=0
        )
        inpoints_mat.append(inpoints_ara)
    inpoints_mat = np.array(inpoints_mat)
    mleninpoints = np.max(np.sum(inpoints_mat[..., 0]<FILLERNUM, axis=1))
    inpoints_mat = inpoints_mat[..., :mleninpoints, :]
    inpoints_mat = inpoints_mat.reshape(Ns, Ns, *inpoints_mat.shape[1:])
    return inpoints_mat #(Ns,Ns,mleninpoints,2)
    
    

def broadcast_func(mat, expshape, insertind):
    '''
    expands an array and stacks according to slice of shape provided, at the 
    location indicated.

    Parameters
        mat (np.array): array to be broadcasted 
                        (a..., b...); len(a...) == insertind
        expshape (array like): shape to expand to 
        insertind (int): axis to insert shape
    Return 
        ret (np.array): (a..., *expshape, b...)
    '''
    ret = mat.copy()
    for _, num in enumerate(expshape[::-1]):
        ret = np.expand_dims(ret, axis=insertind)
        ret = np.repeat(ret, num, axis=insertind)
    return ret
        
def addtrue_func(ara, num):
    '''
    changes the values of ara to True, until the total number of True in ara is 
    the original number plus num
    '''
    argwhere = np.argwhere(~ara)[:num]
    ret = ara.copy()
    ret[tuple(argwhere.T)] = True
    return ret
