# Matplotlib Demo 6
# subplots
# JDWest 10/19/2015 (modified by kpolsen 01/25/16)

import matplotlib.pyplot as plt
import numpy as np
plt.close('all')        # close all windows

# load hourly Earth tide time series
Tide = np.load('Tide.npy')

# load barometric pressure time series
BP = np.load('BP.npy')

# subplot: ONE figure
fig, ax1 = plt.subplots()

# plot histogram
ax1.hist(Tide + BP, bins=20, color='#ff6600', alpha=0.5)

# add labels + title
ax1.set_xlabel("Combined Stress")
ax1.set_ylabel("Number of Samples")
ax1.set_title("Distribution of Stress Measurements")

# grid lines
ax1.grid(True)

# show your work
plt.show(block=False)
