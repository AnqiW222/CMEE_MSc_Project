#!/usr/bin/env python3

"""
This Python script, 'P_Model.py', models the phosphorus cycle in seagrass growth using a system of ordinary differential equations (ODEs). The model considers various forms of phosphorus, including Phosphorus in Organic Particulates (POP), Soluble Reactive Phosphorus (SRP), internal phosphorus in macroalgae (P_ma_int), and internal phosphorus in seagrass (P_R_int), and how they evolve over time.

The script contains three key functions:

1. 'P_model_sol': This function calculates the derivatives (rates of change) of POP, SRP, P_ma_int, and P_R_int at a given time. The rates are influenced by parameters like seagrass growth rate (R), temperature (T), and water column height (h).

2. 'P_model': This function computes the current values of POP, SRP, P_ma_int, and P_R_int for a given set of initial conditions and parameters. It employs the 'odeint' function from the scipy library to numerically solve the system of ODEs defined in 'P_model_sol'.

3. 'lambda_rsed_P': This function calculates a value based on a variable ORP_s using specific formulas. This value appears to be used in the calculation of the rate of change of SRP.

The model provides a detailed understanding of the phosphorus dynamics in seagrass ecosystems, which could be helpful in studying seagrass ecology and predicting seagrass dynamics under different environmental scenarios.
"""

__appname__ = 'P_model'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

import math
import numpy as np
from scipy.integrate import odeint

import Parameters

def P_model_sol(fourPvariable, t, params):
    """
    This function represents a system of four ordinary differential equations (ODEs) which are part of a larger model 
    simulating the phosphorus cycle in a marine or aquatic ecosystem. The function is designed to be used with an ODE solver.

    Parameters:
    fourPvariable (list or numpy array of four floats): The current state of the system. 
      Represents the values of POP (Phosphorus in Organic Particulates), SRP (Soluble Reactive Phosphorus), 
      P_ma_int (internal phosphorus of macroalgae) and P_R_int (internal phosphorus of seagrass).
    t (float): The current time. This input is not used in the function's calculations.
    params (list or numpy array of four floats): The params from growth_model_sol and Ni_model_sol

    Returns:
    list of four floats: Represents the current rates of change (i.e., the time derivatives) of POP, SRP, P_ma_int, and P_R_int.

    Note: The function uses several parameters and functions that are not defined within the function, 
    including lambda_rsed_P, B, R, T, and h. These should be defined or given values in the wider scope where 
    the function is used, or they could be passed as additional parameters to the function.
    """
    # Unpack the variables from the input array
    POP, SRP, P_ma_int, P_R_int = fourPvariable
    NH4,NO3,R,Nrint = params[0],params[1],params[2],params[3]


    # Define the first ODE of POP
    # constants params
    k_AP = 0.043
    k_OP = 4.45
    alpha_P_ma = 0.23 
    alpha_P_R = 0.11
    omega_m = 0.04
    tox = 0.11
    K_tox = 3
    SR = 0.08
    
    # Variable params
    k_PO = 1 # rate of PO
    DO = Parameters.DO 
    f_T = 26 # the value of f_ma_T or f_R_T; or the sum of f_ma_T and f_R_T
    T = Parameters.temperature  # example value, any value between 13 and 24°C
    
    # Need to be calculated from Macroalgae Dynamics
    omega_ma = omega_m + tox * math.exp(K_tox * (T - 26))    
    B = 0.8*Parameters.R
    
    # Need to be calculated from Seagrass Dynamics
    omega_R = SR * (0.098 + math.exp(-6.59 + 0.2217*T))
    R = Parameters.R 
    
    # Equation
    dPOPdt = -((k_AP * k_OP + k_PO * DO) / (k_OP + DO)) * f_T * POP + alpha_P_ma * B * omega_ma + alpha_P_R * R * omega_R
    
    #Define the second ODE of SRP
    # constants params
    vP_ma_max = 0.2
    vP_R_max = 0.1
    kP_ma = 0.0061
    kP_R = 0.0115
    QP_ma_max = 3.9
    QP_R_max = 1.2
    QP_ma_min = 1.1
    QP_R_min = 0.7
    f_v = 0.001
    
    # unknown params - all set as example values, should be set to the correct values
    h = 2 # Water depth, could be treat as an input, values between 1–6m 
    P_ma_int = Parameters.P_ma_int
    P_R_int = Parameters.P_R_int
    ORP_s = Parameters.ORP_s
    
    # uptake equation as Intermediate terms
    uptake_ma = B/h * vP_ma_max * SRP/(SRP + kP_ma) * (QP_ma_max - P_ma_int)/(QP_ma_max - QP_ma_min) * f_v
    uptake_R = R/h * vP_R_max * SRP/(SRP + kP_R) * (QP_R_max - P_R_int)/(QP_R_max - QP_R_min) * f_v
    
    # Equation
    dSRPdt = ((k_AP * k_OP + k_PO * DO) / (k_OP + DO)) * f_T * POP + lambda_rsed_P(ORP_s) - uptake_R - uptake_ma
    
    # Define the third ODE of P_ma_int
    # Constants params
    mu_max = 0.37
    K_oo = 0.4
    Ulv_ext = 0.001
    k_1 = 0.3
    K_I = 242
    T_opt = 24
    T_min = 8
    T_max = 26
    k_1 = 0.3
    k_4 = 0.01
    QN_min = 10
    QN_max = 40
    
    # Unknown params
    P_ma_int = Parameters.P_ma_int
    N_ma_int = 0.8*Parameters.Nrint
    I = 10 # the light intensity, varies by time of the day, weather, season, location and water depth
    
    # Intermediate terms
    gamma_1 = (1 / (T_opt - T_min)) * np.log((0.98 * (1 - k_1)) / (0.02 * k_1))
    gamma_2 = (1 / (T_max - T_min)) * np.log((0.98 * (1 - k_4)) / (0.02 * k_4))
    K_ext = K_oo + Ulv_ext * B/h
    f_ma_I = (1 / (K_ext * h)) * np.log((K_I + I) / (K_I + I * np.exp(-K_ext * h)))
    f_ma_T = ((k_1 * np.exp(gamma_1 * (T - T_min))) / (1 + k_1 * (np.exp(gamma_1 * (T - T_min)) - 1))) * ((k_4 * np.exp(gamma_2 * (T - T_min))) / (1 + k_4 * (np.exp(gamma_2 * (T - T_min)) - 1)))
    f_ma_N_int = (N_ma_int - QN_min) / (QN_max - QN_min)
    f_ma_P_int = (QP_ma_max - P_ma_int) / (QP_ma_max - QP_ma_min)

    # Need to be calculate from Macroalgae dynamics
    mu_ma = mu_max * f_ma_I * f_ma_T * f_ma_N_int * f_ma_P_int
    
    # Equation
    dP_ma_intdt = vP_ma_max * (SRP / (SRP + kP_ma)) * ((QP_ma_max - P_ma_int) / (QP_ma_max - QP_ma_min)) - mu_ma * P_ma_int
    
    #Define the fourth ODE of P_R_int
    # Constants params
    a = 20
    b = 2
    c = 5
    d = 2
    f_o = 14
    T_o = 26
    R_max = 250
    SL = 5
    N_min = 10
    M_cri = 15
    rho_max = 0.23
    
    # Unknown params
    N_R_int = Parameters.Nrint  # Example value, need to be change
    P_R_int = Parameters.P_R_int  # Example value, need to be change
    
    # Intermediate terms
    g_d = 1 - 1 / (1 + b * np.exp(a * (d - f_o)))
    f_R_T = 1 / ((1 + (T - (T_o / c)) ** 2) ** d)
    f_R_R = 1 - np.exp(-(R - R_max) / SL)
    f_R_N_int = (N_R_int - N_min) / (M_cri - N_min)
    f_R_P_int = (QP_R_max - P_R_int) / (QP_R_max - QP_R_min)
    
    # Need to be calculated from Seagrass dynamics
    rho = rho_max * g_d * f_R_T * f_R_R * f_R_N_int * f_R_P_int
    
    # Equation
    dP_R_intdt = vP_R_max * (SRP / (SRP + kP_R)) * ((QP_R_max - P_R_int) / (QP_R_max - QP_R_min)) - rho * P_R_int
    
    return [dPOPdt, dSRPdt, dP_ma_intdt, dP_R_intdt]


