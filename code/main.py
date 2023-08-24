#!/usr/bin/env python3

"""
This Python script, 'main.py', serves as the primary entry point for running a Cellular Automaton (CA) model to simulate seagrass growth. The script coordinates the various components of the model and visualizes the final state of the simulation.

The script contains a main execution block that performs the following tasks:

1. Sets the number of simulation steps (weeks in this context).

2. Collects user inputs for the initial values of parameters R and Nrint using the 'User_Input' function.

3. Creates a new instance of the CA model with a specified grid size.

4. Initializes the grid with initial conditions using the 'initialize_grid' method of the CA instance.

5. Runs the simulation for a defined number of steps using the 'evolution' method of the CA instance and prints the final state of the grid.

This script integrates the CA model, the growth model, and the parameters to run a comprehensive simulation of seagrass growth over time. It is designed to be flexible and can be easily adapted to accommodate different grid sizes, initial conditions, and numbers of simulation steps.
"""

__appname__ = 'main'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

import numpy as np
import matplotlib.pyplot as plt 

import Parameters
import CA_Model
import User_Input

num_of_weeks = 260 # simulation time
if __name__ == "__main__":
    
    
    #define paramters
    # Mock data 1
    # User_Input.User_Input(Nrint = 0.02, N_org = 28.49, NH4 = 0.78, NO2 = 0.4, NO3 = 1.36, POP = 4.66, SRP = 1.56, R = 66.1, P_ma_int = 0.01, P_R_int = 0.04, GROWTH_RATE = 1.02, germination_rate = 3.55, reproduction_rate = 7.62, temperature = 19.96, oxygen = 8.2, ORP_s = 127.66, DO = 5.13)
    # Mock data 2
    # User_Input(N_IDX = None, P_IDX = None, C_IDX = None, CB_IDX = None, NB_IDX = None, PB_IDX = None, LIGHT_IDX = None, R_IDX = None, G_IDX = None, M_IDX = None, R = 72.02, Nrint = 2.8, N_org = 48.11, NH4 = 0.01, NO2 = 0.03, NO3 = 2.77, POP = 1.06, SRP = 1.94, P_ma_int = 0.07, P_R_int = 0.06)
    # Mock data 3
    # User_Input(N_IDX = None, P_IDX = None, C_IDX = None, CB_IDX = None, NB_IDX = None, PB_IDX = None, LIGHT_IDX = None, R_IDX = None, G_IDX = None, M_IDX = None, R = 65.48, Nrint = 4.36, N_org = 15.88, NH4 = 0.85, NO2 = 0.43, NO3 = 4.18, POP = 1.24, SRP = 3.4, P_ma_int = 0.04, P_R_int = 0.01)

    ca = CA_Model.CA(100, 100) # Create a new CA with width and height of 100
    ca.initialize_grid()  # Initialize the grid
    final_state = ca.evolution(num_of_weeks)  # Run the simulation for 50 steps
    print(final_state)
    # CA_Model.PlotResult(final_state,52)
    # Save the final_state matrix to a CSV file
    np.savetxt("ClGS_final_state.csv", final_state, delimiter=",")
    
