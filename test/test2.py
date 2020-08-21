# imports
import time
from .exceptions import *

# params


# main func
def main():
    try:
        time.sleep(5)
    except FuncError:
        print('function terminated')
        time.sleep(3)



# testing
if __name__ == '__main__':
    main()
