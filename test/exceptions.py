class MainError(Exception):
    def __init__(self, *args):
        self.name = 'MainError'
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return f'{self.name}, {self.message} '
        else:
            return f'{self.name} has been raised'

class FuncError(Exception):
    def __init__(self, *args):
        self.name = 'FuncError'
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return f'{self.name}, {self.message} '
        else:
            return f'{self.name} has been raised'


class ProcError(Exception):
    def __init__(self, *args):
        self.name = 'ProcError'
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return f'{self.name}, {self.message} '
        else:
            return f'{self.name} has been raised'