# This method calculates the current POP, SRP, P_ma_int, P_R_int using a given P_model
def P_model(a, b, c, d, e, f, g, h, now_t):
    POP, SRP, P_ma_int, P_R_int, R, Nrint, N_org, NH4 = a, b, c, d, e, f, g, h 

    init = [POP, SRP, P_ma_int, P_R_int]
    t = np.arange(0,100,1)  

    # defining the parameters for the differential equations
    params = [R, Nrint, N_org, NH4]
    # solve the ODE using scipy's odeint function
    result = odeint(P_model_sol,init,t,args=(params,))
    # split the results into separate variables
    sol_POP = result[:,0] 
    sol_SRP = result[:,1]
    sol_P_ma_int = result[:,2]
    sol_P_R_int = result[:,3]

    now_POP = sol_POP[np.argmin(np.abs(t - now_t))]
    now_SRP = sol_SRP[np.argmin(np.abs(t - now_t))]
    now_P_ma_int = sol_P_ma_int[np.argmin(np.abs(t - now_t))]
    now_P_R_int = sol_P_R_int[np.argmin(np.abs(t - now_t))]

    return now_POP, now_SRP, now_P_ma_int, now_P_R_int

def lambda_rsed_P(ORP_s):
    """
    Calculate a value based on ORP_s using specific formulas.
    
    This function uses a conditional to differentiate between two cases:
    when ORP_s is less than or equal to 0 and when ORP_s is greater than 0.
    
    Args:
        ORP_s (float): The input to the function. 
        Note: The meaning and unit of this input should be clarified.
    
    Returns:
        float: The output value.
    """
    # Constant parameter P_SRP
    # Note: The meaning and source of this parameter should be clarified.
    P_SRP = 13.7
    
    # Check the value of ORP_s and apply the appropriate formula
    if ORP_s <= 0:
        # Apply the formula for the case when ORP_s is less than or equal to 0
        # Note: The derivation and meaning of this formula should be clarified.
        return -((P_SRP / np.pi) * np.arctan(ORP_s / 4)) + P_SRP / 2
    else:
        # Apply the formula for the case when ORP_s is greater than 0
        # Note: The derivation and meaning of this formula should be clarified.
        return np.exp(-(ORP_s - (P_SRP / 2)))
