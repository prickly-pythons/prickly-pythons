# Submodule that uses multiprocessing and subprocess packages:
import multiprocessing as mp
import subprocess as sub

# Other packages we will need:
import numpy as np
import pandas as pd
import pdb as pdb
import time as time

def count():
	print('\nUse subprocess package to count list of files in directory')

	# step 1: list all files
	ls 			= 	sub.Popen('ls ', stdout=sub.PIPE,shell=True)
	
	# Let's see what's in the output (will close file):
	# print(ls.stdout.read())

	# step 2: do a wordcount on that output (while it's open):
	wc 			= 	sub.Popen('wc -l', stdin=ls.stdout, stdout=sub.PIPE, shell=True)

	out_count 	= 	int(wc.communicate()[0])
	print('There are ' + str(out_count) + ' files in this directory')
	ding 		=   sub.call(["afplay", 'Bike-Horn.mp3'])

	pdb.set_trace()

def split_gas_particles():
    print('\nSplit gas particles!')

	# For each gas particle in gas_particle dataframe, 
	# split the gas mass into smaller clumps (GMCs)
	# and place them at random distances from original gas particle.

    gas_particles   =   pd.read_pickle('gas_particles')

    # Setup pool of processors to use (8 processors on my Mac Pro...)
    start_time = time.time()

    pool            =   mp.Pool(processes=10)        
    M            	=   gas_particles['m'].values 		   # mass of gas particles
    h            	=   gas_particles['h'].values 		   # smoothing length of gas particles
    b               =   1.8                                # powerlaw slope [Blitz+07]
    frac_h          =   0.5                                # fraction of smoothing length within which to place GMCs
    Mmin            =   1.e4                               # min mass of GMC
    Mmax            =   1.e6                               # max mass of GMC
    tol             =   Mmin                               # precision in reaching total mass
    nn              =   100                                # max draw of masses in each run
    print('\nStart up multiprocessing!')
    results         =   [pool.apply_async(GMC_generator, args=(i,M,h,Mmin,Mmax,b,frac_h,tol,nn,)) for i in range(0,len(gas_particles))]
    # Extracting results to a list of length = number of gas particles:
    results         =   [p.get() for p in results]
    print('Done!')
    elapsed_time 	= 	time.time() - start_time
    print('Took: ' + str(elapsed_time) + ' seconds')
    ding 			=   sub.call(["afplay", 'Bike-Horn.mp3'])

    # Store output in separate lists:
    Mgmc            =   [results[i][1] for i in range(0,len(results))]
    newx            =   [results[i][2] for i in range(0,len(results))]
    newy            =   [results[i][3] for i in range(0,len(results))]
    newz            =   [results[i][4] for i in range(0,len(results))]

    print('\nEach result has a different length...')
    print('Mass of first gas particle [Msun]: ')
    print(M[0])
    print('Is divided into '+str(len(Mgmc[0]))+' GMCs')
    print('Masses of created GMCs [Msun]: ')
    print(Mgmc[0])
    print('Displacement of these GMCs in x direction [kpc]: ')
    print(newx[0])

    pdb.set_trace()



def GMC_generator(i,Mneu,h,Mmin,Mmax,b,frac_h,tol,nn):
    ra      =   np.random.rand(nn)  # draw nn random numbers between 0 and 1
    ra1     =   np.random.rand(nn)  # draw nn random numbers between 0 and 1
    ra2     =   np.random.rand(nn)  # draw nn random numbers between 0 and 1
    Mg      =   np.zeros(nn)
    newm_gmc     =   np.zeros(1)
    if Mneu[i] < Mmin+tol:
        newm_gmc         =   Mneu[i]
    if Mneu[i] > Mmin+tol:
        for ii in range(0,nn):
            k           =   (1/(1-b)*(Mmax**(1-b)-Mmin**(1-b)))**(-1) # Normalization constant (changing with Mmax)
            Mg[ii]      =   (ra[ii]*(1-b)/k+Mmin**(1-b))**(1./(1-b))        # Draw mass (from cumulative distribution function)
            if ii==0 and np.sum(newm_gmc)+Mg[ii] < Mneu[i]+tol:             # Is it the 1st draw and is the GMC mass below total neutral gas mass (M_neutral) available?
                newm_gmc         =   np.array(Mg[ii])                            # - then add that GMC mass
            if ii>0 and np.sum(newm_gmc)+Mg[ii] < Mneu[i]+tol:              # Is the sum of GMC masses still below M_neutral+tolerance?
                newm_gmc         =   np.append(newm_gmc,Mg[ii])                       # - then add that GMC mass
            # if np.sum(newm_gmc) > Mneu[i]-tol:                              # Is the sum of GMC masses above M_neutral-tolerance?
                # break                                                       # - fine! then stop here
    # Add SPH info to new DataFrame (same for all GMCs to this SPH parent)
    # Save indices of original SPH particles
    f1      =   np.size(newm_gmc)
    if f1 ==1:
        if newm_gmc == 0:
            print('No GMCs created for this one?')
            pdb.set_trace()
    SPHindex    =   np.zeros(f1)+i
    # but change coordinates!!
    ra_R        =   ra[0:f1]*frac_h*h[i]
    ra_phi      =   ra1[0:f1]*2*np.pi
    ra_theta    =   ra2[0:f1]*np.pi
    ra_sph      =   [ra_R*np.sin(ra_theta)*np.cos(ra_phi),+\
        ra_R*np.sin(ra_theta)*np.sin(ra_phi),+\
        ra_R*np.cos(ra_theta)]
    newx        =   np.array(ra_sph)[0,:]
    newy        =   np.array(ra_sph)[1,:]
    newz        =   np.array(ra_sph)[2,:]
    # Neutral mass that remains is distributed in equal fractions around the GMCs:
    return f1,newm_gmc,newx,newy,newz





