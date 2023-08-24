#!/usr/bin/env python3

"""
This Python script contains functions for simulating the growth and nutrient interaction of seagrass in a 2D grid environment. It uses several models to simulate different aspects of seagrass life, including growth and nitrogen and phosphorus interactions.

The script contains two main functions:

1. `Have_seagrass`: This function determines the presence of seagrass in each cell of a given grid. It receives a 3D numpy array representing the simulation grid, where each cell is a 1D array representing the cell's state. A cell with all elements equal to zero is considered to be without seagrass. The function returns a 2D numpy array of the same dimensions as the input grid, where each element corresponds to a cell in the grid. A value of 1 indicates the presence of seagrass, while 0 indicates its absence.

2. `one_cell_run`: This function runs a single time step for a cell in the simulation. It receives a time point (`t`) and a `grid` representing the current state of the system. The function first checks whether `t` is equal to 0. If so, it initializes the system using the `Growth_Model`, `Ni_Model`, and `P_Model`. If `t` is not 0, it checks whether there is any seagrass in the grid. If there is no seagrass, the function simply returns the original `grid`. If there is seagrass, the function performs one step of the simulation by calling the `Growth_Model`, `Ni_Model`, and `P_Model` again.

The overall program is designed for simulating how seagrass might grow and interact with its environment over time, considering factors like nutrients (specifically nitrogen and phosphorus) and growth rates.
"""

__appname__ = 'Cell'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

import numpy as np

import Growth_Model
import Parameters
import Ni_Model
import P_Model

num_of_weeks = 52
def Have_seagrass(state, height, width):
    """
    This function determines the presence of seagrass in a given grid.

    Args:
        grid (np.array): A 3D numpy array representing the simulation grid.
                         Each cell in the grid is a 1D array representing the cell's state.
                         A cell with all elements equal to zero is considered to be without seagrass.
        height (int): The number of rows in the grid.
        width (int): The number of columns in the grid.

    Returns:
        result (np.array): A 2D numpy array with the same dimensions as the input grid.
                           Each element in the 'result' array corresponds to a cell in the 'grid'.
                           The value of each element in 'result' is set to 1 if the corresponding cell in 'grid' contains seagrass,
                           and 0 if it does not.
                           
    Usage:
        result = Have_seagrass(grid, 100, 100)
        This will return a 100x100 2D array 'result', with each element indicating the presence or absence of seagrass.
    """
    result = np.zeros((height, width), dtype=int)
    
    # If there is no seagrass (i.e., all elements in the grid's cell are 0), set the corresponding cell in 'result' to 0
    for x in range(width):
        for y in range(height):
            # If all elements in the grid's cell are 0 (indicating no seagrass), continue to the next cell
            if state[x][y] == 'Empty':
                continue
            elif state[x][y] == 'Germinating':
                result[x][y] = 1
            else: # If not all elements in the grid's cell are 0 (indicating presence of seagrass), set the corresponding cell in 'result' to 1
                result[x][y] = 2

    return result



# This method runs one time step for a cell
def one_cell_run(t, grid):
    """
    This function runs one time step for a cell in the simulation. 

    Args:
        t (int): The current time point in the simulation.
        grid (list): The current state of the system.

    Returns:
        grid (list): The state of the system after the time step.
    """
    # print(f"Grid before time step {t}: {grid}")  # Print grid before time step
    # Unpack the grid into its components
    R, Nrint, N_org, NH4, NO2, NO3, POP, SRP, P_ma_int, P_R_int = grid
    
    # If this is the first time step, initialize the system
    if t == 0:
        R, Nrint = Growth_Model.Growth_model(Parameters.NH4,Parameters.NO3,Parameters.R,Parameters.Nrint,t)
        N_org, NH4, NO2, NO3 = Ni_Model.Ni_model(R, Parameters.N_org,Parameters.NH4,Parameters.NO2,Parameters.NO3,t)
        POP, SRP, P_ma_int, P_R_int = P_Model.P_model(Parameters.POP, Parameters.SRP, Parameters.P_ma_int, Parameters.P_R_int, R, Nrint, N_org, NH4, 0)
    else:
        # If there is no seagrass growth, no evolution takes place
        if grid.all() == False:
            return grid
        # If seagrass is present, perform a time step evolution using the growth and nutrient models
        R, Nrint = Growth_Model.Growth_model(NH4, NO3, R, Nrint, t+1)
        N_org, NH4, NO2, NO3 = Ni_Model.Ni_model(R, N_org, NH4, NO2, NO3, t+1)
        POP, SRP, P_ma_int, P_R_int = P_Model.P_model(POP, SRP, P_ma_int, P_R_int, R, Nrint, N_org, NH4, t+1)
    
    # Update the grid with the new state of the system
    grid = [R, Nrint, N_org, NH4, NO2, NO3, POP, SRP, P_ma_int, P_R_int]
    # print(f"Grid after time step {t}: {grid}")  # Print grid after time step
    return grid

