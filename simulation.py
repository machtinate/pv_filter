# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 22:51:57 2023

@author: jmach
"""

import numpy as np
import matplotlib.pyplot as plt

from model import process_variable

dt = 0.1
m = process_variable(0.2, 0.7, 0., 0., dt)

t = np.arange(0, 30, dt)
op = np.where(t < 1, 0, 1)

pv = np.array([m.step(u) for u in op])

plt.plot(t,pv)
