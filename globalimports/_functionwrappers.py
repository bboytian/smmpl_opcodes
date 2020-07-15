# imports
from functools import wraps


# defining decorators for global functions
def haltlogging(func):
    '''
    Halts redirection of stdout and stderr logfiles and outputs to __stdout__ and
    __stderr__
    '''
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        oldstdout_logdir = sys.stdout.name
        oldstderr_logdir = sys.stderr.name
        SETLOGFN()
        ret = func(*args, **kwargs)
        SETLOGFN(oldstdout_logdir, oldstderr_logdir)
        return ret
    return wrapper_func
