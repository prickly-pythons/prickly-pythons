import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import instrumentcommunicationV17spring as IC

#====================
# Note that you can change voltage and current w/ VoltageReading() or CurrentReading() for the HP's
# For the Keithley, the physical instrument must be set to what you want to measure, it will just pull the value
#====================

#====================================================================
#======================= Talk to Instruments ========================
HP34401AAddress1=24
HP34401AAddress2=12
KEITHAddress=16
HP1=IC.HP34401A(HP34401AAddress1)
Keithley=IC.Keithley2010(KEITHAddress)
HP2=IC.HP34401A(HP34401AAddress2)

#====================================================================
#=================== Start Configurable Parameters ==================

FileNameText='Name your file'

#Description for filename
FileNameDesc='Give a description or version number to file name'

#Parameters to be saved in log file
AdditionalInformation='This info will go in the file'

#Specify FilePath, this makes a new folder based on the date
FolderDate = time.strftime("%Y%m%d")
StTime=time.strftime("%H-%M-%S")
path='data/'+str(FolderDate)+'/'+ str(StTime)
try:
    os.makedirs(path)
except OSError:
    if not os.path.isdir(path):
        raise

# Set the total length of time (in seconds) to run for:
Secs=86400 # note: 7200s = 2 hours, 43200s = 12 hours, 86400s = 24 hours
SampleInterval = 10 # Pick the sampling time interval, must be > 2
NumberOfSamples=Secs/SampleInterval # Total number of data points collected


#==================== End Configurable Parameters ===================
#====================================================================

#========================== Start Functions =========================
def SaveDataToFile(FileName, AdditionalInformation, data):
    CompleteData = file(FileName, 'a')
    CompleteData.write("#Data acquired using: " + sys.argv[0] + "\n#")
    CompleteData.write(AdditionalInformation+"\n")
    CompleteData.write("#----------------------------------------\n \n")
    CompleteData.write('#Current time is: ' + time.strftime("%Y-%m-%d at %H:%M:%S"))
    CompleteData.write("\n#|   Time (s)    |  Voltage of HP1  |  Current of HP2   |  Reading on Keithley    | \n")
    np.savetxt(CompleteData, data, fmt="%16.12G")
    CompleteData.close()
    return

#=========================== End FileWrite ==========================
print "==================================================="

print '|   Time (s)   |  Voltage of HP1  |  Current of HP2   |  Reading on Keithley    |'
samples = []

for i in range(0, NumberOfSamples):
    voltage=HP1.VoltageReading()
    current=HP2.CurrentReading()
    Data1=Keithley.Measure()
    #====================
    # Note that you can change voltage and current w/ VoltageReading() or CurrentReading() for the HP's
    # For the Keithley, the physical instrument must be set to what you want to measure, it will just pull the value
    #====================

    sample=[time.time(), voltage, current, Data1]
    samples.append(sample)
    #Time to wait between measurements.
    time.sleep(SampleInterval)

    #Periodicaly save data.
    Q,R=divmod(i,120)
    if R == 0 :
        #Save data to temp file
        FileName=os.path.join(path,time.strftime("%Y.%m.%d-%H-%M-%S")+"."+FileNameText +'.'+ FileNameDesc + '.tmp')
        SaveDataToFile(FileName,AdditionalInformation, np.asarray(samples))

    #Periodicaly print data.
    Q,R=divmod(i,3)
    if R == 0 :
        print sample
        #Save data to temp file

print "==================================================="
print "                Acquisition Complete"
print "==================================================="
print 'Current time is: ' + time.strftime("%Y-%m-%d at %H:%M:%S")
print "==================================================="
#Save the data

FileName=os.path.join(path,time.strftime("%Y.%m.%d-%H-%M-%S")+"."+FileNameText +'.'+ FileNameDesc + '.txt')
SaveDataToFile(FileName, AdditionalInformation, np.asarray(samples))
