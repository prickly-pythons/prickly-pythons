print("Integrate spectrum")

# import modules
import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import quad
import scipy as scipy
from math import *
import matplotlib.pyplot as plt
import pandas as pd
import pdb as pdb                       # Python Debugger - pdb.set_trace() works as stop in IDL

# Some parameters
clight      =   299792458           # m/s
hplanck     =   4.135667662e-15     # eV*s
kpc2m       =   3.085677580666e19  # m
pc2cm       =   kpc2m*100/1000		# cm
plt.close('all')        # close all window

# Get data 
# (this is a spectrum from starburst99, solar metallicity, 1e6 solar masses population, Kroupa IMF, 100Msun/yr cons SFR)
columns     =   ['time','wavelength','ltot','lstellar','lnebular'] 
t1          =   100e6       # choosing a time stamp to look at   
xy	 		=   pd.read_pickle('test_data/spectrum.dat')
x 			=	xy['x']
y 			=	xy['y']

# Plot spectrum
fig         =   plt.figure(0)
ax2         =   fig.add_axes([0.15,0.1,0.75,0.8])
ax2.set_ylim(35,43)
ax2.set_xscale('log')
ax2.set_xlabel('Wavelength [AA]')
ax2.set_ylabel('log flux [erg/s/AA]')
ax2.set_title('Z=0.014, after 1e6 yr, 100 Msun/yr')#+str(t1)+' yr')
plt.plot(x,y,'b')
# The borders for Habing luminosity
int_range   =   clight*hplanck/np.array([13.6,6])*1e10  # eV -> AA
y1 			=	10**y[(x>int_range[0]) & (x<int_range[1])]
x1 			=	x[(x>int_range[0]) & (x<int_range[1])]
plt.plot([int_range[0],int_range[0]],[10,50],'g')
plt.plot([int_range[1],int_range[1]],[10,50],'g')
plt.show(block=False)

pdb.set_trace()
# Integrate spectrum (discrete data points) to get Habing luminosity in ergs/s
L_FUV 		=	scipy.integrate.simps(y1,x1)
print(L_FUV,' ergs/s')
# Convert to erg/s/cm^2, for a chosen distance (1 kpc)
distance 	=	1e3*pc2cm*100 					# cm
flux_FUV 	=	L_FUV/(4*np.pi*distance**2)
Habing 		=	2.74e-3 						# LAMDA [erg/s/cm^2]
print(flux_FUV/Habing,' Habing')


# Fit spectrum with power law:
def pl(x, a, b):
	return a * x**(b)
param, pcov = curve_fit(pl,x1.values,y1.values,p0=(1e42,-1))
print(param)
plt.plot(x1,np.log10(param[0]*x1**param[1]),'r')
plt.show(block=False)

# Integrate the functional fit:
L_FUV1 		=	quad(pl,int_range[0],int_range[1],args=(param[0],param[1]))
print('L_FUV from fit: ',L_FUV1[0],' ergs/s')
print('Error on integration: ',L_FUV1[1],' ergs/s')








