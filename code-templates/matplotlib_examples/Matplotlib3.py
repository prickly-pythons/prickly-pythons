# Matplotlib Demo 3
# scatter plots
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
ax1.set_ylabel('Barometric Pressure Stress (kPa)', fontsize=10, color='blue')
ax2 = ax1.twinx()
ax2.set_ylabel('Tidal Stress (kPa)', fontsize=10, color='green')

# plot it
ax1.scatter(x, BP, color='blue', marker='^', label='Barometric Pressure')
ax2.scatter(x, Tide, color='green', marker='*', label='Earth Tides')
ax1.scatter(x, BP + Tide, color='red', marker='+', label='Combined Stress')

# add labels
plt.xlabel("Hours", fontsize=10)

# and title
plt.title("Stress for 10-day period", fontsize=10 )

# grid lines
plt.grid(True)

# set the y axis to match range
xLow1, xHigh1, yLow1, yHigh1 = ax2.axis()
ax2.axis([xLow1, xHigh1, -3.0, 3.0])
xLow2, xHigh2, yLow2, yHigh2 = ax1.axis()
Avg2 = (yHigh2 + yLow2)/2
ax1.axis([xLow2, xHigh2, Avg2-3.0, Avg2+3.0])

# add legends
ax2.legend(loc='upper right')
ax1.legend(loc='upper left')

# trickery to make the plot come up maximized for presentation
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

plt.show()
