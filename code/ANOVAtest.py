"""
Script Name: ANOVA Analysis of Growth Count Matrices

Description:
This Python script is designed to perform one-way Analysis of Variance (ANOVA) on multiple matrices of growth count data.
It reads data from a CSV file and processes it to calculate the F-statistic and significance probability value.
The purpose is to test if there are any statistically significant differences between the means of the different groups.

Dependencies:
- SciPy for statistical calculations
- pandas for data manipulation

Functions:
- flatten(matrix): Flattens a 2D matrix into a 1D list
- ANOVA(*matrixs): Performs ANOVA on multiple 2D matrices

Usage:
1. Ensure that you have the required libraries installed.
2. Place the CSV file of the experiment in the same directory as this script.
3. Run the script.

Example:
An example is provided within the script to demonstrate its usage. Uncomment it to see how it works.
"""
__appname__ = 'ANOVAtest'
__author__ = 'ANQI WANG (aw222@ic.ac.uk)'
__version__ = '0.0.1'
__license__ = "None"

from scipy import stats  # Import stats module from scipy library for statistical calculations
import pandas as pd  # Import pandas library for data manipulation

# Define a function to flatten a 2D matrix into a 1D list
def flatten(matrix):
    '''
    Flatten a 2D matrix into a 1D list
    '''
    result = []
    for sublist in matrix:
        result += sublist  # Append each element of the sublist to the result list
    return result

# Define a function to perform ANOVA on multiple matrices
def ANOVA(*matrixs):
    '''
    Take the final results of growth count matrices and perform ANOVA analysis on multiple matrices
    '''
    flatten_matrixs = []
    for matrix in matrixs:
        # Flatten each matrix into a 1D list and store in a new variable
        flatten_matrixs.append(flatten(matrix))
    anova_table = stats.f_oneway(*flatten_matrixs)  # Perform one-way ANOVA
    print(anova_table)  # Directly print the result

# Read experimental data from a CSV file
data1 = pd.read_csv('ExperimentName.csv')  
ANOVA(data1)

# Test code:
# Define example data for groups
# group1 = [[12], [13], [11], [14], [10]]   
# group2 = [[10], [15], [9], [12], [11]]   
# group3 = [[14], [16], [15], [17], [13]]

# Comment explaining F-statistic and significance probability value
'''
F: F-statistic, the ratio of the between-group mean square to the within-group mean square.
Pr(>F): Significance probability value, used to evaluate the probability of the null hypothesis being true.
If the significance probability value is less than 0.05, the null hypothesis can be rejected, indicating that there is a significant difference in the means of the groups.
'''
# stats_analysis(group1, group2, group3)  # Last result indicates F-statistic and significance probability value
