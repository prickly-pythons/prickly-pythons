# Matplotlib Demo 6
# subplots
# JDWest 10/19/2015

import matplotlib.pyplot as plt
import numpy as np

# load hourly Earth tide time series
Tide = np.load('Tide.npy')

# load barometric pressure time series
BP = np.load('BP.npy')

# subplot: 2 rows, 2 columns, first figure
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)

# plot histogram
ax1.hist(Tide + BP, bins=20, color='#ff6600', alpha=0.5)

# add labels
ax1.set_xlabel("Combined Stress")
ax1.set_ylabel("Number of Samples")
# plot title
ax1.set_title("Distribution of Stress Measurements")

# grid lines
ax1.grid(True)

# second subplot figure
#~ plt.subplot(2,2,2)

# x axis is just hours, one per sample
x = np.arange(len(Tide))

# scatter plot tides
ax2.scatter(x, Tide, color='green', marker='^')

# add labels
ax2.set_xlabel("Hours")
ax2.set_ylabel("Stress (kPa)")
# plot title
ax2.set_title("Tidal Stress vs Time")

# third subplot figure
#~ ax2.subplot(2,2,3)

# plot barometric pressure
plt.plot(x, BP, color='blue', linewidth = 1.5)

# add labels
plt.xlabel("Hours")
plt.ylabel("Stress (kPa)")
# plot title
plt.title("Barometric Pressure vs Time")

# fourth subplot figure
plt.subplot(2,2,4)

# bar chart
# plot just the first 24 hours
BP = BP[0:24]

# offset by 100 kPa
BP = BP - 100

# x axis is just hours, one per sample
x = np.arange(len(BP))

# plot bar chart
plt.bar(x, BP, facecolor='#660099', edgecolor='green', alpha=0.5)

# add labels
plt.xlabel("Time (hours)")
plt.ylabel("Barometric Pressure + 100kPa")
# plot title
plt.title("Barometric Pressure Bar Chart")

# grid lines
plt.grid(True)


# trickery to make the plot come up maximized for presentation
# figManager = plt.get_current_fig_manager()
# figManager.window.showMaximized()

# show your work
plt.show(block=False)
