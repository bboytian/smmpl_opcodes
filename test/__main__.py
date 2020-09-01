# imports
import time

from .one import main as one
from ..global_imports.smmpl_opcodes import *

# params


# main func
def main():
    a = MPPROCWRAPCL(one, args=(1,))
    b = MPPROCWRAPCL(one, args=(2,))

    a.start()
    b.start()

    time.sleep(5)

    result = a.terminate()
    print(result)
    a.close()


# testing
if __name__ == '__main__':
    main()
