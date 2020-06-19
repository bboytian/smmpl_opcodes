# importing the libraries
import os.path as osp
import numpy as np

# params
filename = '/connexis_scanpttn_20200228.txt'

azioffset = 140.96
azistep = 0.03
azistart, azistop = 85-azioffset, 93-azioffset

elestep = 0.01
elestart, elestop = 0, 0.01

# writing scan pattern
with open(osp.dirname(osp.abspath(__file__)) + filename, 'a') as txt_file:
    for azimuth in np.arange(azistart, azistop, azistep):
        for elevation in np.arange(elestart, elestop, elestep):

            txt_file.write('{}, {}\n\n'.format(round(azimuth, 2), round(elevation, 3)))
            txt_file.write('{}, {}\n\n'.format(round(azimuth, 2), round(elevation, 3)))
