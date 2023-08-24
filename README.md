<<<<<<< HEAD
# *MSc CEMM Project:* 

## Modelling Seagrass Growth Growing Patterns and Identifying the Impact Factor using Cellular Automata for Restoration Purposes

This README file contains details about the cellular automata (CA) model and statistical analysis coding scripts for Anqi Wang's ([aw222@ic.ac.uk](mailto:aw222@ic.ac.uk)) MSc CMEE final thesis. This dissertation contributes towards the fulfilment of MSc Computational Methods in Ecology and Evolution (CMEE) at Imperial College London. 

### Table of Contents
- [Introduction](#introduction)
- [Folder Structure](#folder-structure)
- [Installation and Usage](#installation-and-usage)
- [Scripts Overview](#scripts-overview)
- [Features](#features)
- [Output](#output)

### Introduction

This repository contains code, data, and results for modeling and analyzing seagrass growth. It uses both Cellular Automata (CA) and Ordinary Differential Equations (ODEs) to understand the impact of environmental factors on seagrass ecosystems.

### Folder Structure

- `code/`: Contains all the Python and R scripts.
- `data/`: Stores input data.
- `results/`: Holds output data and visualizations.
- `Proposal/`:  files for proposal writing-up
- `SupplementaryInformation.pdf`: Detailed ecological ODE model and methodology.

### Installation and Usage

Clone the repository:
```bash
git clone https://github.com/your-username/your-repository.git
```

Install required Python packages:

`pip install -r requirements.txt`

Run the main script:

`python main.py`

Run the R script for ANOVA testing:

`source("ANOVAforExp.r")`

### Scripts Overview

#### CA_model.py

The foundational Cellular Automata (CA) model script that serves as the base for various experiments.

#### Growth_Model.py

Models the growth of seagrass using ordinary differential equations (ODEs).

#### Ni_Model.py

Models the nitrogen cycle in seagrass ecosystems using ODEs.

#### P_Model.py

Models the phosphorus cycle in seagrass ecosystems using ODEs.

#### Parameters.py

Centralized location for defining and managing parameters used in the CA model.

#### User_Input.py

Handles user-defined parameters for the CA model.

#### main.py

The main script that ties all modules together for comprehensive analysis.

#### SavingPlot.py

Renames and combines PNG images into a single PDF file.

#### GrowthPattern.py

Visualizes different seagrass growth scenarios.

#### NutrientLevelExperiment.py

Simulates the effect of varying nutrient levels on seagrass growth.

#### CurrentsVelocityExperiment.py

Explores the effect of varying current velocities on seagrass growth.

#### ANOVAtest.py

Performs one-way ANOVA analysis on growth count matrices.

#### DizzyModel.py

Uses a fuzzy logic control system to model seagrass growth.

#### SensitiveAnalysis.py

Performs sensitivity analysis to investigate the impact of environmental parameters on seagrass density.

#### ANOVAforExp.r

R script for testing the ANOVA for nutrient and current velocity experiments.

### Features

- Modular design for ease of experimentation

- Utilizes both Cellular Automata and Ordinary Differential Equations for modeling

- Extensive parameter control through `Parameters.py` and `User_Input.py`

- Capability to perform sensitivity analysis

  ### Output

  - Various visualizations of seagrass growth scenarios
  - CSV files representing the CA grid states at different time steps
  - ANOVA results for different experiments
  - A single PDF file combining various plots

### Language Versions

**Python:** 3.9.12 
**R:** 4.2.1 
**bash:** 3.2 
**LaTeX:** 3.141592653-2.6-1.40.24 (TeX Live 2022) 

All code has been written on a MacOS version 12.6 and any dependencies are detailed below the script names

### Author & Contact

**Name:** ANQI WANG
**Email:** [aw222@ic.ac.uk](mailto:aw222@ic.ac.uk)
=======
# CMEE_MSc_Project
CMEE MSc Project: Predicting high carbon seagrass sites to aid protection of coastal carbon stock
>>>>>>> 3ab93a3086c03dff45853145dca7ab629e666b23
