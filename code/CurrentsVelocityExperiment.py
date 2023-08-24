#!/usr/bin/env python3
"""
This script simulates and visualizes a Modified Mock Cellular Automata model to explore the effect of varying current velocities on seagrass growth.
The grid-based simulation evolves over time based on given parameters and rules. The output grids are saved as CSV files and visualized using Matplotlib.
"""

__appname__ = 'CurrentsVelocityExperiment'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define mock parameters for the cellular automata model
# These include various physical and environmental parameters
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

# Define the Modified Mock Cellular Automata class
# It simulates a grid-based environment with active and inactive cells
class ModifiedMockCA:
    def __init__(self, rows, cols, initial_active_fraction=0.1):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols))
        self.next_grid = np.zeros((rows, cols))
        
        # Randomly activate some cells based on the given active fraction
        num_active_cells = int(rows * cols * initial_active_fraction)
        active_indices = np.random.choice(rows * cols, num_active_cells, replace=False)
        for index in active_indices:
            row, col = divmod(index, cols)
            self.grid[row, col] = 1

    # Set the current velocity parameter
    def set_current_velocity(self, velocity):
        mock_parameters['current_velocity'] = velocity

    # Function to simulate the next state (evolution) of the grid
    def evolution(self):
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

# Function to run the mock cellular automata model for different current velocities
def run_mock_ca_model(velocity, grid_size, iterations=10):
    ca = ModifiedMockCA(grid_size[0], grid_size[1])
    ca.set_current_velocity(velocity)
    for _ in range(iterations):
        ca.evolution()
    return ca.grid

# Define grid size and current velocities to be simulated
grid_size = (100, 100)
current_velocities = [0.5, 1.5, 3.0]
velocity_labels = ['low', 'medium', 'high']

# Initialize the plot to visualize the output grids
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Loop through each velocity to generate, visualize, and save the grids
for ax, (velocity, label) in zip(axes, zip(current_velocities, velocity_labels)):
    grid = run_mock_ca_model(velocity, grid_size)
    
    # Flatten the grid and save it to a CSV file through a Pandas DataFrame
    flattened_grid = grid.flatten()
    df = pd.DataFrame({
        'Seagrass_Coverage': flattened_grid,
        'Current_Velocity': [velocity] * len(flattened_grid)
    })
    df.to_csv(f'../data/seagrass_coverage_{label}_velocity.csv', index=False)
    
    # Visualization of the grid
    ax.imshow(grid, cmap="GnBu", origin='lower')
    ax.set_title(f"Current Velocity: {velocity} m/s", fontsize=20, fontweight = 'bold')
    ax.set_xticks(np.arange(0, grid_size[0], 10))
    ax.set_yticks(np.arange(0, grid_size[1], 10))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(which='both', axis='both', linestyle='-', color='white', linewidth=0.5)

# Finalize the plot and display
plt.tight_layout()
plt.subplots_adjust(top=5)
# Uncomment the following line to set a super title for the plot
# plt.suptitle("Seagrass Growth Patterns for Different Current Velocities", y=0.95, fontsize=20)
plt.show()
