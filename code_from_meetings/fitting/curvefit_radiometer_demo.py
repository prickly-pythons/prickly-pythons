import numpy as nm
import matplotlib.pyplot as pl

def model_of_p(theta,g,Tsys,Tatm,Tbg,tau):
	# define output array
	p_out = nm.zeros_like(theta)

	# define the secant function, and conversion from degrees
	def sec(theta):
		return 1.0/nm.cos(theta*(nm.pi/180.0))

	for i in xrange(len(theta)):
		if theta[i]==-2:
			# special case if theta=-2, that's a flag, so assume T=293 K
			p_out[i] = g*(Tsys + 293.0)
		elif theta[i]==-1:
			# another special case if theta=-1, that's a flag, so assume T=393 K
			p_out[i] = g*(Tsys + 393.0)
		else:
			# if theta is some usual value, that isn't a flag, so use the real formula
			p_out[i] = g*(Tsys + Tatm*(1.0 - nm.exp(-tau*sec(theta[i]))) + Tbg*nm.exp(-tau*sec(theta[i])))

	return p_out

# choose angles from horizontal to vertical
theta_min = 0.0
theta_max = 90.0
n_angles = 91
theta_obs  = nm.linspace(theta_min,theta_max,num=n_angles)

# annoying bookkeeping
# each observation should:
#   -look at the room temp reference
#   -then look at the hot load reference
#   -then look at the sky
# so, make an array interleaved like that
angles = []
on_sky = []
for i in xrange(len(theta_obs)):
	angles.append(-2.0)
	angles.append(-1.0)
	angles.append(theta_obs[i])
	on_sky.append(False)
	on_sky.append(False)
	on_sky.append(True)
# convert from list to numpy array
angles = nm.array(angles)
on_sky = nm.array(on_sky)

# set the noise level in K
noise = 0.1

# set the true parameters, to be used to simulate some fake data
g=1.0 # gain, in radiometer output per kelvin of input
Tsys=500.0 # noise level of radiometer
Tatm=20.0 # physical temperature of the gasses in the atmosphere
Tbg=2.725 # physical temperature of the cosmic microwave background
tau=0.05 # atmospheric transmission, in tau units
params_in = nm.array([g,Tsys,Tatm,Tbg,tau])
# print out the input parameters
print 'Actual Atmospheric Properties'
print 'Tatm = '+str(Tatm)+' K'
print 'atm_tx = '+str(nm.exp(-tau)*100.0)+'%'
print ' '


# make the fake data, with noise
p_mes = model_of_p(angles,*params_in) + noise*nm.random.randn(len(angles))

# fit this fake data to the model using curvefit
from scipy.optimize import curve_fit
p_mean, pcov = curve_fit(model_of_p, angles, p_mes, bounds=([0.1,400.0,1.0,2.6,0.0001],[10.0,600.0,150.0,6.0,0.5]) )
# get the diagonal values of the covariance matrix
# and convert to "standard deviation" by taking the square root
p_std = nm.diag(nm.sqrt(pcov))

# take these best parameters, and do a variable change to measured transmission
atm_tx_meas = nm.exp(-p_mean[4])
sigma_atm_tx = nm.exp(-p_mean[4])*p_std[4]
T_atm_meas = p_mean[2]
sigma_T_atm = p_std[2]
# print out the measured results
print 'Measures Atmospheric Properties with '+str(len(theta_obs))+' 3-second data points'
print 'Tatm = '+str(T_atm_meas)+' +/- '+str(sigma_T_atm)+' K'
print 'atm_tx = '+str(atm_tx_meas*100.0)+'% +/- '+str(sigma_atm_tx*100.0)+'%'
print ' '

# make a plot of the fake data and the best fit
pl.ion()
pl.plot(angles[on_sky],p_mes[on_sky],'*',label='Data')

pl.plot(angles[on_sky],model_of_p(angles[on_sky],*p_mean),label='Best-fit')
pl.xlabel('Angle from Zenith [deg]')
pl.ylabel('Apparent Temperature at Radiometer [K]')

pl.xticks([0,10,20,30,40,50,60,70,80,90])
pl.yticks([502.5,505,507.5,510,512.5,515,517.5,520])


# annotate with limiting cases
T_zenith = Tsys+Tbg*nm.exp(-tau)+Tatm*(1.0-nm.exp(-tau))
pl.plot([0,90],[T_zenith,T_zenith],':',label='Zenith Temperature (~$T_{sys}$ + $T_{bg}$)')
T_horizon = Tsys+Tatm
pl.plot([0,90],[T_horizon,T_horizon],':',label='Horizon Temperature ($T_{sys}$+$T_{atm}$)')
pl.legend()