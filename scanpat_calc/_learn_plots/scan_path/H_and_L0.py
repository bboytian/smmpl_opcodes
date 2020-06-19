# -------
# imports

import matplotlib.pyplot as plt
import numpy as np


# ---------
# operation

fig = plt.figure()
ax = fig.add_subplot(111)

for R in range(15, 27, 2):
    L0o2 = np.linspace(0, 18, 10000)
    H = np.sqrt(R**2 - 0.5 * (L0o2*2)**2)
    ax.plot(L0o2, H, label='R={}'.format(R))
    ax.set_xlabel('L0/2')
    ax.set_ylabel('H')

plt.legend(fontsize='small')
plt.show()
