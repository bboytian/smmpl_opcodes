# imports
import matplotlib.pyplot as plt
import numpy as np


# main func
def main(conelen, *dir_aa):
    fig3d = plt.figure(figsize=(10, 10), constrained_layout=True)
    ax3d = fig3d.add_subplot(111, projection='3d')
    ax3d.set_xlabel('South -- North')
    ax3d.set_ylabel('East -- West')

    for dir_a in dir_aa:

        # plotting points in order of lines
        rx_a = conelen * np.sin(dir_a[:, 1]) * np.cos(dir_a[:, 0])
        ry_a = conelen * np.sin(dir_a[:, 1]) * np.sin(dir_a[:, 0])
        rz_a = conelen * np.cos(dir_a[:, 1])
        ax3d.plot(rx_a, ry_a, rz_a)
        ax3d.scatter(rx_a, ry_a, rz_a)

        # plotting aimlines
        ind_a = range(0, len(rx_a)+1, 2)
        rx_a = np.insert(rx_a, ind_a, 0)
        ry_a = np.insert(ry_a, ind_a, 0)
        rz_a = np.insert(rz_a, ind_a, 0)
        ax3d.plot(rx_a, ry_a, rz_a, alpha=0.2)

        ax3d.set_xlim([-1, 1])
        ax3d.set_ylim([-1, 1])
        ax3d.set_zlim([-1, 1])

    plt.show()
