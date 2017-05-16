#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Computer Engineering Section
The Military Institute of Engineering
Rio de Janeiro, Brazil
June 28, 2016
author: Elias Gonçalves
email: esgoncalves@ime.eb.br
"""

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import sys

reload(sys)
sys.setdefaultencoding('utf8')

class Plot:

    def __init__(self):
        pass
        # print "\nPlot is running."

    # Filter Plot
    def vizualize_raw_data(self, ti, s1, s2, title, name):
        plt.title(title)
        plt.plot(ti, s1, 'b', label='IMU1')
        plt.plot(ti, s2, 'g', label='IMU2')
        plt.ylabel('Data [raw]')
        plt.xlabel('Time [s]')
        plt.xlim(ti[0], ti[len(ti) - 1])
        plt.legend(loc='best')

        plt.savefig(name)
        plt.close()

    # Cointegration Plots
    def visualize_dataframe(self, y, title, name, label):
        y.plot()
        plt.title(title)
        plt.ylabel(label)
        plt.xlabel('Time [s]')
        plt.legend(loc='best')

        plt.savefig(name)
        plt.close()

    def errors_cointegration(self, yi, yj, yi_hat, e, ti, name, title, label):
        plt.subplot(2, 1, 1)
        plt.title(title)
        plt.plot(ti, yi, 'b', label='IMU1')
        plt.plot(ti, yj, 'g', label='IMU2')
        plt.plot(ti, yi_hat, 'm', label='Estimated')
        plt.ylabel(label)
        plt.xlim(ti[0], ti[len(ti) - 1])
        plt.legend(loc='best')

        plt.subplot(2, 1, 2)
        plt.plot(ti, e, 'r', label='Residual')
        plt.ylabel(label)
        plt.xlabel('Time [s]')
        plt.xlim(ti[0], ti[len(ti) - 3])
        plt.legend(loc='best')

        plt.savefig(name)
        plt.close()
