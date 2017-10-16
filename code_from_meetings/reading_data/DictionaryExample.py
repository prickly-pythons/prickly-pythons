#DICTIONARIES AS DATA USE AND STORAGE OPTIONS
import numpy as np
import random as rd

def TwoDimVPF(array,NumberofMCruns,Radiusarray,DirectiontoUse):
    '''Here's how you indicate that you're creating a dictionary.'''
    currentVPF={} 
    
    points=len(array)
    randomcircles=3*len(array)
    if DirectiontoUse==0:
        size=np.amax(array[:,0])
    elif DirectiontoUse==1:
        size=np.amax(array[:,1])
    elif DirectiontoUse != 0 or 1:
        sys.exit("The fourth input should be whichever of your axes is the smallest.")
    for d in np.arange(0,NumberofMCruns):
        Radii=[]
        for R in Radiusarray:
            cx=[]
            cy=[]
            for e in np.arange(0,randomcircles,1):
                cx.append(rd.randint(int(0+10000*R),int(size*10000.-10000.*R))/10000.)
                cy.append(rd.randint(int(0+10000*R),int(size*10000-10000.*R))/10000.)
                e+=1
            cx=np.array(cx)
            cy=np.array(cy)
            Voids=0
            for f in np.arange(0,randomcircles,1):
                for g in np.arange(0,points):
                    if (cx[f]-array[g,0])**2 + (cy[f]-array[g,1])**2  <= R**2:
                        break
                else:
                    Voids=Voids+1.
                #break
            R=float(R)
            VPF=float(Voids/randomcircles)
            
            Radii.append([R,VPF]) 
            '''Every loop of this makes its own array! Not easy to combine into one MEGA-
            array, so a dictionary is the best option.'''
            
            
        currentVPF[d]=Radii
        '''Now I'm creating a new entry in my dictionary whose KEY (identifying name) 
        is d [my current count], and whose VALUE is the array of data I want 
        [my calculations]. Pros: the arrays don't all have to be the same shape!'''
        
    print 'VPF successfully completed! Output is a dictionary.'
    return currentVPF

newXs=(np.random.uniform(0,100,100))
newYs=(np.random.uniform(0,100,100))
inputarray=np.array([newXs,newYs])

Dictionary=TwoDimVPF(inputarray, 10, np.arange(0,10,1),0)
np.save('TestDict.npy',Dictionary)

'''Here, the key is my count, goes from 0 to 9, and it's associated with an array 
that I calculated. Normally, keys are strings, but I made them numbers for ease.'''

print Dictionary
print Dictionary.keys()
print Dictionary.values()

'''Here's how you iterate through a dictionary as generally as possible! First,
be CAREFUL how you load the dictionary! Without the .item(), it assumes it's an
array of no dimentionsand it can't iterate through them or read it.'''
Dictionary=np.load('TestDict.npy').item()
#Dictionary=np.load('TestDict.npy').iteritems()
#Dictionary=np.load('TestDict.npy')

#print Dictionary.shape
print type(Dictionary)
print len(Dictionary)

def AverageVPFandSigma(DictofVPFS):
    """
    Takes a dictionary with all of your Monte Carlo runs of the VPF, 
    and gives you an array with the average VPF calculation for each radius.
    Module assumes that the dictionary has keys that are just counting what run you're on,
    and each array for the key has the 0th column as the radii tested (same across
    all MC runs) and has the 1st column as the VPF calculation.
    """
    Base=np.array(DictofVPFS[0])
    vpfs=np.empty([len(Base),len(DictofVPFS)+1])
    sigma=np.empty([len(Base),2])
    vpfs[:,0]=Base[:,0]
    sigma[:,0]=Base[:,0]
    averaged=np.zeros([len(Base),2])
    averaged[:,0]=Base[:,0]
    a=1
    
    '''.iteritems() is how you have python go through each key and value pair 
    in the dictionary, giving you each separately. To get the key and pair in a 
    list together, use .items() instead.'''
    for key, array in DictofVPFS.iteritems():
               
        #print key,array
        #VPFS=np.array(Dict31Aa[key])
        VPFS=np.array(array)
        vpfs[:,a]=VPFS[:,1]
        averaged[:,1]=averaged[:,1]+VPFS[:,1]
        a+=1
    averaged[:,1]=averaged[:,1]/len(DictofVPFS)
    for b in np.arange(0,len(Base),1):  
        sigma[b,1]=np.std(vpfs[b,1:])
    return averaged,sigma

averages,sigma=AverageVPFandSigma(Dictionary)
print averages, sigma