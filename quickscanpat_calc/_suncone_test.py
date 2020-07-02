# imports
import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..globalimports import *
from ..scanpat_calc.sunforecaster import sunforecaster
from ..scan_vis.plotshapes import cone as cone


# params
Thetas = THETAS

SCALE = 1.3
CURLYL = 30
u = 10                          # unit length


# computing sun angles
sf = sunforecaster(LATITUDE, LONGITUDE)
observetime = pd.Timestamp('202007021500').tz_localize(
    dt.timezone(dt.timedelta(hours=8))
)
thetas, phis = sf.get_angles(observetime)


# computing lidar point
rsz = u * np.cos(thetas)
rsx = u * np.sin(thetas) * np.cos(phis)
rly = rsy = u * np.sin(thetas) * np.sin(phis)  # considered to be static

a = (rsz**2) + (rsx**2)
bOm2rsz = (np.cos(Thetas) * (u**2) - (rsy**2))

b = -2 * bOm2rsz * rsz
c = (bOm2rsz**2) - (rsx**2) * (rsx**2 + rsz**2)

prlz = (-b + np.sqrt((b**2) - 4*a*c))/2/a
mrlz = (-b - np.sqrt((b**2) - 4*a*c))/2/a

prlx = (bOm2rsz - rsz*prlz)/rsx
mrlx = (bOm2rsz - rsz*mrlz)/rsx


# creating figure
fig3d = plt.figure(figsize=(10, 10), constrained_layout=True)
ax3d = fig3d.add_subplot(111, projection='3d')
ax3d.pbaspect = [SCALE, SCALE, SCALE]
ax3d.set_xlabel('South -- North')
ax3d.set_ylabel('East -- West')
ax3d.set_xlim([-CURLYL/2, CURLYL/2])
ax3d.set_ylim([-CURLYL/2, CURLYL/2])
ax3d.set_zlim([0, CURLYL])


# plotting lidar point
ax3d.scatter(prlx, rly, prlz, 'ro')
ax3d.scatter(mrlx, rly, mrlz, 'go')


# plotting cone
for conelen in [u, 30]:
    cone_ps = cone(
        ax3d, 0,
        None, None,
        conelen,
        False,
        0.1, f'C{conelen}',
        1,
        thetas=thetas, phis=phis,
        Thetas=Thetas,
    )
    cone_ps.plot_ts()
    
cone_ps = cone(
    ax3d, 0,
    None, None,
    30,
    False,
    0.1, 'C3',
    1,
    thetas=thetas, phis=phis,
    Thetas=0.001,
)
cone_ps.plot_ts()


# showing
plt.show()
