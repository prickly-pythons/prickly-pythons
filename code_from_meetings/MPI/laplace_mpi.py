"""****************************************************************
 * Laplace MPI Template Python Version                                         
 *                                                               
 * T is initially 0.0                                            
 * Boundaries are as follows                                     
 *                                                               
 *                T                      4 sub-grids            
 *   0  +-------------------+  0    +-------------------+       
 *      |                   |       |                   |           
 *      |                   |       |-------------------|         
 *      |                   |       |                   |      
 *   T  |                   |  T    |-------------------|             
 *      |                   |       |                   |     
 *      |                   |       |-------------------|            
 *      |                   |       |                   |   
 *   0  +-------------------+ 100   +-------------------+         
 *      0         T       100                                    
 *                                                                 
 * Each PE only has a local subgrid.
 * Each PE works on a sub grid and then sends         
 * its boundaries to neighbors.
 *                                                                 
 *  Exercise by John Urbanic, PSC 2014, translated from C to Python by Karen Olsen
 *
 *******************************************************************"""

import numpy as np
from mpi4py import MPI
import time
# Not sure the following is necessary, but see : https://stackoverflow.com/questions/40951782/mpi4py-does-not-speed-up-embarrisingly-parallelizable-code
import mkl
mkl.set_num_threads(1) 

COLUMNS             =   1000                    # this is a "global" column count
ROWS_GLOBAL         =   1000                    # this is a "global" row count
NPES                =   4                       # number of processors
ROWS                =   (ROWS_GLOBAL/NPES)      # number of real local rows

# communication tags
DOWN                =   100
UP                  =   101   

MAX_TEMP_ERROR      =   0.01

# Set up arrays for current temperature and last-iteration temperature:
Temperature         =   np.zeros([ROWS+2,COLUMNS+2])
Temperature_last    =   np.zeros([ROWS+2,COLUMNS+2])

# only called by last PE
def track_progress(iteration,Temperature):

    print("---------- Iteration number: %i ------------\n" % iteration)

    # output global coordinates so user doesn't have to understand decomposition
    for i in np.arange(5)[::-1]:
      print("[%d,%d]: %5.2f  " % (ROWS_GLOBAL-i, COLUMNS-i, Temperature[ROWS-i][COLUMNS-i]))
    print("\n")

def initialize(size, rank):

    for i in range(ROWS+2):
        for j in range(COLUMNS+2):
            Temperature_last[i,j] = 0.0

    # Local boundry condition endpoints
    tMin = (rank)*100.0/size
    tMax = (rank+1)*100.0/size

    # Left and right boundaries
    for i in range(ROWS+2):
        Temperature_last[i,0] = 0.0
        Temperature_last[i,COLUMNS+1] = tMin + ((tMax-tMin)/ROWS)*i

    # Top boundary (PE 0 only)
    if rank == 0:
        for j in range(COLUMNS+2):
            Temperature_last[0,j] = 0.0

    # Bottom boundary (Last PE only)
    if rank == size-1:
        for j in range(COLUMNS+2):
            Temperature_last[ROWS+1,j] = (100.0/COLUMNS) * j

    return(Temperature_last)


iteration           =   1
dt_global           =   100 # delta t across all PEs

# the usual MPI startup routines
comm                =   MPI.COMM_WORLD
rank                =   comm.Get_rank()
size                =   comm.Get_size()
if rank==0:
    print("number of cores available = %s" % size)

# verify only size PEs are being used
if size != NPES:
    if rank==0:
        print("This code must be run with %s PEs\n" % NPES)
    MPI.Finalize();
    exit()

# PE 0 asks for input 
if rank==0: 
    max_iterations      =   float(raw_input("Maximum iterations [100-4000]?\n"))
else:
    max_iterations      =   100 # (need to set the case for the other PEs)
# bcast max iterations to other PEs
max_iterations = comm.bcast(max_iterations, root=0)

if rank==0: start_time     =   time.clock()

print('Now initializing on core #%s' % rank)
Temperature_last    =   initialize(size, rank)

while dt_global > MAX_TEMP_ERROR and iteration <= max_iterations:
    # print(dt_global,MAX_TEMP_ERROR,iteration,max_iterations)

    # # main calculation: average my four neighbors
    for i in range(1,ROWS+1):
        for j in range(1,COLUMNS+1):
            Temperature[i,j] = 0.25 * (Temperature_last[i+1,j] + Temperature_last[i-1,j] +
                                        Temperature_last[i,j+1] + Temperature_last[i,j-1])

    # COMMUNICATION PHASE: send ghost rows for next iteration

    # send bottom real row down
    if rank != size-1:         # unless we are bottom PE
        comm.send(Temperature[ROWS][1], rank+1, tag = DOWN);

    # receive the bottom row from above into our top ghost row
    if rank != 0:              # unless we are top PE
        Temperature_last[0][1] = comm.recv(buf=None, source = rank-1, tag = DOWN, status=None);

    # send top real row up
    if rank != 0:              # unless we are top PE
        comm.send(Temperature[1][1], rank-1, tag = UP);

    # receive the top row from below into our bottom ghost row
    if rank != size-1:         # unless we are bottom PE
        Temperature_last[ROWS+1][1] = comm.recv(buf=None, source=rank+1, tag = UP, status=None);

    dt = 0.0;

    # Find largest temperature difference in each core
    # and update Temperature_last
    for i in range(1, ROWS+1):
        for j in range(1,COLUMNS+1):
            dt = np.max( np.append(np.abs(Temperature[i,j]-Temperature_last[i,j]), dt))
            Temperature_last[i,j] = Temperature[i,j]
        # broadcast dt to all other PEs                                                        
        dt_global = comm.reduce(dt, op=min, root=0)
        dt_global = comm.bcast(dt_global, root=0)


    # periodically print test values - only for PE in lower corner
    if iteration%1 == 0:
        if rank == size-1:
            track_progress(iteration,Temperature)

    iteration   +=  1
else:

    # Slightly more accurate timing and cleaner output 
    comm.barrier();


    print("\nMax error at iteration %s on PE %s was %s" % (iteration-1, rank, dt_global))
    if rank==0: 
        stop_time     =   time.clock()
        print("\nTotal time: %s s\n" % (stop_time-start_time))
    MPI.Finalize();













