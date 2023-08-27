#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to Create a GIF from PNG Images

This script takes multiple PNG images from a specified directory, 
filters them based on their filename ending with '_week.png', 
and then creates a GIF animation from these images.

Requirements:
- PIL (Pillow) library for image manipulation.

Usage:
1. Replace '../results/Scenario_output/AbS/AbS_image/***' with the directory where your PNG images are stored.
2. Replace '../reslts/Scenario_output/*.gif' with the directory where you want to save the generated GIF.
3. Run the script.

Author: Your Name
Date: Date of Creation
"""

from PIL import Image
import os

# Define the directory where the images are saved
image_dir = '../results/Scenario_output/RIS/RIS_image'

# List all files in the directory without any filtering
all_files_in_subfolder = os.listdir(image_dir)

# Filter the filenames to include only those that start with 'week_' and end with '.png'
image_files = [f for f in all_files_in_subfolder if f.startswith('week_') and f.endswith('.png')]

# Sort the image files
image_files = sorted(image_files)

# Create a list to hold Image objects
images = []

# Load all the images
for filename in image_files:
    images.append(Image.open(os.path.join(image_dir, filename)))

# Create the GIF
gif_path = '../results/RIS_output.gif'
images[0].save(gif_path,
               save_all=True,
               append_images=images[1:],
               loop=0,  # 0 for infinite loop
               duration=300)  # Duration for each frame in milliseconds
