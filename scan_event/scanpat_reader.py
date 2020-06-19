'''
This file serves to read the scanpattern files for a certain day in retrospect.

The parsing of the scanpattern file is not expected to change in format, as such no paramters are created

future improvements:
- operational measurements might consist of various scan pattern files
'''
# imports
import os
import os.path as osp

import numpy as np
import pandas as pd


# main func
def main(data_dir):
    '''
    Parameters
        data_dir (str): dirname of file
        filename (str): filename

    Returns
        ang_ara (np array): array containing scan angles [deg] in
                            chronological order,(chrono, 2(azi, ele)
    '''
    # reading files
    ## edit this part for multiple files
    filename = list(filter(lambda x: x[-11:]=='scanpat.txt',
                           os.listdir(data_dir)))[0]        
    scanpat_df = pd.read_csv(osp.join(data_dir, filename),
                             sep=',', header=None)
    
    ang_ara = scanpat_df.to_numpy()
    
    return ang_ara


# testing
if __name__ == '__main__':
    
    file_dir = '/home/tianli/SOLAR_EMA_project/data/20200304'

    ang_ara = main(file_dir)

    print(ang_ara)
