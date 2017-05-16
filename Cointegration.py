#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys

reload(sys)
sys.setdefaultencoding('utf8')

"""
Computer Engineering Section
The Military Institute of Engineering
Rio de Janeiro, Brazil
June 28, 2016
author: Elias Gonçalves
email: esgoncalves@ime.eb.br
"""

import pandas as pd
import statsmodels.api as sm
import numpy as np

path_coi = 'output/cointegration/'
path_converted = 'output/converted/'


class Cointegration:
    """
    Cointegration test and others functions of linear regressions
    yi and yj are the dependents variables. It is what we want to forecast.
    x is the independent variable. It is the cause of forecast
    df is the Vector which have all data from flight
    With adaptation from:
    http://nbviewer.jupyter.org/github/mapsa/seminario-doc-2014/blob/master/cointegration-example.ipynb
    """

    def __init__(self):
        pass

    def get_variance_and_standard_deviation(self, lst, population=True):
        """
        Variance and Standard Deviation
        Thanks http://codeselfstudy.com/blogs/how-to-calculate-standard-deviation-in-python
        -----------
        :param lst: a list of numbers
        :return variance:
        :return sd:
        """
        from math import sqrt
        num_items = len(lst)
        mean = sum(lst) / num_items
        differences = [x - mean for x in lst]
        sq_differences = [d ** 2 for d in differences]
        ssd = sum(sq_differences)

        if population is True:
            variance = ssd / num_items
        else:
            variance = ssd / (num_items - 1)
        sd = sqrt(variance)
        return variance, sd

    def ADF(self, v, crit='5%', max_d=6, reg='nc', autolag='AIC'):
        """
        The Augmented Dickey-Fuller test can be used to test for a unit root in a
        univariate process in the presence of serial correlation.
        -----------
        :param v: ndarray matrix, residuals matrix
        :return bool: true if v pass the test
        """
        from statsmodels.tsa.stattools import adfuller
        boolean = False
        adf = adfuller(v, max_d, reg, autolag)

        print(' -> P-value: ', adf[0], '\n -> Significance level: ', adf[4])

        if adf[0] < adf[4][crit]:  # if Tau < crit value reject null hypothesis, not has unit root, is stationary
            pass
        else:
            boolean = True  # accept null hypothesis, has unit root is not stationary
        return boolean

    def get_johansen(self, y, p):
        """
        Johansen test get the cointegration vectors at 95% level of significance
        given by the trace statistic test.
        -----------
        :param y: ndarray matrix, residuals matrix
        :param p: detrend data
        :return jres: Johansen result object
        """
        from statsmodels.tsa.johansen import coint_johansen
        N, l = y.shape
        jres = coint_johansen(y, 0, p)

        trstat = jres.lr1  # trace statistic
        print('\n -> Trace statistic: ', trstat)

        tsignf = jres.cvt  # critical values
        print(' -> Critical values: ', tsignf)

        for i in range(l):
            # print('trstat[', i, '] > tsignf[', i, ', 1]?')
            # print(trstat[i], tsignf[i, 1])
            if trstat[i] > tsignf[i, 1]:  # 0: 90%  1:95% 2: 99%
                r = i + 1

        jres.r = r
        jres.evecr = jres.evec[:, :r]
        # print('Cointegration vectors: ', jres.evec[:, :r])
        return jres

    def calculate_regression(self, y, X):
        """
        Regression
        The main reference paper for that is:
        http://www.sciencedirect.com/science/article/pii/S1000936115000849
        -----------
        :param y: Dependent variable
        :param X: Independents variables
        :return e: The residual error
        :return yi_hat: A vector predicted
        """

        # -----------
        # 1: Regression
        # a) Equation 7 - Linear combination. Calculate the estimated values
        est = sm.OLS(y, sm.add_constant(X)).fit()

        # b) Equation 6 - Residual error: e = |yi - ŷi| (White noise)
        e = est.resid

        # c) Predicted series
        y_hat = est.predict()

        # -----------
        # 2: Summarize
        # print (est.summary())

        # -----------
        # 3: Return values
        return e, y_hat

    def test(self, s1, s2, ti, level=1):
        """
        Cointegration test
        -----------
        :param s1: first time series (accelerometer[x,y,z] or gyrometer[x,y,z])
        :param s2: second time series (accelerometer[x,y,z] or gyrometer[x,y,z])
        :param ti: time (seconds or microseconds)
        :return hat: estimated vector at time (accelerometer[x,y,z] or gyrometer[x,y,z])
        :return sd: standard deviation of error
        """
        from Plot import Plot

        # Create the process. We don't know the properties of process. I(1), I(0)???
        # Obs: for more levels implements elif and else and change the names in 'data' variable
        if 1 <= level <= 6:
            data = {'IMU 1': s1, 'IMU 2': s2}
        else:
            data = {'Data 1': s1, 'Data 2': s2}

        # Create the process
        y = pd.DataFrame(index=ti, data=data)

        # Initial Plots
        p = Plot()

        if level == 1:  # Acceleration in x
            p.visualize_dataframe(y, 'Filtered acceleration X axis', str(path_converted + 'true_ax.eps'),
                                  'Acceleration [g]')

        elif level == 2:  # Acceleration in y
            p.visualize_dataframe(y, 'Filtered acceleration Y axis', str(path_converted + 'true_ay.eps'),
                                  'Acceleration [g]')

        elif level == 3:  # Acceleration in z
            p.visualize_dataframe(y, 'Filtered acceleration Z axis', str(path_converted + 'true_az.eps'),
                                  'Acceleration [g]')

        elif level == 4:  # Gyroscope in x
            p.visualize_dataframe(y, 'Filtered angular speed X axis', str(path_converted + 'true_gx.eps'),
                                  'Angular speed [$deg/s$]')

        elif level == 5:  # Gyroscope in y
            p.visualize_dataframe(y, 'Filtered angular speed Y axis', str(path_converted + 'true_gy.eps'),
                                  'Angular speed [$deg/s$]')

        elif level == 6:  # Gyroscope in z
            p.visualize_dataframe(y, 'Filtered angular speed Z axis', str(path_converted + 'true_gz.eps'),
                                  'Angular speed [$deg/s$]')

        # If s1 and s2 are both non-stationary [I(1)], there exists a linear combination of them which is stationary
        if self.ADF(s1) and self.ADF(s2):  # not stationary
            # Johansen
            l = 1  # Order of auto regression
            jres = self.get_johansen(y, l)
            print('\nCointegration vectors: ', jres.r)
            v0 = jres.evecr[:, 0]
            v1 = jres.evecr[:, 1]
            print(' -> First vector: ', v0)
            print(' -> Second vector: ', v1)
            s1_correct = np.dot(y.as_matrix(), v0)  # stationary, after apply vector error correction
            s2_correct = np.dot(y.as_matrix(), v1)  # stationary, after apply vector error correction
            xt, yt = s1_correct, s2_correct  # Now, the time series are stationary
            # e, hat = self.calculate_regression(s1_correct, s2_correct)

            #  Or by mean:
            hat = (s1_correct + s2_correct) / 2
            e = (s1_correct + s2_correct) - hat
        else:
            xt, yt = s1, s2
            e, hat = self.calculate_regression(s1, s2)

        # Calculate Variance and Standard Deviation of error
        var, sd = self.get_variance_and_standard_deviation(e)

        # Plot
        if level == 1:  # Acceleration in x
            p.errors_cointegration(xt, yt, hat, e, ti, str(path_coi + 'unit_root_ax.eps'),
                                   'Stationary acceleration X axis', 'Acceleration [g]')

        elif level == 2:  # Acceleration in y
            p.errors_cointegration(xt, yt, hat, e, ti, str(path_coi + 'unit_root_ay.eps'),
                                   'Stationary acceleration Y axis', 'Acceleration [g]')

        elif level == 3:  # Acceleration in z
            p.errors_cointegration(xt, yt, hat, e, ti, str(path_coi + 'unit_root_az.eps'),
                                   'Stationary acceleration Z axis', 'Acceleration [g]')

        elif level == 4:  # Gyroscope in x
            p.errors_cointegration(xt, yt, hat, e, ti, str(path_coi + 'unit_root_gx.eps'),
                                   'Stationary angular speed X axis', 'Angular speed [$deg/s$]')

        elif level == 5:  # Gyroscope in y
            p.errors_cointegration(xt, yt, hat, e, ti, str(path_coi + 'unit_root_gy.eps'),
                                   'Stationary angular speed Y axis', 'Angular speed [$deg/s$]')

        elif level == 6:  # Gyroscope in z
            p.errors_cointegration(xt, yt, hat, e, ti, str(path_coi + 'unit_root_gz.eps'),
                                   'Stationary angular speed Z axis', 'Angular speed [$deg/s$]')
        return sd, hat
