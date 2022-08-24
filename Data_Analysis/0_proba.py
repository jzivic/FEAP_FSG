import numpy as np
import pandas as pd

from matplotlib import pyplot as plt


z =[i for i in range(10)]

rad = [i*2 for i in z]
tawss = [i**2 for i in z]


def net():
    t = np.arange(0.01, 10.0, 0.01)
    data1 = np.exp(t)
    data2 = np.sin(2 * np.pi * t)

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('exp', color=color)
    ax1.plot(t, data1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
    ax2.plot(t, data2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

# net()



def dupli_graf():
    fig, graf_tawss = plt.subplots()

    color = 'tab:red'
    graf_tawss.set_xlabel('tawss', color=color)
    graf_tawss.set_ylabel('z')

    graf_tawss.plot(tawss, z, color=color)
    graf_tawss.tick_params(axis='x', labelcolor=color)


    graf_radius = graf_tawss.twiny()

    color = 'tab:blue'
    graf_radius.set_xlabel('radius', color=color)  # we already handled the x-label with ax1
    graf_radius.plot(rad, z, color=color)
    graf_radius.tick_params(axis='x', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

# dupli_graf()


def dupli_graf():
    Z_cont_DG, inner_cont_DG, ILT_cont_DG = Z_cont, inner_cont, ILT_cont

    Z_cont_DG.append(Z_cont_DG[-1])
    inner_cont_DG.append(inner_cont_DG[-1])
    ILT_cont_DG.append(ILT_cont_DG[-1])

    fig, graf_tawss = plt.subplots()

    color_tawss = 'tab:red'
    graf_tawss.set_xlabel('TAWSS [Pa]', color=color_tawss)
    graf_tawss.set_ylabel('$z$ [mm]')

    graf_tawss.plot(TAWSS, Z_cont_DG, color=color_tawss)
    graf_tawss.axvline(x=0.4, linestyle='--', color="red", label='axvline - full height')
    graf_tawss.tick_params(axis='x', labelcolor=color_tawss)

    graf_tawss.set_xlim([0.3, 0.7])
    graf_tawss.set_ylim([50, 200])

    graf_radius = graf_tawss.twiny()

    color_r = 'tab:blue'
    graf_radius.set_xlabel('$r$ [mm]', color=color_r)  # we already handled the x-label with ax1
    graf_radius.plot(inner_cont_DG, Z_cont_DG, color=color_r)
    graf_radius.plot(ILT_cont_DG, Z_cont_DG, color=color_r)
    # plt.grid(which='both', linestyle='--', linewidth='0.5')

    graf_radius.tick_params(axis='x', labelcolor=color_r)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


dupli_graf()











