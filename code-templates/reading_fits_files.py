print('-- ')
print('-- Read and visualize fits (Flexible Image Transport System) file')
print('-- ')

# Modules
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pdb as pdb

# Close all windows
plt.close('all') 

# Read fits file (simulated HCO+ data cube of cloud, calculated with RT code LIME)
data 		=	fits.open('test_data/cloud.fits')
#pdb.set_trace()
data.info()				# get basic info
print(data[0].header)	# get header
imgres 		=	data[0].header['CDELT2']			
print('Image resolution: ',imgres,' degrees')
npix 		=   data[0].header['NAXIS1']			
print('Number of pixels on each side: ',npix)
velres 		=	data[0].header['CDELT3']			
print('Velocity resolution [m/s]: ',velres)
HCO_flux 	=	data[0].data 						# [velocity channels, x axis, y axis]
print(HCO_flux[:,50,50])
mom0 		=	HCO_flux.sum(axis=0)*velres/1000 	# moment 0 map, Jy*km/s

# Contour plot of data cube
#plt.figure(1)
fig         =   plt.figure(1,figsize=(13,13))
# fig, ax1 	=	plt.figure(1)???
ax1         =   fig.add_axes([0.15,0.1,0.75,0.8],ylabel="y ['']")
cax			=	fig.add_axes([0.9,0.1,0.05,0.8])
ax1.set_xlabel("x ['']")
#ax1.set_ylabel("y ['']")
ax1.set_title("Moment 0 map of HCO$^+$ gas cloud")
x1 			=	imgres*(np.arange(npix)-npix/2) # image axis
xmax 		= 	max(x1)
im 			=	ax1.imshow(mom0,interpolation='bilinear',origin='lower',cmap=cm.hot,extent=(-xmax,xmax,-xmax,xmax),vmax=120)
plt.colorbar(im,cax=cax)
plt.show(block=False)