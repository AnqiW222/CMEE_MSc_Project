#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script extends a Cellular Automata (CA) model to investigate the impact of multiple environmental
parameters on seagrass density. The CA model is extended to include additional initialization methods.
We run simulations for different parameter ranges and then perform a sensitivity analysis to find out
which parameters have the most significant impact on seagrass density.
"""
__appname__ = 'SensitiveAnalysis'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

import numpy as np
import matplotlib.pyplot as plt
from CA_Model import CA

# Extend the CA class to include the new initialization methods
class ExtendedCA(CA):
    
    def random_initialize_grid(self, seagrass_probability=0.5):
        for i in range(self.width):
            for j in range(self.height):
                if np.random.rand() < seagrass_probability:
                    self.grid[i][j] = "Seagrass"
                else:
                    self.grid[i][j] = "Water"

    def center_patch_initialize_grid(self, patch_size=20):
        start_x = (self.width - patch_size) // 2
        start_y = (self.height - patch_size) // 2
        for i in range(start_x, start_x + patch_size):
            for j in range(start_y, start_y + patch_size):
                self.grid[i][j] = "Seagrass"

# Define the parameter ranges
silt_levels = np.linspace(5, 500, 10)
temperatures = np.linspace(10, 25, 8)
depths = np.linspace(0.5, 40, 10)
salinities = np.linspace(30, 40, 11)
light_conditions = np.linspace(10, 100, 10) / 100  # Convert to fraction
current_velocities = np.linspace(0, 1.5, 8)

NH4_levels = np.linspace(0, 3, 10)
NO3_levels = np.linspace(0, 30, 10)
SRP_levels = np.linspace(0.1, 2, 10)
POP_levels = np.linspace(0, 10, 10)

# Initialize the CA model
ca = CA(100, 100, plot_results=False)

# Function to run the simulation for each parameter range and record the final density of seagrass
def run_simulation(param_values, param_name):
    final_seagrass_densities = []
    for value in param_values:
        ca.initialize_grid()
        
        # Set the parameter value
        if param_name == "silt":
            ca.silt = value
        elif param_name == "temperature":
            ca.temp = value
        elif param_name == "depth":
            ca.depth = value
        elif param_name == "salinity":
            ca.salinity = value
        elif param_name == "light":
            ca.light = value
        elif param_name == "current":
            ca.current = value
        elif param_name == "NH4":
            ca.NH4 = value
        elif param_name == "NO3":
            ca.NO3 = value
        elif param_name == "SRP":
            ca.SRP = value
        elif param_name == "POP":
            ca.POP = value
        
        # Run the simulation
        ca.evolution(num_of_steps=52)  # For 52 weeks
        
        # Record the final density of seagrass
        final_seagrass_densities.append(np.sum(ca.grid == "Seagrass") / (ca.width * ca.height))
    
    return final_seagrass_densities

# Run simulations for each parameter
results = {}
params = [
    ("silt", silt_levels),
    ("temperature", temperatures),
    ("depth", depths),
    ("salinity", salinities),
    ("light", light_conditions),
    ("current", current_velocities),
    ("NH4", NH4_levels),
    ("NO3", NO3_levels),
    ("SRP", SRP_levels),
    ("POP", POP_levels)
]

for param_name, param_values in params:
    results[param_name] = run_simulation(param_values, param_name)

# Compute the impact of each parameter
differences = {param: max(densities) - min(densities) for param, densities in results.items()}

# Normalize the differences to compute the relative impact in percentage
total_difference = sum(differences.values())
percent_impact = {param: (diff / total_difference) * 100 for param, diff in differences.items()}

# After computing the differences and percent impacts in the sensitivity analysis code
# Print the raw differences for each parameter
print("Raw Differences:")
for param, diff in differences.items():
    print(f"{param}: {diff}")

# Print the normalized percent impacts for each parameter
print("\nPercent Impacts:")
for param, impact in percent_impact.items():
    print(f"{param}: {impact:.2f}%")

# Plot the fractional impact using a bar chart
plt.bar(percent_impact.keys(), percent_impact.values(), color='blue')
plt.ylabel('Fractional Impact (%)')
plt.title('Fractional Impact of Factors on Seagrass Density')
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
plt.tight_layout()  # Ensure labels don't get cut off
plt.show()
