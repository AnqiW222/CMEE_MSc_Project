#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script uses a fuzzy logic control system to model the growth rate of seagrass
based on two environmental variables: nutrient level and current velocity.
The script also includes a 1D Cellular Automata model to simulate the seagrass growth over time.
"""
__appname__ = 'DizzyModel'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Define the fuzzy input variables for nutrient level and current velocity
nutrient_level = ctrl.Antecedent(np.linspace(0, 10, 100), 'Nutrient Level')
current_velocity = ctrl.Antecedent(np.linspace(0, 20, 100), 'Current Velocity')

# Define the fuzzy output variable for seagrass growth rate
seagrass_growth = ctrl.Consequent(np.linspace(0, 1, 100), 'Seagrass Growth Rate')

# Define the membership functions for each fuzzy variable
nutrient_level['Low'] = fuzz.trimf(nutrient_level.universe, [0, 0, 5])
nutrient_level['Medium'] = fuzz.trimf(nutrient_level.universe, [0, 5, 10])
nutrient_level['High'] = fuzz.trimf(nutrient_level.universe, [5, 10, 10])

current_velocity['Slow'] = fuzz.trimf(current_velocity.universe, [0, 0, 10])
current_velocity['Moderate'] = fuzz.trimf(current_velocity.universe, [0, 10, 20])
current_velocity['Fast'] = fuzz.trimf(current_velocity.universe, [10, 20, 20])

seagrass_growth['Low'] = fuzz.trimf(seagrass_growth.universe, [0, 0, 0.5])
seagrass_growth['Medium'] = fuzz.trimf(seagrass_growth.universe, [0, 0.5, 1])
seagrass_growth['High'] = fuzz.trimf(seagrass_growth.universe, [0.5, 1, 1])

# Define the fuzzy rules for the control system
rule1 = ctrl.Rule(nutrient_level['Low'] & current_velocity['Slow'], seagrass_growth['Low'])
rule2 = ctrl.Rule(nutrient_level['Low'] & current_velocity['Fast'], seagrass_growth['Low'])
rule3 = ctrl.Rule(nutrient_level['High'] & current_velocity['Slow'], seagrass_growth['High'])
rule4 = ctrl.Rule(nutrient_level['High'] & current_velocity['Fast'], seagrass_growth['Medium'])
rule5 = ctrl.Rule(nutrient_level['Medium'] & current_velocity['Moderate'], seagrass_growth['Medium'])

# Create the fuzzy control system with the rules
fuzzy_system = ctrl.ControlSystem(rules=[rule1, rule2, rule3, rule4, rule5])

# Create a simulation environment for the control system
fuzzy_simulation = ctrl.ControlSystemSimulation(fuzzy_system)

# Initialize 1D Cellular Automata model
num_cells = 10
num_steps = 5
initial_nutrient_levels = np.random.uniform(0, 10, num_cells)
initial_current_velocity = np.random.uniform(0, 20, num_cells)
ca_grid = np.zeros((num_steps, num_cells))
ca_grid[0, :] = initial_nutrient_levels

# Run the Cellular Automata model
for t in range(1, num_steps):
    for i in range(num_cells):
        fuzzy_simulation.input['Nutrient Level'] = ca_grid[t-1, i]
        fuzzy_simulation.input['Current Velocity'] = initial_current_velocity[i]
        fuzzy_simulation.compute()
        ca_grid[t, i] = fuzzy_simulation.output['Seagrass Growth Rate']

# Plot the simulation results
plt.imshow(ca_grid, aspect='auto', cmap='viridis')
plt.colorbar(label='Seagrass Growth Rate')
plt.xlabel('Cell Index')
plt.ylabel('Time Step')
plt.title('Seagrass Growth Over Time')
plt.show()
