'''
Only run this script before measurement (NOT DURING), it does the following:

-
- Delete previous logfile, which could be due to program opening and closing or usage of program
'''
# imports
import datetime as dt
import os

from ...globalimports import *


# main func
@announcer
def premea_fileman(coldstart_boo):
    '''
    For now, coldstart_boo=False does nothing. This is left as a filler in the
    event we need to configure something.
    the latest datafiles and logfiles are not moved, because they are to be
    treated as one united data set.

    In the scanning and searching of scan_event, the scanpattern file timing will
    be used as the guide to finding the start. But this is most likely an uneeded
    feature, as scan_event is only needed in scan_vis for live visualisation

    Parameters
        coldstart_boo (boolean): determines whether to delete exisiting
                                 mpllogfiles (due to sigmaMPL open and close)
                                 copy mpllogfiles (due to sigmaMPL start kill
                                 during operation)
    '''
    # if coldstart_boo:           # when first running operational measurements
    #     # removing redudant logfiles
    #     mpllogfile_lst = list(filter(
    #         lambda x: MPLLOGFILE[MPLLOGTIMEIND:] in x or
    #         MPLLOGCURFILE in x,
    #         os.listdir(MPLSIGMALOGDIR)
    #     ))
    #     mpllogfile_lst = [dc_gfunc(MPLSIGMALOGDIR,mlf) for mlf in mpllogfile_lst]
    #     for mlf in mpllogfile_lst:
    #         print('removing {}'.format(mlf))
    #         os.remove(mlf)

    # else:                       # when code has already been running operationaly
    #     pass


@announcer
def postmea_fileman():
    '''
    creates a flag file to show where the end of measurement data is
    '''
    now = dt.datetime.now()
    with open(dc_gfunc(
            MPLDATADIR, DATEFMT.format(now),
            MPLEOMFILE.format(now)
    ), 'w') as flag:
        pass



# running
if __name__ == '__main__':
    pass
