import matplotlib.pyplot as plt
import numpy as np

pitch_opt=np.load("pitch_opt.npy")
plt.ion() # turn on interactive mode
for p in pitch_opt:
	plt.imshow(p, vmin=pitch_opt.min(), vmax=pitch_opt.max())
	plt.show()
	raw_input("Press any key to show the next image.")
