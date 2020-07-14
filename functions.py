# imports
import sys


# defining functions

def DIRCONFN(*dirl):
    '''
    Windows friendly directory concat function. Works exactly as os.path.join
    in linux.
    Here we assume that the directories are delimited by '/'

    Parameters
        dirl (list): list of path strings
    '''
    path = ''
    for i, dirstr in enumerate(dirl):
        if i == 0:
            path += dirstr
        else:

            if dirstr[0] == '/':    # start anew if argument starts with root
                path = dirstr
            else:
                if path[-1] == '/':
                    path += dirstr
                else:
                    path += '/' + dirstr

    return path


def SETLOGFN(logfile):
    '''
    Directs stdout and stderr to logfile
    '''
    sys.stdout = open(logfile, 'a+')
    sys.stderr = open(logfile, 'a+')

def UNSETLOGFN():
    '''
    Resets stdout and stderr to system default
    '''
    sys.stdout.close()
    sys.stderr.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


def GETRESPONSEFN(message, exitboo, twiceboo, checkboo=False, prevmsg=None):
    '''
    input function can only be used on main thread.
    Keeps prompting for response until it is a definite yes or no

    Parameters
        message (str): prompting string
        exitboo (boolean): decides whether or not to exit when response is 'n'
        twiceboo (boolean): prompts a second time if response == 'y'
        checkboo (boolean): determines whether or not the prompt is from the
                            second check, managed by recursive nature
        prevmsg (str): original prompt message, managed by recursive nature

    Return
        ret (boolean): True -> response was 'y'
                       False -> response was 'n'
    '''
    while True:
        response = input(message + ' y or n\n')
        if response == 'y':
            if twiceboo:
                return GETRESPONSEFN('Are you sure?', exitboo, False,
                                     True, message)
            else:
                return True
        elif response == 'n':
            if exitboo and not checkboo:
                sys.exit(0)         # exits without error
            elif not exitboo and not checkboo:
                return False
            elif checkboo:      # repeats the original prompt
                return GETRESPONSEFN(prevmsg, exitboo, True)
        else:
            print('Enter either y or n\n')


# testing
if __name__ == '__main__':
    # from .params import *

    # print('{}'.format(DIRCONFN(WINDOWFILESDIR, SEDFILE)))

    GETRESPONSEFN('this is a test?', True, True)
