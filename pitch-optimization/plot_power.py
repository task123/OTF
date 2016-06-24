import matplotlib.pyplot as plt
import numpy as np

power = np.load("power.npy")
plt.plot(np.linspace(0,200,len(power)), power)
plt.show()
