# imports
import multiprocessing as mp


# Process class
class mtproc_wrapper(mp.Process):
    '''
    To be used in a way similar to multiprocessing.Process.
    terminates process base on specified exceptions
    '''
    def __init__(self, exception_t, target, args=(), kwargs={}):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self.exception_t = exception_t

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except self.exception_t as e:
            self.terminate()
            print('done terminating')
