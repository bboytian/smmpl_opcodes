# imports
import os

from ..global_imports.smmpl_opcodes import *


# main func
def main():
    '''
    delete .mpl files and .mplLog files existing in the SigmaMPL folder

    this function will throw an error if the SigmaMPL program has locked the file
    One should untick the 'save file' check box before running this function
    again
    '''
    # finding any existing files
    mpl_l = FINDFILESFN(MPLFILE, MPLSIGMADATADIR)
    mpl_l.sort(reverse=True)    # making the current .mpl file the first position
    log_l = FINDFILESFN(MPLLOGCURFILE, MPLSIGMALOGDIR) \
        + FINDFILESFN(MPLLOGFILE, MPLSIGMALOGDIR)

    # prompting before deleting
    mplnum = len(mpl_l)
    lognum = len(log_l)
    GETRESPONSEFN(
        f'There are {lognum} mpllog files and'
        f' {mplnum} mpl files, do you want to delete them?',
        True, True
    )

    # deleting files
    print('deleting files...')
    for fl in mpl_l + log_l:
        print(f'\t{fl}')
        os.remove(fl)


# running
if __name__ == '__main__':
    main()
