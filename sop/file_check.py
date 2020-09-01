# imports
import os

from ..global_imports.smmpl_opcodes import *


# main func
def main():
    '''
    the system will check for any existing logfiles and
    mplfiles. If there are, the user can choose whether to delete the files.
    If the files are not deleted, the function will raise an exception to halt
    the program, for the user to move the files manually.
    Note that this requires an input which multiprocessing cannot handle, thus
    the function has to be called on the main thread
    '''
    # finding any existing files
    mpllogfile_lst = list(filter(
        lambda x: MPLLOGFILE[MPLLOGTIMEIND:] in x or
        MPLLOGCURFILE in x,
        os.listdir(MPLSIGMALOGDIR)
    ))
    mpllogfile_lst = [DIRCONFN(MPLSIGMALOGDIR, mlf) for mlf in mpllogfile_lst]

    mplfile_lst = list(filter(
        lambda x: MPLFILE[MPLTIMEIND:] in x,
        os.listdir(MPLSIGMADATADIR)
    ))
    mplfile_lst = [DIRCONFN(MPLSIGMADATADIR, mf) for mf in mplfile_lst]

    # asking user
    if mpllogfile_lst or mplfile_lst:
        GETRESPONSEFN(
            f'There are {len(mpllogfile_lst)} mpllog files and'
            f' {len(mplfile_lst)} mpl files, shall we continue?',
            True, True
        )

# running
if __name__ == '__main__':
    main()
