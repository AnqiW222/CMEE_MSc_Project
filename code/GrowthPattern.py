#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is designed to create a visualization of different seagrass growth scenarios.
It reads images that represent the state of seagrass in each scenario at specific weeks 
and arranges them in a grid for comparative analysis.
"""
__appname__ = 'GrowthPattern'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

# Import the necessary libraries
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Define the file paths for the PNG files of the five scenarios
# Dictionary containing the paths to the images for each scenario at different weeks
image_filepaths = {
    'AbS': ['../results/AbS/AbS_image/week_0.png', '../results/AbS/AbS_image/week_26.png', '../results/AbS/AbS_image/week_51.png'],
    'CCS': ['../results/CCS/CCS_image/week_0.png', '../results/CCS/CCS_image/week_26.png', '../results/CCS/CCS_image/week_51.png'],
    'CGS': ['../results/CGS/CGS_image/week_0.png', '../results/CGS/CGS_image/week_26.png', '../results/CGS/CGS_image/week_51.png'],
    'ClGS': ['../results/ClGS/ClGS_image/week_0.png', '../results/ClGS/ClGS_image/week_26.png', '../results/ClGS/ClGS_image/week_51.png'],
    'RIS': ['../results/RS/RIS_image/week_0.png', '../results/RIS/RIS_image/week_26.png', '../results/RIS/RIS_image/week_51.png']
}

# Weeks for which we have images
# List of selected weeks to be displayed in the grid
selected_weeks = [0, 26, 51]

# Initialize a figure to combine all the images
# Create a subplot grid layout to hold all the images
num_scenarios = len(image_filepaths)
num_weeks_per_scenario = len(selected_weeks)
fig, axes = plt.subplots(num_scenarios, num_weeks_per_scenario, figsize=(30, 40))

# Loop through each scenario and week to place images in the grid
# Populate the grid with images from each scenario and week
for i, (scenario, filepaths) in enumerate(image_filepaths.items()):
    for j, filepath in enumerate(filepaths):
        ax = axes[i, j]
        img = mpimg.imread(filepath)
        ax.imshow(img)
        ax.axis('off')
        
        # Label the images with the new format: "Scenario Name: Week Number"
        ax.set_title(f'{scenario}: Week {selected_weeks[j]}', fontsize= 24, fontweight = 'bold')

# Reduce the gap between the plots for clearer readability
plt.subplots_adjust(wspace=0.001, hspace=0.3)

# Add a title for the entire plot
# Uncomment this if you want to add a super title for the whole grid
# plt.suptitle('Seagrass Growth Heatmaps for Selected Weeks Across Different Scenarios', fontsize= 24, fontweight='bold')

# Adjust the layout to make sure everything fits
plt.tight_layout(rect=[0, 0, 1, 0.98])

# Show the combined plot
plt.show()
