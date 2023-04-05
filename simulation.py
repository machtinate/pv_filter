# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 22:51:57 2023

@author: jmach

A short script to demonstrate configuration of the PV and filter objects and a
simulation over a defined time range in response to a control input step change.
"""

import numpy as np
import matplotlib.pyplot as plt

from model import process_variable, fo_filter

# configure the sampling time constant
dt = 0.05

# configure the model and filter objects, note that the cutoff frequency for 
# the filter should be chosen betwen the implied noise frequency that is 
# dependent on the sample time constant e.g. w_noise = 1/dt
m = process_variable(0.3, 0.5, np.array([[0.], [0.]]), 0., dt, 0.1)
f = fo_filter(1, 0, dt)

# create a time range and simulate a step change in control input (op) @ 5 sec
t = np.arange(0, 30, dt)
op = np.where(t < 5, 0, 1)

# first generate the noisy pv from the model, then apply the filter over it
pv = np.array([m.step(u) for u in op], dtype=object)
pv_filt = np.array([f.filt(v) for v in pv], dtype=object)

# plot the raw signal and the filtered signal over time
plt.plot(t, op, label='Control input')
plt.plot(t, pv, label='Noisy signal')
plt.plot(t, pv_filt, label='Filtered signal')
plt.title('Process Variable Filter Simulation')
plt.xlabel('Time [s]')
plt.ylabel('PV')
plt.legend()
