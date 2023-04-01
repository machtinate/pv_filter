# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 21:50:10 2023

@author: jmacht

Purpose: 
    Provide first order filtering for a continuous signal, or Process 
    Variable (PV).

Assumptions:
    - A 'first order' filter implies that there is one pole to place in the 
    theoretical transfer function for the system. This could act in one of two
    ways:
        - LOW PASS - attenuating information above a certain cutoff frequency
        - HIGH PASS - attenuating information below a certaing cutoff frequency
    - This said, given the PV is very likely a low frequency signal, and a 
    'first order filter' is usually just referring to a low pass filter, the
    digital filter in this case will be configured to only provide LOW PASS
    capabilities.
    - While the PV may be a continuous signal, we are assuming here that it is
    sampled in a discrete fashion. As such, the filter is designed as a
    discrete filter to emulate the characteristics of it's continuous
    counterpart.
    - It is assumed that the 
    - It is assumed that the data to be filtered has been collected and stored
    prior to filtering. That is, the filter is not being applied in realtime on
    the PV, but instead as a batch operation on a set collected data.

"""

import numpy as np

class process_variable(object):
    
    def __init__(self, zeta, wn, x_0, u_0, dt, sigma):
        # initial conditions
        self.x = x_0
        self.u = u_0
        self.wn = wn
        self.sigma = sigma
        self.y = np.dot(np.array([wn**2, 0.]),  x_0)
        
        # discretized process model
        self.Ad = np.eye(2) + np.array([[0., 1.], [-(wn**2.), (-2.)*zeta*wn]]) * dt
        self.Bd = np.array([[0.], [1.]]) * dt
        
    def step(self, u):
        self.x = np.dot(self.Ad, self.x) + (self.Bd * u)
        self.y = np.dot(np.array([self.wn**2, 0.]),  self.x) + np.random.normal(0, self.sigma)
        return self.y

        
class fo_filter(object):
    def __init__(self, wc, z_0, dt):
        self.z = z_0
        self.alpha = dt / ((1/wc) + dt)
        
        # step counter
        self.i = 0
        
    def filt(self, data):
        if self.i == 0:
            self.i += 1
        else:
            self.z = self.alpha * data + (1-self.alpha) * self.z
            self.i += 1
        return self.z

