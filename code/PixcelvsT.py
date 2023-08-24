#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script processes images from different scenarios to extract the seagrass coverage and germination rates over a period of 260 weeks.
It then visualizes these rates using matplotlib.
"""
__appname__ = 'PixcelvsT'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Define the list of scenario folders
scenarios = ['RIS_5yrs_image', 'CCS_5yrs_image', 'ClGS_5yrs_image', 'AbS_5yrs_image', 'CGS_5yrs_image']

# Initialize a dictionary to store coverage and germination rates for each scenario
scenario_data = {}

# Loop through each scenario to process images and calculate rates
for scenario in scenarios:
    coverage_rates = []
    germination_rates = []
    
    # Loop through each week's image for the current scenario
    for week in range(260):
        # Construct the file path for the image of the current week and scenario
        img_path = f"../results/5yrs_Scenario_images/Gray/{scenario}/week_{week}.png"
        
        # Read the image and convert to grayscale
        img = Image.open(img_path).convert("L")
        img_array = np.array(img)
        
        # Identify black (0), gray (128), and white (255) pixels
        is_black = (img_array == 0)
        is_gray = (img_array == 128)  
        is_white = (img_array == 255)
        
        # Calculate the total number of pixels in the image
        total_pixels = img_array.size
        
        # Calculate coverage and germination percentages
        coverage_rate = np.sum(is_white) / total_pixels * 100
        germination_rate = np.sum(is_gray) / total_pixels * 100
        
        # Append these rates to their respective lists
        coverage_rates.append(coverage_rate)
        germination_rates.append(germination_rate)
    
    # Store calculated rates for the current scenario in the dictionary
    scenario_data[scenario] = {'coverage_rates': coverage_rates, 'germination_rates': germination_rates}

# Define short names for scenarios for plotting
short_names = {'RIS_5yrs_image': 'RIS', 'CCS_5yrs_image': 'CCS', 'AbS_5yrs_image': 'AbS', 'ClGS_5yrs_image': 'ClGS', 'CGS_5yrs_image': 'CGS'}

# Set global font size for the plots
plt.rcParams.update({'font.size': 16})

# Create and show the coverage rate plot
plt.figure(figsize=(12, 6))
for scenario in scenarios:
    plt.plot(range(260), scenario_data[scenario]['coverage_rates'], label=short_names[scenario])
plt.xlabel('Week')
plt.ylabel('Coverage Percentage')
# plt.title('Seagrass Coverage Rates Over Time')
plt.legend(loc='lower right')
plt.savefig("./5yrs_Scenario_images/coverage_rates_high_quality.png", dpi=300, format='png', bbox_inches='tight')
plt.show()

# Create and show the germination rate plot
plt.figure(figsize=(12, 6))
for scenario in scenarios:
    plt.plot(range(260), scenario_data[scenario]['germination_rates'], label=short_names[scenario])
plt.xlabel('Week')
plt.ylabel('Germination Percentage')
# plt.title('Seagrass Germination Rates Over Time')
plt.legend()
plt.savefig("../results/5yrs_Scenario_images/germination_rates_high_quality.png", dpi=300, format='png', bbox_inches='tight')
plt.show()
