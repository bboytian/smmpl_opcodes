'''
organises the following files:

- useful MPLLog.txt file from sigma/Log; excluding the one that is currently being written on
- .mpl files from sigma/DATA
'''
# imports
import datetime as dt
import os
import os.path as osp
import shutil

from ...params import *


# main function
def main(tailend_boo):
    '''
    shutil.copy is assumed to not interrupt with sigmaMPL writing to the .mpl 
    file
    
    current log file being written to is not copied over. It is assumed that 
    sigmaMPL starts a new logfile when measurement is stopped.

    this means that scan_vis with scan_event life update cannot be run via 
    SOLARIS server, but has to be run on the local computer

    Parameters
        tailend_boo (boolean): decides whether or not to move the latest mpl file
                               should be True when wrapping up operations
    '''
    print('start {}@{:%Y%m%d%H%M}'.format(__name__, dt.datetime.now()))

    # # getting file lst(absolute path), and date lst
    # mplfile_lst = list(filter(
    #     lambda x:MPLFILE[MPLTIMEIND:] in x,
    #     os.listdir(MPLSIGMADATADIR)
    # ))
    # mplfile_lst.sort()
    # mpllatestfile = mplfile_lst.pop() # to be copied safely
    # mpldate_lst = [mf[:MPLDATEIND] for mf in mplfile_lst]
    
    # mpllogfile_lst = list(filter(
    #     lambda x: MPLLOGFILE[MPLLOGTIMEIND:] in x,
    #     os.listdir(MPLSIGMALOGDIR)
    # ))
    # mpllogdate_lst = [mlf[:MPLLOGDATEIND] for mlf in mpllogfile_lst]

    # filename_lst = mplfile_lst + mpllogfile_lst
    # filedir_lst = [osp.join(MPLSIGMADATADIR, mf) for mf in mplfile_lst]\
    #     + [osp.join(MPLSIGMALOGDIR, mlf) for mlf in mpllogfile_lst]
    # date_lst = mpldate_lst + mpllogdate_lst
    
    # # making non existent directories; required for shutil move
    # d_lst = list(set(date_lst))
    # for date in d_lst:
    #     datadate_dir = osp.join(MPLDATADIR, date)
    #     if not osp.exists(datadate_dir):
    #         os.mkdir(datadate_dir)

    # # moving files; preserving nomenclature
    # for i, filedir in enumerate(filedir_lst):
    #     newfiledir = osp.join(MPLDATADIR, date_lst[i], filename_lst[i])
    #     print('moving {} -> {}'.format(filedir, newfiledir))
    #     # shutil.move(filedir, newfiledir)
    #     shutil.copy(filedir, newfiledir)

    # # copying the latest .mpl file in case software is still writing
    # mpllatestfiledir = osp.join(MPLSIGMADATADIR, mpllatestfile)        
    # newmpllatestfiledir = osp.join(MPLDATADIR, mpllatestfile[:MPLDATEIND],
    #                                mpllatestfile)

    # if tailend_boo:
    #     print('move current .mpl file {} -> {}'.\
    #           format(mpllatestfiledir, newmpllatestfiledir))
    #     shutil.move(mpllatestfiledir, newmpllatestfiledir)                
    # else:
    #     print('copying current .mpl file {} -> {}'\
    #           .format(mpllatestfiledir, newmpllatestfiledir))        
    #     shutil.copy(mpllatestfiledir, newmpllatestfiledir)        
    
    
    print('done {}@{:%Y%m%d%H%M}'.format(__name__, dt.datetime.now()))

    
# running
if __name__ == '__main__':
    main(False)
