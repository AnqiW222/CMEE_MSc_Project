#!/usr/bin/env python3

"""
This Python script defines a Cellular Automaton (CA) for simulating seagrass growth and behavior. The CA is a 2D grid where each cell represents a patch of seabed and contains state variables for seagrass and its environment.

The script contains a class 'CA' with the following key methods:

1. '__init__': This method initializes the CA with the specified width and height, and sets initial values for the environmental parameters in each cell of the grid.

2. 'transition_rule': This method defines the transition rules for the cellular automaton, which dictate how the state of a cell changes over time based on its current state and environmental parameters.

3. 'initialize_grid': This method randomly initializes some cells with seagrass at the start of the simulation.

4. 'evolution': This method runs the simulation for a specified number of time steps. In each time step, it applies the transition rules to each cell, saves the state of the grid, and then calculates and plots the frequency of seagrass presence over the course of the simulation.

The simulation considers various environmental factors for seagrass growth, including silt concentration, temperature, depth, salinity, nutrient levels, light conditions, and current velocity. These factors influence the recruitment, germination, growth, and reproduction stages of the seagrass lifecycle.

The grid's state is saved at each step, allowing the user to observe the temporal evolution of the seagrass population.
"""

__appname__ = 'CA_Model'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

import pickle 
import numpy as np
import random
import Parameters
import Cell
import matplotlib.pyplot as plt

def PlotResult(matrix,m):
    # plot the heat map
    plt.imshow(matrix, cmap='viridis') # viridis -- for the coloured plot 'Greys_r' for bw
    # add colour bar
    plt.colorbar()  
    # show the plot
    plt.show()
    # save the plot
    # plt.savefig(f'week={m}.png')
    plt.pause(0.5)
    
def get_result(flag_now,flag_last,seagrass_counts):     
    for i in range(len(flag_last)):  
        for j in range(len(flag_last[0])):  
            if flag_now[i][j] == 1 and flag_last[i][j] == 0:  
                seagrass_counts[i][j] += 1  
                  
    return seagrass_counts
    
