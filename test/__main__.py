import time
import os.path as osp

from .. import sop
from ..globalimports import *

wd = osp.dirname(osp.abspath(__file__))
sp_l = list(map(lambda x: DIRCONFN(wd, x), filter(
    lambda x: '.txt' in x, os.listdir(wd)
)))


def main():

    print(sp_l)
    sop.sigmampl_boot(sp_l[0], coldstart_boo=True, tailend_boo=False)

    time.sleep(120)

    sop.sigmampl_boot(sp_l[1], coldstart_boo=True, tailend_boo=False)
    

if __name__ == '__main__':
    main()
