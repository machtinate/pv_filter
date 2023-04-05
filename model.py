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
    - It is assumed that the data to be filtered has been collected and stored
    prior to filtering. That is, the filter is not being applied in realtime on
    the PV, but instead as a batch operation on a set collected data.

"""

import numpy as np

class process_variable(object):
    """
    A simulated process variable (PV).
    
    Defined as a linear time invariant (LTI) system with second order dynamics.
    Zeta and wn (natural frequency) can be adjusted to simulate different
    dynamics.
    
    After initial conditions are configured on instantiation, control inputs 
    can be passed through the step() function to move the process around. Noise
    is added to the output of the system, configurable with the sigma variable.
    """
    def __init__(self, zeta, wn, x_0, u_0, dt, sigma):
        """
        Parameters
        ----------
        zeta : float
            Damping factor.
                - overdamped -> zeta > 1
                - critically damped -> zeta = 1
                - under damped -> 0 < zeta < 1
        wn : float
            Natural frequency. The larger the number, the faster the system
            oscillates in time.
        x_0 : np.array([float])
            Initial state. 2x1 numpy vector. First entry is zeroeth order state
            variable (e.g. displacement), second entry is the first order
            state variable (e.g. velocity).
        u_0 : float
            Control input. No gain configurable gain in this system so the 
            response is 1-to-1.
        dt : float
            Time constant. Time lapse between discrete samples of the system.
        sigma : float
            Noise standard deviation. Std dev of measurement noise.

        Returns
        -------
        None.

        """
        # initial conditions
        self.x = x_0
        self.u = u_0
        
        # dynamic and noise variables
        self.wn = wn
        self.sigma = sigma
        
        # initial output
        self.y = np.dot(np.array([wn**2, 0.]),  x_0)
        
        # discretized process model
        self.Ad = np.eye(2) + np.array([[0., 1.], [-(wn**2.), (-2.)*zeta*wn]]) * dt
        self.Bd = np.array([[0.], [1.]]) * dt
        
    def step(self, u):
        """        
        Parameters
        ----------
        u : float
            Control input. 1-to-1 gain, applied to the second order state
            rate of change (e.g. acceleration).

        Returns
        -------
        y : float
            Process output. In this case, defined as the first order state
            variable (e.g. displacement). Gaussian noise is applied with
            standard deviation defined by sigma variable.

        """
        # apply the state update
        self.x = np.dot(self.Ad, self.x) + (self.Bd * u)
        
        # extract the new output
        self.y = np.dot(np.array([self.wn**2, 0.]),  self.x) + np.random.normal(0, self.sigma)
        
        return self.y

        
class fo_filter(object):
    """
    A first order low pass filter.
    
    The cutoff frequency is configurable at instantiation.
    
    For a discrete system, a low pass filter is equivalently modelled by an
    exponentially weighted moving average algorithm. The smoothing factor is 
    alpha, calculated by the relationship in the init function.
    """
    def __init__(self, wc, z_0, dt):
        """
        Parameters
        ----------
        wc : float
            Cutoff frequency. Defines the frequency above which the signal is 
            attenuated.
        z_0 : float
            Initial filter state. Initial state of the variable to be filtered.
        dt : float
            Filter time constant. The time lapse between discrete samples of 
            the variable to be filtered. Should be the same as the model.

        Returns
        -------
        None.

        """
        # initialize filter state
        self.z = z_0
        
        # calculate the smoothing factor for the corresponding cutoff frequency
        self.alpha = dt / ((1/wc) + dt)
        
        # step counter
        self.i = 0
        
    def filt(self, data):
        """
        Parameters
        ----------
        data : float
            New data point for the filter. Assumed to be the next piece of
            information passed to the filtering algorithm in the time sequence.

        Returns
        -------
        z : float
            Filtered state. The filtered state after being passed through the
            low-pass algorithm.

        """
        if self.i == 0:
            # skip the first time step, corresponds with the intitial condition
            self.i += 1
        else:
            # apply the exponentially weighted smoothing algorithm
            self.z = self.alpha * data + (1-self.alpha) * self.z
            self.i += 1
        return self.z

