#!/usr/bin/env python3

"""
This Python script, 'Ni_Model.py', models the nitrogen cycle in seagrass growth using a system of ordinary differential equations (ODEs). The model considers various forms of nitrogen, including organic nitrogen (N_org), ammonia (NH4), nitrite (NO2), and nitrate (NO3), and how they evolve over time.

The script contains two key functions:

1. 'Ni_model_sol': This function calculates the derivatives (rates of change) of N_org, NH4, NO2, and NO3 at a given time. The rates are influenced by parameters like seagrass growth rate (R), temperature (T), and water column height (h).

2. 'Ni_model': This function computes the current values of N_org, NH4, NO2, and NO3 for a given set of initial conditions and parameters. It employs the 'odeint' function from the scipy library to numerically solve the system of ODEs defined in 'Ni_model_sol'.

The model provides a detailed understanding of the nitrogen dynamics in seagrass ecosystems, which could be helpful in studying seagrass ecology and predicting seagrass dynamics under different environmental scenarios.
"""

__appname__ = 'Ni_model'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

import math
import numpy as np
from scipy.integrate import odeint

import Parameters

# This method calculates the current N_org, NH4, NO2, NO3 using a given Ni_model
def Ni_model(a,b,c,d,e,now_t):
    # set class variables according to the passed parameters
    R,N_org,NH4,NO2,NO3 = a,b,c,d,e

    # initial conditions for ODE solver
    init=[N_org,NH4,NO2,NO3]
    # generate a range of time steps
    t = np.arange(0,100,1)   
    # define parameters for the ODE
    params = R
    # solve the ODE using scipy's odeint function
    result =odeint(Ni_model_sol,init,t,args=(params,))
    # split the results into separate variables
    sol_N_org = result[:,0] 
    sol_NH4 = result[:,1]
    sol_NO2 = result[:,2]
    sol_NO3 = result[:,3]
    # find the current values by taking the value at the closest time step to now_t
    now_N_org = sol_N_org[np.argmin(np.abs(t - now_t))]
    now_NH4 = sol_NH4[np.argmin(np.abs(t - now_t))]
    now_NO2 = sol_NO2[np.argmin(np.abs(t - now_t))]
    now_NO3 = sol_NO3[np.argmin(np.abs(t - now_t))]
    return now_N_org,now_NH4,now_NO2,now_NO3

# Need to be optimised with initial value
def Ni_model_sol(fourNivariable,t, params):
    """
    Calculate the derivatives of N_org, NH4, NO2, and NO3 at time t according to specified ODEs.

    Args:
        fourNivariable (tuple of float): A tuple containing the current values of N_org, NH4, NO2, and NO3.
        t (float): The current time.
        params (list or numpy array of one floats): The params from growth_model_sol


    Returns:
        list: A list containing the derivatives of N_org, NH4, NO2, and NO3.
    """
    
    # Defining the first ODE for N_org.
    N_org, NH4, NO2, NO3 = fourNivariable
    R = params
    
    # Need initial values
    DO = Parameters.DO
    T = Parameters.temperature
    
    # Constants params
    f_v = 0.001
    w_a1 = 0.43
    f_deta1 = 70
    w_a2 = 0.23
    f_deta2 = 60
    u_max04 = 0.045
    omega_m = 0.03
    tox= 0.11
    K_tox= 3
    
    # Need to be calculated from Macroalgae dynamics
    omega_ma = omega_m + tox * math.exp (K_tox * (T - 26))
    B = 0.8*Parameters.R

    # Need to be calculated from Seagrass dynamics
    omega_R = 0.041 * (0.098 + math.exp(-6.59 + 0.2217 * T))
    R = Parameters.R
    
    # Unknow params - need to be change
    h = 2 # Water depth, could be treat as an input, values between 1–6m
    
    # Equation
    dNorgdt = f_v * w_a1 * f_deta1 * omega_ma * B/h + f_v * w_a2 * f_deta2 * omega_R * R/h - u_max04 * N_org
    
    # Defining the second ODE for NH4.
    # Unknow params - need to be change
    N_int = Parameters.N_org
    v_R_NH4 = 0.01
    v_ma_NH = 0.005
    
    # Constants params
    u_max42 = 0.011
    K_O = 1.0
    V = 1.066 
    K_NH = 0.5
    QN_min = 10
    QN_max = 40
    K_NH4 = 0.13
    
    # Uptakes
    up_NH4a1 = B/h * v_ma_NH * NH4/(NH4 + K_NH) * (N_int - QN_min)/(QN_max - QN_min) * f_v
    up_NH4a2 = R/h * v_R_NH4 * NH4/(NH4 + K_NH4) * f_v
    
    median_1 = J_rsed4(Parameters.ORP_s)
    dNH4dt = u_max04 * N_org + median_1 - up_NH4a1 - up_NH4a2 - u_max42 * DO/(DO + K_O) * V * (T - 20) * NH4
    
    # Defining the third ODE for NO2.
    u_max23 = 0.046
    dNO2dt = u_max42 * DO/(DO + K_O) * V * (T - 20) * NH4 - u_max23 * DO/(DO + K_O) * V * (T - 20) * NO2
    
    # Defining the fourth ODE for NO3.
    # Constants params
    u_denit = 0.37
    K_NO = 0.25
    K_NO3 = 0.25
    K_O3 = 0.1
    
    # Unknown params - need to be change
    v_ma_NO = 0.03
    v_R_NO3 = 0.035
    
    # Uptakes
    up_NO3a1 = B/h * v_ma_NO * NO3/(NO3 + K_NO) * (N_int - QN_min)/(QN_max - QN_min) * f_v
    up_NO3a2 = R/h * v_R_NO3 * NO3/(NO3 + K_NO3) * f_v
    
    dNO3dt = u_max23 * DO/(DO + K_O) * V * (T - 20) * NO2 - u_denit * K_O3/(DO + K_O3) * V * (T - 20) * NO3 - up_NO3a1 - up_NO3a2 + J_rsed3(Parameters.ORP_s)
    
    # Return the list of derivatives
    return [dNorgdt,dNH4dt,dNO2dt,dNO3dt]

def J_rsed4(ORP_s):
    """
    Computes the sediment flux of ammonia (NH4) based on the oxidation-reduction potential (ORP).
    
    Args:
        ORP_s (float): The oxidation-reduction potential.
    
    Returns:
        float: The sediment flux of ammonia.
    """
    P_NH4 = 180
    if ORP_s <= 0:
        # When ORP is less than or equal to 0, the sediment flux is calculated with an arctan-based formula.
        return -((P_NH4 / np.pi) * np.arctan(ORP_s / 4)) + P_NH4 / 2
    else:
        # When ORP is greater than 0, the sediment flux is calculated with an exponential-based formula.
        return np.exp(-(ORP_s - (P_NH4 / 2)))
    
    
def J_rsed3(ORP_s):
    """
    Computes the sediment flux of nitrate (NO3) based on the oxidation-reduction potential (ORP).
    
    Args:
        ORP_s (float): The oxidation-reduction potential.
    
    Returns:
        float: The sediment flux of nitrate.
    """
    P_NO3 = 31.3
    if ORP_s <= 0:
        # When ORP is less than or equal to 0, the sediment flux is calculated with an arctan-based formula.
        return -((P_NO3 / np.pi) * np.arctan(ORP_s / 4)) + P_NO3 / 2
    else:
        # When ORP is greater than 0, the sediment flux is calculated with an exponential-based formula.
        return np.exp(-(ORP_s - (P_NO3 / 2)))