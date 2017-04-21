import numpy as np
import matplotlib.pyplot as plt
#import os
#os.chdir(u'/Users/luciaperez/Documents/ASUResearch/LyAVPF/angcor/MonteCarloRuns')

plt.close('all')

Wavg31=np.load('Wavgfor31.npy')
Wavg66=np.load('Wavgfor66.npy')

Wsigma31=np.load('Wsigma31.npy') 
Wsigma66=np.load('Wsigma66.npy')  


#a power law relationship looks linear on a log-log plot
logRs31=np.log10(Wsigma31[2:60,0])
logWs31=np.log10(Wavg31[2:60])
logRs66=np.log10(Wsigma66[3:25,0])
logWs66=np.log10(Wavg66[3:25])
#print logWs


#-----------    FIX SLOPE!!!    -------------------
#create line that intercepts zero with slope 1.8, and lift each point by the corresponding \
#value in the data
Guess31=logWs31 + 1.8*logRs31

#I guess an average value for the y-intercept of the curve, by seeing the average \
#y-value for the whole data set
IntFit31=np.mean(Guess31)

#I use polyfit to see how well my guess curve matches the data with a 0 dimensional fit--just a straight line?
refit31=np.polyfit(logRs31,Guess31,0,w=Wsigma31[2:60,1])
Fit31E=-1.8*logRs31+refit31[0]
Fit31NE=-1.8*logRs31+IntFit31
print refit31
print 'Guess for the y intercept, IntFit: ',IntFit31
print '3.1 Ro = ',10.**(refit31[0]/1.8)

Guess66=logWs66 + 1.8*logRs66
IntFit66=np.mean(Guess66)
refit66=np.polyfit(logRs66,Guess66,0,w=Wsigma66[3:25,1])
Fit66E=-1.8*logRs66+refit66[0]
Fit66NE=-1.8*logRs66+IntFit66
print refit66
print 'Guess for the y intercept, IntFit: ', IntFit66
print '6.6 Ro = ',10.**(refit66[0]/1.8)

#-----------    DON'T FIX SLOPE!!!    -------------------
#This time, fit something in the form of y = mx + b
coefficients31 = np.polyfit(logRs31, logWs31, 1,w=Wsigma31[2:60,1])
polynomial31 = np.poly1d(coefficients31)
ys31 = polynomial31(logRs31)

coefficients66a = np.polyfit(logRs66, logWs66, 1) #No error!
polynomial66a = np.poly1d(coefficients66a)
ys66a = polynomial66a(logRs66)
coefficients66b = np.polyfit(logRs66, logWs66, 1,w=Wsigma66[3:25,1])
polynomial66b = np.poly1d(coefficients66b)
ys66b = polynomial66b(logRs66)

print 'Point-slope form for 3.1: ',polynomial31
print 'Point-slope form for 6.6, no errors: ',polynomial66a
print 'Point-slope form for 6.6, errors: ',polynomial66b


#-------

plt.close()  
plt.figure(1,figsize=(10,7))

plt.plot(np.log10(Wsigma31[:,0]),np.log10(Wavg31[:]),'k.', linestyle='-', label='Mine, 3.1')
plt.errorbar(np.log10(Wsigma31[:,0]),np.log10(Wavg31[:]),Wsigma66[:])
plt.plot(logRs31,Fit31E,'r-',linewidth=2,label='Fixed slope, with error')
plt.plot(logRs31,Fit31NE,'b-',linewidth=2,label='Fixed slope, no error')
plt.plot(logRs31,ys31,'g-',linewidth=2,label=polynomial31)

plt.title('Linear fit of Two Point Correlation Function, z=3.1')
plt.xlabel('log_10 of Angular Distances, in Comoving MPc')
plt.ylabel('log_10 of W')
plt.legend(loc='lower left')
plt.show()

plt.figure(2,figsize=(10,7))
plt.plot(np.log10(Wsigma66[:,0]),np.log10(Wavg66[:]),'k.', linestyle='-', label='Mine, 6.6')
plt.plot(logRs66,Fit66E,'r-',linewidth=2,label='Fixed slope, with error')
plt.plot(logRs66,Fit66NE,'b-',linewidth=2,label='Fixed slope, no error')
plt.plot(logRs66,ys66a,'g-',linewidth=2,label=polynomial66a)
plt.plot(logRs66,ys66b,'c-',linewidth=2,label=polynomial66b)
plt.plot(0,0,'w',label='green is w/ no error, cyan includes them')

plt.title('Linear fit of Two Point Correlation Function, z=6.6')
plt.xlabel('log_10 of Angular Distances, in Comoving MPc')
plt.ylabel('log_10 of W')
plt.legend(loc='lower left')
plt.show()