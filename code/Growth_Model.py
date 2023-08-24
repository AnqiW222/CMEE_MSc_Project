#!/usr/bin/env python3

"""
This Python script, 'Growth_Model.py', models the growth of seagrass using ordinary differential equations (ODEs). The model focuses on the seagrass's uptake of nitrogen and its rate of growth, considering various environmental and physiological factors.

The script contains two key functions:

1. 'Growth_model_sol': This function calculates the derivative (rate of change) of the seagrass's nitrogen internalization rate (Nrint) and growth rate (R) at a given time. The rates are influenced by parameters like the concentration of nitrogen sources (NH4 and NO3), the temperature, and the light conditions.

2. 'Growth_model': This function computes the current values of Nrint and R for a given set of initial conditions and parameters. It employs the 'odeint' function from the scipy library to numerically solve the system of ODEs defined in 'Growth_model_sol'.

The model provides a detailed understanding of how various factors affect seagrass growth, which could be helpful in studying seagrass ecology and predicting seagrass dynamics under different environmental scenarios.
"""

__appname__ = 'Growth_Model'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"


import math
import numpy as np
from scipy.integrate import odeint


def Growth_model_sol(R_and_Nrint, t, params):
    """
    Calculate the derivative of R and Nrint at time t.

    Args:
        R_and_Nrint (tuple of float): A tuple containing the current values of R and Nrint.
        t (float): The current time.
        params (list or numpy array of four floats): The params from Ni_model_sol 


    Returns:
        list: A list containing the derivatives of R and Nrint.
    """
    R, Nrint = R_and_Nrint
    # Params from Ni_model 
    NH4,NO3,R,Nrint = params[0],params[1],params[2],params[3]
    # Defining the first differential equation related to Nrint.
    v_R_NH4 = 0.1
    NH4 = 0.3
    K_NH4 = 0.13
    v_R_NO3 = 0.29
    NO3 = 1.2
    K_NO3 = 0.25
    p_N = 0.1
    
    dNrint_dt = v_R_NH4 * NH4 / (NH4 + K_NH4) + v_R_NO3 * NO3 /(NO3 + K_NO3) - p_N *Nrint 

    # Defining the second differential equation related to R.
    N_min = 10
    N_cri = 15
    f_Nrint = (Nrint - N_min)/(N_cri - N_min)
    
    R_max = 250
    SL = 5
    f_R = 1- math.exp(-(R-R_max)/SL)
    
    T = 12
    To = 26
    c = 1
    d = 3
    fR_T = 1/(1+(((T-To)/c)**2)**d)
    
    b = 2
    a = 5
    fo =14
    g_d = 1 - 1/(1+ b* math.exp(a*(fo - d)))
    
    p_max = 1
    p = p_max * g_d * fR_T * f_Nrint * f_R
    
    SR = 0.041
    omega_R = SR * (0.098 + math.exp(-6.59 + 0.2217*T))
    
    dR_dt = (p - omega_R)*R

    # Total system of differential equations
    du_dt = [dR_dt, dNrint_dt]

    return du_dt



# This method calculates the current R and Nrint using a given Growth_model
def Growth_model(a,b,c,d,now_t):
    # set class variables according to the passed parameters
    NH4,NO3,R,Nrint = a,b,c,d
    
    # initial conditions for ODE solver
    growth_init = [R,Nrint]
    # generate a range of time steps
    t = np.linspace(0, now_t, num=now_t+1)  # Generate an array of time points   
    # define parameters for the ODE
    params = [NH4,NO3,R,Nrint]
    # solve the ODE using scipy's odeint function
    result =odeint(Growth_model_sol,growth_init,t,args=(params,)) 
    # split the results into separate variables
    sol_R = result[:,0]
    sol_Nrint = result[:,1]
    # find the current values by taking the value at the closest time step to now_t
    now_R = sol_R[np.argmin(np.abs(t - now_t))]  
    now_Nrint = sol_Nrint[np.argmin(np.abs(t - now_t))]  
    return now_R,now_Nrint



