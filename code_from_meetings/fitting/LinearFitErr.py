import numpy as np
import scipy
import scipy.optimize
import math
import matplotlib.pyplot as plt
#--------------------------------------


#---------------------------------------------------------------
# Read input file with columns x, y, xerror, yerror
fn = 'cooltemp.dat'
xb, yb, xerror, yerror = np.loadtxt(fn,unpack=True, usecols=[0,1,2,3])
#---------------------------------------------------------------




#------------------------------------------------------------
#Plot data only
plt.plot(xb, yb, 'ro', markersize=12)
#------------------------------------------------------------


#------------------------------------------------------------
# Do a linear fit; no error bars included
a1, b1 = np.polyfit(xb, yb, 1)
plt.plot(xb, a1*xb + b1, 'r') 
#------------------------------------------------------------


#------------------------------------------------------------
#Plot data with error bars
plt.errorbar(xb, yb, fmt='ro', label="data",
             xerr=0.3, yerr=yerror, ecolor='black')
#------------------------------------------------------------


#----------------------------------------------------------------
# Now do the linear fit using Y-errors
f = lambda x, a, b: a*x + b  # function to fit


# Initial  guess for parameters [1, 1]
pars, corr = scipy.optimize.curve_fit(f, xb, yb, [1, 1], yerror)
a2, b2 = pars

plt.plot(xb, a2*xb + b2, 'b')
#----------------------------------------------------------------

plt.show()
