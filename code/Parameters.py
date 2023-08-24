#!/usr/bin/env python3

"""
This Python script, 'Parameters.py', serves as a centralized location for defining and managing parameters used in the Cellular Automata (CA) model for simulating seagrass growth. The script contains parameters that include initial values for various environmental and physiological variables, indices for each variable, and constants for different growth stages.

The script contains several key components:

1. Indices for each variable: The script defines constants for the indices of each variable in the system state, which include nitrogen (N), phosphorus (P), carbon (C), and light conditions, among others.

2. Initial values for variables: The script defines initial values for variables such as seagrass growth biomass (R), internal nitrogen (Nrint), organic nitrogen (N_org), ammonia (NH4), nitrite (NO2), nitrate (NO3), and various forms of phosphorus. These initial values are set according to the number of weeks that have passed in the simulation, which is meant to represent different seasons of the year (spring, summer, autumn, and winter).

The script allows for easy modification and access to the parameters used in the CA model, aiding in the flexibility and extensibility of the model.
"""

__appname__ = 'Parameters'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

from main import num_of_weeks
# Constants representing the indices of each variables
N_IDX = 0
P_IDX = 1
C_IDX = 2
CB_IDX = 3
NB_IDX = 4
PB_IDX = 5
LIGHT_IDX = 6
R_IDX = 7
G_IDX = 8
M_IDX = 9
    

# Set different initial values for differnt 
if num_of_weeks < 13:
    # Spring
    R=110 # Slightly increased in spring
    Nrint = 2.4
    N_org = 25
    NH4 = 0.05
    NO2 = 0.01
    NO3 = 0.22
    POP = 0.23
    SRP = 0.12
    P_ma_int = 0.02
    P_R_int = 0.02
    GROWTH_RATE = 0.84  # Increased by 20%
    germination_rate = 3
    reproduction_rate = 5.5
    temperature = 16.5  # Increased by 10%
    oxygen = 3.62
    ORP_s = 100
    DO = 4.97

    
elif num_of_weeks >= 13 and num_of_weeks < 26:
    # Summer
    R = 120 # Further increased in summer
    Nrint = 2.4
    N_org = 25
    NH4 = 0.05
    NO2 = 0.01
    NO3 = 0.22
    POP = 0.23
    SRP = 0.12
    P_ma_int = 0.02
    P_R_int = 0.02
    GROWTH_RATE = 0.91  # Increased by 30%
    germination_rate = 3
    reproduction_rate = 5.5
    temperature = 18.0  # Increased by 20%
    oxygen = 3.26  # Decreased slightly
    ORP_s = 400.0  # Dramatically increased
    DO = 4.97

    
elif num_of_weeks >= 26 and num_of_weeks < 39:
    # Autumn
    R = 90 # Slightly decreased in autumn
    Nrint = 2.4
    N_org = 25
    NH4 = 0.05
    NO2 = 0.01
    NO3 = 0.22
    POP = 0.23
    SRP = 0.12
    P_ma_int = 0.02
    P_R_int = 0.02
    GROWTH_RATE = 0.56  # Decreased by 20%
    germination_rate = 2.4  # Decreased by 20%
    reproduction_rate = 4.4  # Decreased by 20%
    temperature = 13.5  # Decreased by 10%
    oxygen = 3.62
    ORP_s = 200.0  # Increased
    DO = 4.97

    
else:
    # Winter
    R = 70 # Significantly decreased in winter
    Nrint = 2.4
    N_org = 25
    NH4 = 0.05
    NO2 = 0.01
    NO3 = 0.22
    POP = 0.23
    SRP = 0.12
    P_ma_int = 0.02
    P_R_int = 0.02
    GROWTH_RATE = 0.35  # Significantly decreased
    germination_rate = 1.5  # Significantly decreased
    reproduction_rate = 2.75  # Significantly decreased
    temperature = 9.0  # Significantly decreased
    oxygen = 3.62
    ORP_s = -100.0  # Dramatically decreased
    DO = 4.97

        



__all__ = ['N_IDX', 'P_IDX','C_IDX','CB_IDX','NB_IDX','PB_IDX','LIGHT_IDX',
           'R_IDX','G_IDX','M_IDX','R','Nrint','N_org','NH4','NO2','NO3','POP',
           'SRP','P_ma_int','P_R_int','ORP_s']
