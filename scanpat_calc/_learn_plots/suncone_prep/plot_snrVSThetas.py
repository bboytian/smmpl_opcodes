# imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ... import sunforecaster as sf
from ....scan2ara import ncreader as sanr


data20200228_dir = '/home/tianli/SOLAR_EMA_project/data/20200228'
data20200228_ara = sanr.main(data20200228_dir)


_sf = sf.sunforecaster(8, razonlt_flt, razonlg_flt, razonele_flt)
pysolarthetas_ara, pysolarphis_ara = _sf.get_anglesvec(ts_sr)
pysolarthetas_ara = np.rad2deg(pysolarthetas_ara)
pysolarphis_ara = np.rad2deg(pysolarphis_ara)
