# Matplotlib Demo 2
# additional axis, colors
# JDWest 10/19/2015

import matplotlib.pyplot as plt
import numpy as np

# load hourly Earth tide time series
Tide = np.load('Tide.npy')

# load barometric pressure time series
BP = np.load('BP.npy')

# x axis is just hours, one per sample
x = np.arange(len(Tide))

# create multiple y axes
fig, ax1 = plt.subplots()
ax1.set_ylabel('Barometric Pressure Stress (kPa)', color='blue')
ax2 = ax1.twinx()
ax2.set_ylabel('Tidal Stress (kPa)', color='green')

# plot it
#~ ax1.plot(x, BP, color='blue', linewidth = 1.5)
#~ ax2.plot(x, Tide, color='green', linewidth=1.5)

#~ ax1.plot(x, BP + Tide, color='red', linewidth=1.5)
#~ 
ax1.plot(x, BP, color='blue', linewidth = 1.5, linestyle='--', label='Barometric Pressure')
ax2.plot(x, Tide, color='green', linewidth=1.5, linestyle = '--', label='Earth Tides')
ax1.plot(x, BP + Tide, color='red', linewidth=1.5, label='Combined Stress')

# add labels
plt.xlabel("Hours", fontsize=10)
#~ plt.ylabel("Radial Stress (kPa)")

# and title
plt.title("Stress for 10-day period")

# grid lines
plt.grid(True)

# set the y axis to match range
xLow1, xHigh1, yLow1, yHigh1 = ax2.axis()
ax2.axis([xLow1, xHigh1, -3.0, 3.0])
xLow2, xHigh2, yLow2, yHigh2 = ax1.axis()
Avg2 = (yHigh2 + yLow2)/2
ax1.axis([xLow2, xHigh2, Avg2-3.0, Avg2+3.0])
#~ 
#~ # add legends
ax2.legend(loc='upper right')
ax1.legend(loc='upper left')

# trickery to make the plot come up maximized for presentation
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

plt.show()
