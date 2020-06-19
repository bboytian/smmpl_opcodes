'''
code has to be run by gitbash, as rsync is in gitbash
uses rsync to sync specified data folder with specified data folder in solaris
By default syncs current day and previous day's data.
'''
# imports
import datetime as dt
import os

from ...params import *


# static params
_gitbash_mpldatadir = MPLDATADIR.replace('C:', '/c') # required for rsync


# main func
def main(syncday_lst=None):
    '''
    Parameters
        syncday_lst (lst): list objects are strings of the format DATEFMT
    '''
    print('start {}@{:%Y%m%d%H%M}'.format(__name__, dt.datetime.now()))
    # # getting timings; sync today and uesterday
    # if not syncday_lst:
    #     today = dt.datetime.now()
    #     syncday_lst = [
    #         DATEFMT.format(today),
    #         DATEFMT.format(today - dt.timedelta(1))
    #     ]    

    # # rsync
    # cmd_str = 'rsync -azzvi -e ssh -R {}/./{{{}}} {}@{}:{}'\
    #     .format(
    #         _gitbash_mpldatadir, ','.join(syncday_lst),
    #         SOLARISUSER, SOLARISIP, SOLARISMPLDATADIR
    #     )
    # os.system(cmd_str)
    
    print('done {}@{:%Y%m%d%H%M}'.format(__name__, dt.datetime.now()))    

        
# running
if __name__ == '__main__':
    main()