# This line declares a new class named "CA" (Cellular Automata).
class CA:  
    # The "__init__" method is the initialiser (constructor) for the class.
    def __init__(self, width, height, plot_results=True):
        # print("Grid initialized.")
        # Here the width and height for the cellular automata grid are set.
        self.width = width  
        self.height = height  
        # The grid is initialised as a 3-dimensional NumPy array of zeroes.
        # It's basically a 2-dimensional grid where each cell has 6 variables (third dimension).
        self.grid = np.zeros((height, width, 10), dtype=int) 
        # Create a matrix to save the states of each cell
        self.state = np.zeros((height, width), dtype=object)
        self.plot_results = plot_results
        
        # Set initial values for each cell
        for x in range (width):
            for y in range (height):
                self.state[x][y] = 'Empty'
                self.grid[x][y][Parameters.N_IDX] = 0.5 # Nitrogen concentration
                self.grid[x][y][Parameters.P_IDX] = 0.3 # Phosphrus concentration
                self.grid[x][y][Parameters.C_IDX] = 1.0
                self.grid[x][y][Parameters.CB_IDX] = 0 # Amount of seagrass
    
        # Set thresholds
        # Parameterss for the indices of light, nitrogen, phosphorus, and seagrass in the cell state array
        self.LIGHT_IDX = 3  # Assuming the 4th element represents light
        self.N_IDX = 0
        self.P_IDX = 1
        self.CB_IDX = 2  # Assuming the 3rd element represents seagrass

        # Thresholds for light and nutrient levels required for seagrass growth
        self.LIGHT_THRESHOLD_GROWTH = 0.5
        self.N_THRESHOLD_GROWTH = 0.3
        self.P_THRESHOLD_GROWTH = 0.3

        # Thresholds for light and nutrient levels required for seagrass death
        self.N_THRESHOLD_DEATH = 0.2
        self.P_THRESHOLD_DEATH = 0.2
        self.LIGHT_THRESHOLD_DEATH = 0.4
        self.RANDOMNESS_THRESHOLD_DEATH = 0.01
        self.CARRYING_CAPACITY = width * height * 0.75  # Assume that up to 75% of the grid can be covered with seagrass
        self.DISTURBANCE_THRESHOLD_DEATH = 0.01

        # Growth rate of the seagrass
        self.GROWTH_RATE = 0.1
        
       
        '''
        This part sets the attributes for the transition rules. Initial values are set here.
        Note: When an attribute is specific to a cell, keep it here.
        When an attribute is a fixed value, like temperature or threshold, it should be put in the parameter module and should change over time.
        '''
        self.silt = 0.5
        self.sand_to_silt_ratio = 0.7
        # self.temperature
        self.depth = 2
        self.salinity = 23.7
        # self.germination_rate
        self.oxygen_threshold = 2
        # self.oxygen
        self.nutrient_n = 2.4
        self.nutrient_n_threshold = 4.9
        self.light = 20
        self.current_velocity = 0.5
        # self.growth
        # self.growth_rate
        self.nutrient_p = 0.49
        self.nutrient_p_threshold = 0.83
        self.nutrient_n_threshold_for_reproduction = 0.41
        self.reproduction = 5
        self.reproduction_rate = 3

    # This function initializes the grid with all cells containing seagrass at the start of the simulation.
    def transition_rule(self, x, y):
        
        """
        This function represents a transition rule for a cell at position (x, y) 
        in a grid that models an environment.

        The cell can be in one of three states: 'Empty', 'Germinating', or 'Seagrass'. 
        The function checks the state of the cell and the environmental conditions,
        and updates the cell's state based on these conditions.

        'Empty': The cell can become 'Germinating' if certain conditions are met, 
        including the silt level, the sand to silt ratio, the temperature, the depth, 
        the salinity, and a random chance for germination.

        'Germinating': The cell can become 'Seagrass' if the oxygen level is below 
        a certain threshold.

        'Seagrass': The seagrass can grow or reproduce if certain conditions are met, 
        including the silt level, the nutrient levels, the light level, the temperature, 
        the depth, the salinity, and the current velocity.

        The function then updates the seagrass level in the grid at position (x, y),
        ensuring it doesn't exceed 1.

        Finally, the function returns the updated cell.
        """
        # print(f"Initial state at ({x}, {y}): {self.state[x][y]}")
        # Note: Here, 'self' refers to the cell at position (x, y) in the grid.
            # self = self.grid[x][y]
        if self.state[x][y] == 'Empty':
                # This line checks if all the variables in a particular grid cell [x][y] are zero.
            if self.grid[x][y].all() == False:  
                    # With a 10% chance, a new cell is grown at the location [x][y] by using the one_cell_run function of A_Cell class.
                    if np.random.rand() < 0.1:
                        # self.grid[x][y] = self.a_cell.one_cell_run(0, self.grid[x][y])
                        if self.grid[x][y][Parameters.N_IDX] > self.N_THRESHOLD_GROWTH:
                            if self.grid[x][y][Parameters.P_IDX] > self.P_THRESHOLD_GROWTH:
                            # if self.grid[x][y][Parameters.LIGHT_IDX] > self.LIGHT_THRESHOLD_GROWTH:
                                    # if self.grid[x][y][Parameters.NH4] > 0.01:
                                        # if self.grid[x][y][Parameters.NO2] > 0.01:
                                            # if self.grid[x][y][Parameters.NO3] > 0.1:
                    # if self.silt >= 0.2 and self.silt <= 0.9 and self.sand_to_silt_ratio == 2:  # Conditions for recruitment
                    #     if self.temperature >= 10 and self.temperature <= 20:  # Adding temperature conditions for recruitment
                    #         if self.depth <= 4:  # Adding depth conditions for recruitment
                    #             if self.salinity >= 20:  # Adding salinity conditions for recruitment
                    #                 if random.random() < self.germination_rate:  # Germination rate can be adjusted
                                self.state[x][y] = 'Germinating'
        elif self.state[x][y] == 'Germinating':
            if np.random.rand() < 0.1: 
                # if self.grid[x][y][Parameters.R_IDX] > 0.5:
                #     if self.oxygen < self.oxygen_threshold:  # Conditions for germination completion
                self.state[x][y] = 'Seagrass'
        elif self.state[x][y] == 'Seagrass':
            if np.random.rand() < 0.1: # Random death rate
                # if np.random.rand() < self.DISTURBANCE_THRESHOLD_DEATH:
                    # if np.random.rand() < self.CARRYING_CAPACITY:
                        # if np.random.rand() < self.RANDOMNESS_THRESHOLD_DEATH:
                            # if self.grid[x][y][Parameters.N_IDX] < self.N_THRESHOLD_DEATH:
                                # if self.grid[x][y][Parameters.P_IDX] < self.P_THRESHOLD_DEATH:
                                    # if self.grid[x][y][Parameters.LIGHT_IDX] < self.P_THRESHOLD_DEATH:
                                        # if self.grid[x][y][Parameters.P_IDX]>0.5:
                self.state[x][y] = 'Empty'
                # Conditions for growth and reproduction
            #         if self.silt >= 0.6 and self.silt <= 0.8 and self.nutrient_n > self.nutrient_n_threshold:
            #             if self.light >= 0.12 and self.light <= 0.37:  # Adding light conditions for growth
            #                 if self.temperature >= 13 and self.temperature <= 24:  # Adding temperature conditions for growth
            #                     if self.depth >= 1 and self.depth <= 6:  # Adding depth conditions for growth
            #                         if self.salinity >= 15 and self.salinity <= 20:  # Adding salinity conditions for growth
            #                             if self.current_velocity <= 0.5:  # Adding current velocity conditions for growth
            #                                 self.growth += self.growth_rate
            #         if self.nutrient_p > self.nutrient_p_threshold:
            #             if self.light >= 0.12 and self.light <= 0.37:  # Adding light conditions for growth
            #                 if self.temperature >= 13 and self.temperature <= 24:  # Adding temperature conditions for growth
            #                     if self.depth >= 1 and self.depth <= 6:  # Adding depth conditions for growth
            #                         if self.salinity >= 15 and self.salinity <= 20:  # Adding salinity conditions for growth
            #                             if self.current_velocity <= 0.5:  # Adding current velocity conditions for growth
            #                                 self.growth += self.growth_rate / 2  # Adjust as needed
            #         if self.nutrient_n > self.nutrient_n_threshold_for_reproduction:
            #             if self.light >= 0.12 and self.light <= 0.37:  # Adding light conditions for reproduction
            #                 if self.temperature >= 15 and self.temperature <= 20:  # Adding temperature conditions for reproduction
            #                     if self.depth >= 1 and self.depth <= 6:  # Adding depth conditions for reproduction
            #                         # Data for salinity conditions for reproduction is unavailable
            #                         self.reproduction += self.reproduction_rate
            # # Ensure the seagrass level doesn't exceed 1
            # self.grid[x][y][self.CB_IDX] = min(1, self.grid[x][y][self.CB_IDX])
        # Assuming you're inside the transition_rule function and currently processing a 'Seagrass' cell at position (x, y)
        # Spread/Reproduction
        if self.state[x][y] == 'Seagrass':
            # List of neighboring coordinates
            neighbors = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]

            for nx, ny in neighbors:
                # Ensure the neighbor coordinates are inside the grid boundaries
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.state[nx][ny] == 'Empty' and np.random.rand() < 0.2:  # 20% reproduction chance, for absecnt scenario increased probability (0.25)
                        self.state[nx][ny] = 'Germinating'  # or 'Seagrass' based on your model's logic
                
                return self.state[x][y]

        # print(f"Final state at ({x}, {y}): {self.state[x][y]}")   
        return self.state[x][y]
    

    # This function initializes the grid with some initial cells using a similar random chance mechanism as in transition_rule.
    # The Random initial growth Scenario 
    # def initialize_grid(self):  
    #     for i in range(self.height):  
    #         for j in range(self.width):  
    #             if np.random.rand() < 0.1: 
    #                 self.grid[i][j] = Cell.one_cell_run(0,self.grid[i][j])
    #                 self.state[i][j] = 'Germinating'
    #     # plt.imshow(self.grid, cmap='Greens')
    #     # plt.title('initial')
    #     # plt.show()
    #     # plt.pause(0.5)
    #     return self.grid
    
    # # The Central growth scenario
    # def initialize_grid(self):
    #     center_x, center_y = self.width // 2, self.height // 2
    #     radius = min(self.width, self.height) // 4  # Adjust the radius as needed
    #     for i in range(self.height):
    #         for j in range(self.width):
    #             if (center_x - j)**2 + (center_y - i)**2 <= radius**2:
    #                 self.state[i][j] = 'Seagrass'
    #             else:
    #                 self.state[i][j] = 'Empty'
    #     return self.grid
    
    # This function initializes the grid with clusters of seagrass at the start of the simulation. 
    # The clusters are arranged in a regular pattern with equidistant spacing.
    def initialize_grid(self):
        cluster_size = 5  # Adjust as needed
        cluster_spacing = 10  # Adjust as needed
        for i in range(self.height):
            for j in range(self.width):
                if (i // cluster_spacing) % 2 == (j // cluster_spacing) % 2 and \
                    i % cluster_spacing < cluster_size and j % cluster_spacing < cluster_size:
                    self.state[i][j] = 'Seagrass'
                else:
                    self.state[i][j] = 'Empty'
        return self.grid
    
    # # The Abesent Scenario
    # def initialize_grid(self):
    #     # Initialize the grid with all cells being empty
    #     for i in range(self.height):
    #         for j in range(self.width):
    #             self.state[i][j] = 'Empty'

    #     # Optionally, introduce some initial 'Seagrass' cells
    #     # For instance, setting the center of the grid as 'Seagrass'
    #     center_x, center_y = self.width // 2, self.height // 2
    #     self.state[center_x][center_y] = 'Seagrass'
    
    #     return self.grid
    
    # # Complete coverage Scenario
    # def initialize_grid(self):
    #     for i in range(self.height):
    #         for j in range(self.width):
    #             self.state[i][j] = 'Seagrass'
    #     return self.grid
           
    def evolution(self, num_of_steps, subplot = None):  
        # Create an empty grid to hold the seagrass counts
        seagrass_counts = np.zeros((self.height, self.width))
        flag_last = np.zeros((self.height, self.width))

        for m in range(num_of_steps):  
            #weekly loop
            for s in range(7):  
                for x in range(self.width):  
                    for y in range(self.height):  
                        # First let it evolve on its own (daily loop)
                        self.grid[x][y] = Cell.one_cell_run(s+1,self.grid[x][y])
            for x in range(self.width):  
                for y in range(self.height): 
                    # Then according to the transition rules to diffuse (monthly)
                    self.state[x][y] = self.transition_rule(x, y)
                    # Record the growth of seagrass here
                    # If the conditions for regrowth are met, the corresponding position of the result matrix +1
                    # Need to judge according to the transition rules

            
            # save the matrix  
            with open(f"./matrix/matrix_week={m}.pkl", "wb") as f:
                pickle.dump(self.grid, f)
            # print(f"Saved grid for week={m}")  # Print confirmation message
            # Read the matrix
            # with open("matrix_week=0.pkl", "rb") as f:  
                # loaded_grid = pickle.load(f)
            # print(f"Loaded grid for week={m}: {loaded_grid}")  # Print loaded grid
            if self.plot_results:
                flag_now = Cell.Have_seagrass(self.state, self.height, self.width)
                PlotResult(flag_now, m)
        #         seagrass_counts=get_result(flag_now, flag_last, seagrass_counts)
        #         PlotResult(seagrass_counts,m)
        #         flag_last = flag_now
        # return seagrass_counts
        return flag_now
