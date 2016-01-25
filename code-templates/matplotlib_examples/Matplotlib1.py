# Matplotlib Demo 1
# basic line plotting
# JDWest 10/19/2015

import matplotlib.pyplot as plt
import numpy as np

# load hourly Earth tide time series
Tide = np.load('Tide.npy')

# x axis is just hours, one per sample
x = np.arange(len(Tide))

print Tide
print x

# plot it
plt.plot(x, Tide)

# add labels
plt.xlabel("Hours", fontsize='large')
plt.ylabel("Radial Stress (kPa)", fontsize='large')

# and title
plt.title("Stress for 10-day period\nThis is a new line\n3rd line", fontsize=24)

plt.tick_params(labelsize=24, width=5)
plt.minorticks_on()

# grid lines
plt.grid(True)

#~ plt.tight_layout()

# trickery to make the plot come up maximized for presentation
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

plt.show()
