# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 23:09:27 2021

@author: aso
"""

import numpy as np
import matplotlib.pyplot as plt

from pyController.sensor import sensor

def closest_index(x, x_values):
    """
    Find the index of a value in array x_values that is clostest to x.

    Parameters
    ----------
    x : float or list of float
        A single value or a list of values to look for in x_values.
    x_values : ndarray or list
        The array with the values to compare to x.

    Returns
    -------
    ndarray
        The indices of the values in x_values that are clostest to x.

    """
    x_values = np.asarray(x_values)
    return np.argmin(np.abs(x-x_values[:, np.newaxis]), axis=0)

sampling_interval = 0.1  # in s
t_min = sampling_interval  # in s
t_max = 600  # in s

time_points = int((t_max-t_min)//sampling_interval+1)
time_values = np.linspace(t_min, t_max, time_points)

ph_sensor = sensor(7, start_real=7, k=0.03)

signal = np.full_like(time_values, 7)
signal[closest_index(50, time_values)[0]:closest_index(100, time_values)[0]] = 8
signal[closest_index(200, time_values)[0]:closest_index(400, time_values)[0]] = 8

for curr_t, curr_ph in zip(time_values, signal):
    ph_sensor.next_sensor_value(curr_ph, curr_t)

fig1, ax1 = plt.subplots()
ax1.plot(time_values, signal, label='real pH')
ax1.plot(ph_sensor.times, ph_sensor.sensor_values,
         label='delayed sensor response')
ax1.set_xlabel('time [s]')
ax1.set_ylabel('pH value')
ax1.legend()