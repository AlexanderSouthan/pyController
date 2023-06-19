# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 16:41:51 2021

@author: aso
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz

from pyController.pid_control import pid_control
from pyController.on_off_control import on_off_control
from pyController.sensor import sensor

# This example simulates the response of a PID controller when used for keeping
# the pH of a solution constant by adding a base. This is necessary because
# an acid is added with a constant flow rate.

# Define how often the pH sensor collects a signal
sampling_interval = 0.1  # in s
t_min = sampling_interval  # in s
t_max = 2000  # in s

# Define the concentrations of acid and base, the starting volume of the acid
# and the flow rate of the acid
c_acid = 0.01  # in mol/L
c_base = 0.01  # in mol/L
v0 = 0.2  # in L
flow_rate_acid = 0.001  # in L/s

# Define the time points for sensor readouts
time_points = int((t_max-t_min)//sampling_interval+1)
time_values = np.linspace(t_min, t_max, time_points)

# Calculte the added acid amounts for all time points of the simulation
acid_flow = np.full_like(time_values, flow_rate_acid)
acid_vol = cumtrapz(acid_flow, x=time_values, initial=0)
acid_amount = acid_vol * c_acid + 1E-7 * (v0 + acid_vol)  # strongly simplified model

# Set up PID and on/off controller for a set point of 8
pid = pid_control(8, 0.001, 0.00002, 0.005, response_limits=[0, None])
on_off = on_off_control(8, 'lower_limit', 0.002)

# Set up pH sensor as a relatively slow sensor
ph_sensor = {'pid': sensor(7, start_real=7, k=0.05),
             'onoff': sensor(7, start_real=7, k=0.05)}

# initialize lists which collect the simulation data for PID and on/off control
base_flow = {'pid': [0], 'onoff': [0]}
base_vol = {'pid': [0], 'onoff': [0]}
base_amount = {'pid': [0], 'onoff': [0]}
acid_balance = {'pid': [acid_amount[0]], 'onoff': [acid_amount[0]]}
ph = {'pid': [-math.log10(acid_amount[0]/(v0))],
      'onoff': [-math.log10(acid_amount[0]/(v0))]}

# Calulate pH values and the controller responses for all time points
for ii, (curr_time, curr_acid_vol, curr_acid_amount) in enumerate(
        zip(time_values[1:], acid_vol[1:], acid_amount[1:])):

    for curr_key in ['pid', 'onoff']:
        if curr_key == 'pid':
            base_flow[curr_key].append(
                pid.calc_response(ph_sensor[curr_key].sensor_values[-1],
                                  curr_time, d_window=5))
        else:
            base_flow[curr_key].append(
                on_off.calc_response(ph_sensor[curr_key].sensor_values[-1],
                                     curr_time))

        base_vol[curr_key].append(
            base_vol[curr_key][-1] + base_flow[curr_key][-1] *
            sampling_interval)
        base_amount[curr_key].append(base_vol[curr_key][-1] * c_base)
        acid_balance[curr_key].append(
            curr_acid_amount-base_amount[curr_key][-1])
    
        total_vol = v0 + base_vol[curr_key][-1]
    
        if acid_balance[curr_key][-1] >= 0:
            ph[curr_key].append(
                -math.log10((acid_balance[curr_key][-1]/total_vol)))
        else:
            ph[curr_key].append(
                14 + math.log10(-acid_balance[curr_key][-1]/total_vol))
        ph_sensor[curr_key].next_sensor_value(ph[curr_key][-1], curr_time)


# Plot the results of the pH value over time with PID and on/off control
fig1, ax1 = plt.subplots(2)
ax1[0].plot(time_values, ph['pid'], label='real pH PID control')
ax1[0].plot(ph_sensor['pid'].times, ph_sensor['pid'].sensor_values,
            label='measured pH PID control')
ax1[1].plot(time_values, ph['onoff'], label='real pH on/off control')
ax1[1].plot(ph_sensor['onoff'].times, ph_sensor['onoff'].sensor_values,
            label='measured pH on/off control')
ax1[0].legend()
ax1[1].legend()
ax1[0].set_xlabel('time [s]')
ax1[0].set_ylabel('pH')
ax1[1].set_xlabel('time [s]')
ax1[1].set_ylabel('pH')
plt.tight_layout()
