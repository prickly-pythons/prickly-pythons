# Matplotlib Demo 4
# histograms
# JDWest 10/19/2015

import matplotlib.pyplot as plt
import numpy as np

# load hourly Earth tide time series
Tide = np.load('Tide.npy')

# load barometric pressure time series
BP = np.load('BP.npy')

Count, Bin_Edges, Whatever = plt.hist(Tide + BP, bins=20, color='#99ccaa', alpha=0.5)

print Count

print Bin_Edges

print Whatever

# add labels
plt.xlabel("Combined Stress")
plt.ylabel("Number of Samples")

# and title
plt.title("Stress distribution")

# grid lines
plt.grid(True)


# trickery to make the plot come up maximized for presentation
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

plt.show()
