def dc_gfunc(*dirl):
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


# testing
if __name__ == '__main__':
    from .params import *

    print('{}'.format(dc_gfunc(WINDOWFILESDIR, SEDFILE)))
