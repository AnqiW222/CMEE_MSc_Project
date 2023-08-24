#!/usr/bin/env python3

"""
This Python script, 'User_Input.py', is developed to handle user input for the parameters used in the simulation of seagrass growth using a Cellular Automaton (CA) model. The script allows users to modify the predefined parameters in the 'Parameters.py' module according to their specific requirements.

The script contains one key function:

1. 'User_Input': This function accepts user-defined values for various parameters used in the CA model. If a user provides a value for a parameter, the function overwrites the corresponding default value in the 'Parameters.py' module with the user-defined value. If the user does not provide a value, the function leaves the default value unchanged. The parameters that can be modified include indices for each variable, initial values for variables, and constants for different growth stages.

The script provides a flexible interface for users to customize the parameters of the CA model, thereby allowing users to simulate seagrass growth under different conditions and scenarios.
"""

__appname__ = 'User_Input'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

# Import the Parameters module, which contains our predefined parameters
import Parameters

def User_Input(N_IDX = None, P_IDX = None, C_IDX = None, CB_IDX = None, NB_IDX = None, PB_IDX = None, LIGHT_IDX = None, 
               R_IDX = None, G_IDX = None, M_IDX = None, Nrint = None, N_org = None, NH4 = None, NO2 = None, 
               NO3 = None, POP = None, SRP = None, R = None, P_ma_int = None, P_R_int = None, GROWTH_RATE = None, 
               germination_rate = None, reproduction_rate = None, temperature = None, oxygen = None, ORP_s = None, DO = None):
    """
    Function to update the parameters in the Parameters module based on user input. 
    
    Each argument corresponds to a parameter in the Parameters module. If an argument is provided when calling 
    the function, the corresponding parameter in the Parameters module will be overwritten with the new value. 
    If an argument is not provided, the corresponding parameter in the Parameters module will remain unchanged.
    
    Parameters:
    N_IDX (int): Index for parameter N.
    P_IDX (int): Index for parameter P.
    C_IDX (int): Index for parameter C.
    CB_IDX (int): Index for parameter CB.
    NB_IDX (int): Index for parameter NB.
    PB_IDX (int): Index for parameter PB.
    LIGHT_IDX (int): Index for parameter LIGHT.
    R_IDX (int): Index for parameter R.
    G_IDX (int): Index for parameter G.
    M_IDX (int): Index for parameter M.
    R (int): Parameter R.
    Nrint (int): Parameter Nrint.
    N_org (int): Parameter N_org.
    NH4 (int): Parameter NH4.
    NO2 (int): Parameter NO2.
    NO3 (int): Parameter NO3.
    POP (int): Parameter POP.
    SRP (int): Parameter SRP.
    R (int): Parameter R.
    P_ma_int (int): Parameter P_ma_int.
    P_R_int (int): Parameter P_R_int.
    GROWTH_RATE, germination_rate, reproduction_rate: Rates for different biological processes (Default: None)
    temperature: Environmental temperature (Default: None, Units: °C)
    oxygen, ORP_s, DO: Oxygen-related parameters (Default: None, Units: mg/L)
    
    Returns:
    None
    """
    if N_IDX is not None:
        Parameters.N_IDX = N_IDX
        
    if P_IDX is not None:
        Parameters.P_IDX = P_IDX
        
    if C_IDX is not None:
        Parameters.C_IDX = C_IDX
        
    if CB_IDX is not None:
        Parameters.CB_IDX = CB_IDX
        
    if NB_IDX is not None:
        Parameters.NB_IDX = NB_IDX
        
    if PB_IDX is not None:
        Parameters.PB_IDX = PB_IDX
        
    if LIGHT_IDX is not None:
        Parameters.LIGHT_IDX = LIGHT_IDX
        
    if R_IDX is not None:
        Parameters.R_IDX = R_IDX
        
    if G_IDX is not None:
        Parameters.G_IDX = G_IDX
        
    if M_IDX is not None:
        Parameters.M_IDX = M_IDX
        
    if Nrint is not None:
        Parameters.Nrint = Nrint
        
    if N_org is not None:
        Parameters.N_org = N_org
        
    if NH4 is not None:
        Parameters.NH4 = NH4
        
    if NO2 is not None:
        Parameters.NO2 = NO2
        
    if NO3 is not None:
        Parameters.NO3 = NO3
        
    if POP is not None:
        Parameters.POP = POP
        
    if SRP is not None:
        Parameters.SRP = SRP
        
    if R is not None:
        Parameters.R = R
        
    if P_ma_int is not None:
        Parameters.P_ma_int = P_ma_int
        
    if P_R_int is not None:
        Parameters.P_R_int = P_R_int
        
    if GROWTH_RATE is not None:
        Parameters.GROWTH_RATE = GROWTH_RATE
        
    if germination_rate is not None:
        Parameters.germination_rate = germination_rate
        
    if reproduction_rate is not None:
        Parameters.reproduction_rate = reproduction_rate
        
    if temperature is not None:
        Parameters.temperature = temperature
        
    if oxygen is not None:
        Parameters.oxygen = oxygen
        
    if ORP_s is not None:
        Parameters.ORP_s = ORP_s
        
    if DO is not None:
        Parameters.DO = DO
