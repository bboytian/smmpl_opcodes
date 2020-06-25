'''
This file serves to read all yyyyMMddHHmmMPLLog.txt files for a certain day in retrospect.

The parsing of the MPLLog file is not expected to change in format, as such no paramters are created

for now test files do not follow proper measurement sop, there are multiple program starts. To combat this we take the last one

future improvements would be able to handle multiple dates
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
        file_dir (str): file path

    Returns
        time_ara (pd.Series):array containing times inwhich scanner
                             is in position
    '''
    # reading files
    loglines = np.array([])            
    for filename in os.listdir(data_dir)[::-1]: # chronolo order
        if filename[-10:] == 'MPLLog.txt':
            with open(dc_gfunc(data_dir, filename),'r') as txtfile:
                loglines = np.append(loglines, txtfile.readlines())

    # getting date for parsing
    day = int(data_dir[-2:])
    if day < 10:
        dateend_pos = 22 + 1
        parseend_pos = 66 + 1
    else:
        dateend_pos = 23 + 1
        parseend_pos = 67 + 1

    # slicing data to start when prog starts
    loglinesm1 = np.vectorize(lambda x:x[-3:])(loglines)
    ## edit here once we have good SOP
    progstart_pos = np.argwhere(loglinesm1 == '* \n')[-1][0]
    loglines = loglines[progstart_pos:]

    # parsing all scanner movements
    time_ara = np.vectorize(lambda x:x[:dateend_pos])(loglines)
    time_ara = pd.to_datetime(time_ara)
    scanmoveboo_ara = np.vectorize(
        lambda x:x[parseend_pos-4:parseend_pos]
    )(loglines) == '4253' 
    time_ara = time_ara[scanmoveboo_ara]
    
    return time_ara


# testing
if __name__ == '__main__':
    
    file_dir = '/home/tianli/SOLAR_EMA_project/data/smmpl_E2/20200304'

    time_ara = main(file_dir)
