# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 22:51:57 2023

@author: jmach
"""

import numpy as np
import matplotlib.pyplot as plt

from model import process_variable, fo_filter

dt = 0.1
m = process_variable(0.2, 0.7, 0., 0., dt, 0.05)
f = fo_filter(30, 0, dt)

t = np.arange(0, 30, dt)
op = np.where(t < 1, 0, 1)

pv = np.array([m.step(u) for u in op])

pv_filt = np.array([f.filt(v) for v in pv])

plt.plot(t, pv)
plt.plot(t, pv_filt)
