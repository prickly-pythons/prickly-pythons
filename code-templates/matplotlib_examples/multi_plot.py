# Matplotlib Demo 6
# subplots
# JDWest 10/19/2015

import matplotlib.pyplot as plt
import numpy as np
plt.close('all')        # close all windows

# load hourly Earth tide time series
Tide = np.load('Tide.npy')

# load barometric pressure time series
BP = np.load('BP.npy')

# subplot: 2 rows, 2 columns => 4 figures! 
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2,figsize=(10,8))


### 1st subplot figure! 

# plot histogram
ax1.hist(Tide + BP, bins=20, color='#ff6600', alpha=0.5)

# add labels + title
ax1.set_xlabel("Combined Stress")
ax1.set_ylabel("Number of Samples")
ax1.set_title("Distribution of Stress Measurements")

# grid lines
ax1.grid(True)

### 2nd subplot figure! 

# x axis is just hours, one per sample
x = np.arange(len(Tide))

# scatter plot tides
ax2.scatter(x, Tide, color='green', marker='^')

# add labels + title
ax2.set_xlabel("Hours")
ax2.set_ylabel("Stress (kPa)")
ax2.set_title("Tidal Stress vs Time")

### 3rd subplot figure! 

# plot barometric pressure
ax3.plot(x, BP, color='blue', linewidth = 1.5)

# add labels + title
ax3.set_xlabel("Hours")
ax3.set_ylabel("Stress (kPa)")
ax3.set_title("Barometric Pressure vs Time",fontsize=13)

### 4th subplot figure! 

# plot just the first 24 hours
BP = BP[0:24]

# offset by 100 kPa
BP = BP - 100

# x axis is just hours, one per sample
x = np.arange(len(BP))

# plot bar chart
ax4.bar(x, BP, facecolor='#660099', edgecolor='green', alpha=0.5)

# add labels + title
ax4.set_xlabel("Time (hours)")
ax4.set_ylabel("Barometric Pressure + 100kPa")
ax4.set_title("Barometric Pressure Bar Chart")

# grid lines
ax4.grid(True)

### Alternative 4th subplot figure! 

# import matplotlib.image as mpimg

# # Load image of NGC 2997 from ESO: https://www.eso.org/public/images/eso9921a/
# img = mpimg.imread('NGC_2997.jpg')

# ax4.imshow(img,extent=(0,3.4,0,3.4)) 	# image size from webpage
# ax4.locator_params(nbins=6)	# number of ticks
# ax4.set_xlim(0,3.4) # force axes range (no whitespace!)
# ax4.set_ylim(0,3.4) # force axes range (no whitespace!)

# x_axis = ax4.xaxis.get_ticklocs()
# y_axis = ax4.yaxis.get_ticklocs()

# # Move center:
# x_center = 1.067389
# y_center = 1.285878
# # Put x on center
# ax4.plot(x_center,y_center,'x',mew=2,ms=5)
# x_axis = x_axis-x_center
# y_axis = y_axis-y_center
# ax4.xaxis.set_ticklabels(['%.3f' %x1 for x1 in x_axis])
# ax4.yaxis.set_ticklabels(['%.3f' %y1 for y1 in y_axis])

# # Put center in title, ra: 09h 45m 38.8s, dec:-31deg 11sec 28arcsec
# ax4.set_xlabel("Degrees")
# ax4.set_ylabel("Degrees")
# ax4.set_title("RA: 09h 45m 38.8s, DEC:-31$^o$ 11' 28arcsec''",fontsize=13)

# Some ideas to put coordinates on ALL tick marks
# astropy SkyCoord: http://www.astropy.org/astropy-tutorials/Coordinates.html
# from astropy.coordinates import SkyCoord
# from astropy import units as u
# center_NGC2997 = SkyCoord('9:45:38.8 -31:11:28',unit=(u.hour, u.deg), frame='icrs')	# galaxy center in degrees
# x_axis = x_axis+center_NGC2997.ra.arcmin
# y_axis = y_axis+center_NGC2997.dec.arcmin
# axes = SkyCoord(x_axis*u.arcmin, y_axis*u.arcmin, frame='icrs')
# print(axes.ra)
# print(axes.dec)
# ax4.xaxis.set_ticklabels(axes.ra)
# ax4.yaxis.set_ticklabels(axes.dec)

# Get center position in pixels:
def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

# for better layout

fig.tight_layout()

# show your work
plt.show(block=False)
