# Matplotlib Demo 5
# bar chart
# JDWest 10/19/2015

import matplotlib.pyplot as plt
import numpy as np

# load barometric pressure time series
BP = np.load('BP.npy')

# plot just the first 24 hours
BP = BP[0:24]

# offset by 100 kPa
BP = BP - 100

# x axis is just hours, one per sample
x = np.arange(len(BP))

# plot bar chart
plt.bar(x, BP, facecolor='#660099', edgecolor='green')

# add labels
plt.xlabel("Time (hours)")
plt.ylabel("Barometric Pressure + 100kPa")
# plot title
plt.title("Barometric Pressure Bar Chart")

# grid lines
plt.grid(True)

# trickery to make the plot come up maximized for presentation
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

# show your work
plt.show()
