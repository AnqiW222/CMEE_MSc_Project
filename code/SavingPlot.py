#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script renames PNG images in a specified directory based on a given pattern and then combines them into a single PDF file.
"""
__appname__ = 'SavingPlot'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"
# Import the necessary libraries
import os  # For operating system dependent functionality like reading file names
import re  # For regular expression matching
from PIL import Image  # For image processing

# Define the path to the directory containing the images
directory_path = '../results/RIS/RIS_image'  # Change to the desired directory path

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    # Use regular expression to match file names of the pattern 'FigureNames (X).png' where X is any number
    match = re.match(r'FigureNames \((\d+)\).png', filename)  # figure names pattern
    if match:
        # Rename the file to 'week_X.png'
        new_name = f"week_{match.group(1)}.png"
        # Rename the file using os.rename()
        os.rename(os.path.join(directory_path, filename), os.path.join(directory_path, new_name))

# Define the path and name for the output PDF file
output_file = '../results/RIS_output.pdf'  # Change to the desired output file name and location

# Create a list of .png files in the directory
png_files = [f for f in os.listdir(directory_path) if f.endswith('.png')]

# Sort the list of .png files to maintain order
png_files.sort()

# Open each image file and append it to the 'images' list
images = [Image.open(os.path.join(directory_path, f)) for f in png_files]

# Save the images as a PDF
# The first image will be the cover, and the rest will be appended
images[0].save(output_file, save_all=True, append_images=images[1:])

