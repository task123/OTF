import matplotlib.pyplot as plt
import numpy as np

name = input("Type in the name of the file you want to plot with fileending
        .npy:")
pitch_opt=np.load(name)
n_turbines_x = input("Type in number of turbines in x direction:")
n_turbines_y = input("Type in number of turbines in y direction:")
for i in range(0,len(pitch_opt)):
    for x in range(0, n_turbines_x):
        for y in range(0, n_turbines_y):
            plt.

