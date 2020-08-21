class MainthreadInterrupt(Exception):
    def __init__(self, *args):
        self.name = 'SkyscanInterrupt'
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

class MeasurementInterrupt(Exception):
    def __init__(self, *args):
        self.name = 'MeasurementInterrupt'
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

class ScaneventInterrupt(Exception):
    def __init__(self, *args):
        self.name = 'SkyscanInterrupt'
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
