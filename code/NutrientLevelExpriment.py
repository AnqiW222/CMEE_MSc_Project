#!/usr/bin/env python3
"""
The code simulates the growth of seagrass under different nutrient conditions using a Cellular Automata (CA) model.
It generates mock data for the CA model, evolves the system for each nutrient condition, and saves the output
as CSV files. It also visualizes the seagrass distribution for different nutrient levels.
"""

__appname__ = 'NutrientLevelExpriment'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

# Importing necessary modules
# numpy for numerical computations and array manipulation
import numpy as np
# matplotlib for visualization
import matplotlib.pyplot as plt
# pandas for data manipulation and CSV file creation
import pandas as pd


# Define the size of the grid
grid_size = (100, 100)  # Size of the CA grid, 100x100 cells

# Define different nutrient levels
nutrient_levels = ["Low", "Medium", "High"]  # Possible nutrient levels: Low, Medium, High

# Mock parameters for the CA model
# dx, dy, dt, etc. are model parameters for the CA simulation
mock_parameters = {
    'dx': 1,
    'dy': 1,
    'dt': 1,
    'Tmax': 100,
    'Imax': 300,
    'PAR': 400,
    'I0': 200,
    'Kd': 0.1,
    'z': 5,
    'T': 25,
    'S': 35,
    'current_velocity': 1.0
}

class MockCA:
    """
    Mock Cellular Automata (CA) class for seagrass growth simulation.
    """
    def __init__(self, rows, cols):
        """
        Initialize the CA grid with given number of rows and columns.
        
        :param rows: Number of rows in the grid
        :param cols: Number of columns in the grid
        """
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols))
        self.next_grid = np.zeros((rows, cols))

    def set_current_velocity(self, velocity):
        """
        Update the current velocity parameter for the CA model.
        
        :param velocity: New value for the current velocity
        """
        mock_parameters['current_velocity'] = velocity

    def evolution(self):
        """
        Evolve the CA grid by one time step based on the predefined rules.
        """
        for i in range(1, self.rows - 1):
            for j in range(1, self.cols - 1):
                total = int((self.grid[i, j - 1] + self.grid[i, j + 1] +
                             self.grid[i - 1, j] + self.grid[i + 1, j] +
                             self.grid[i - 1, j - 1] + self.grid[i - 1, j + 1] +
                             self.grid[i + 1, j - 1] + self.grid[i + 1, j + 1]) * mock_parameters['current_velocity'])
                if self.grid[i, j] == 1:
                    if total < 2 or total > 3:
                        self.next_grid[i, j] = 0
                    else:
                        self.next_grid[i, j] = 1
                else:
                    if total == 3:
                        self.next_grid[i, j] = 1
        self.grid, self.next_grid = self.next_grid, self.grid

def run_mock_nutrient_experiment(nutrient_level, grid_size, iterations=10):
    """
    Run a mock nutrient experiment to simulate seagrass growth based on nutrient levels.
    
    :param nutrient_level: The level of nutrients ('Low', 'Medium', or 'High')
    :param grid_size: The size of the CA grid
    :param iterations: The number of CA evolution iterations
    :return: A CA grid showing the distribution of seagrass
    """
    ca = MockCA(grid_size[0], grid_size[1])
    
    # Adjust the growth probability based on nutrient level
    if nutrient_level == "Low":
        growth_probability = 0.4
    elif nutrient_level == "Medium":
        growth_probability = 0.7
    else:  # High
        growth_probability = 0.5
    
    for _ in range(iterations):
        ca.evolution()
        ca.grid = np.random.choice([1, 0], size=grid_size, p=[growth_probability, 1 - growth_probability])
    return ca.grid

# Visualization and running the experiment
# Creating a subplot with 1 row and 3 columns for visualizing each nutrient condition
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for ax, nutrient_level in zip(axes, nutrient_levels):
    # Run the CA simulation for each nutrient level
    grid = run_mock_nutrient_experiment(nutrient_level, grid_size)
    
    # Saving the grid to a CSV file
    flattened_matrix = grid.flatten()
    data = pd.DataFrame({
        'Seagrass_Coverage': flattened_matrix,
        'Nutrient_Level': [nutrient_level] * len(flattened_matrix)
    })
    csv_filename = f"../data/seagrass_coverage_matrix_nutrient_{nutrient_level}.csv"
    data.to_csv(csv_filename, index=False)
    
    # Visualization code (unchanged)
    ax.imshow(grid, cmap="GnBu", origin='lower')
    ax.set_title(f"{nutrient_level} Nutrient Level", fontsize=20, fontweight = 'bold')
    ax.set_xticks(np.arange(0, grid_size[0], 10))
    ax.set_yticks(np.arange(0, grid_size[1], 10))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(which='both', axis='both', linestyle='-', color='white', linewidth=0.5)

# Adjust the layout for better visibility
plt.tight_layout()
plt.subplots_adjust(top=1.25)
# plt.suptitle("Mock Seagrass Growth Patterns for Different Nutrient Levels", y=1.25, fontsize=20)
plt.show()
