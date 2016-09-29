print('-- ')
print('-- Read data files in different formats')
print('-- ')

# Modules
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import fits
import matplotlib.cm as cm
import pdb as pdb

# Close all windows
plt.close('all') 

print('ascii files!')
# (spectrum.dat is a spectrum from starburst99, 0.7 x solar metallicity, 1e4 solar masses population, Kroupa IMF, starburst 10e6 years ago)


print('Read data into numpy array!')
spectrum1    =   np.loadtxt('test_data/spectrum2.dat',skiprows=6)
print(type(spectrum1))

print('Read data into pandas dataframe!')
spectrum2    =   pd.read_table('test_data/spectrum2.dat',names=['time','wavelength','L_tot','L_stellar','L_nebular'],skiprows=6,sep=r"\s*",engine='python')    
print(type(spectrum2))

spectrum3    =   np.genfromtxt('test_data/spectrum2.dat',skip_header=6,dtype=None,names=['time','wavelength','L_tot','L_stellar','L_nebular'])
print(type(spectrum3))

pdb.set_trace()
# Saving a dataframe to use it later:
spectrum2.to_pickle('test_data/spectrum.dataframe')
spectrum2    =   pd.read_pickle('test_data/spectrum.dataframe')    

# Plot spectrum
fig          =   plt.figure(0)
ax2          =   fig.add_axes([0.15,0.1,0.75,0.8])
ax2.set_ylim(31,39)
ax2.set_xlim(1e2,1e6)
ax2.set_xscale('log')
ax2.set_xlabel('Wavelength [AA]')
ax2.set_ylabel('log flux [erg/s/AA]')
ax2.set_title('1e4 M$_{\odot}$ of stars with Z=0.008 after 10e6 yr')#+str(t1)+' yr')
# plt.plot(spectrum1[:,1],spectrum1[:,2],'b')
plt.plot(spectrum2['wavelength'],spectrum2['L_tot'],'b')
plt.show(block=False)

# And we save in postscript!!
fig.savefig('plots/spectrum.eps',dpi=300)

print('Fits files!')
# (cloud.fits is a simulated HCO+ data cube of a cloud, calculated with RT code LIME)

# Read fits file into HDU (Header Data Unit) list-like Python opject
data 		=	fits.open('test_data/cloud.fits')
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
fig         =   plt.figure(1,figsize=(9,9))
ax1         =   fig.add_axes([0.15,0.1,0.75,0.8],ylabel="y ['']")
ax1.set_xlabel("x ['']")
ax1.set_ylabel("y ['']")
ax1.set_title("Moment 0 map of HCO$^+$ gas cloud")
x1 			=	imgres*(np.arange(npix)-npix/2) # image axis
xmax 		= 	max(x1)
im 			=	ax1.imshow(mom0,interpolation='bilinear',origin='lower',cmap=cm.hot,extent=(-xmax,xmax,-xmax,xmax),vmax=120)
cax			=	fig.add_axes([0.9,0.1,0.05,0.8])
plt.colorbar(im,cax=cax)
plt.show(block=False)







