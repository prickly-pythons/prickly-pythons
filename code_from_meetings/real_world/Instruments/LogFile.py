#! /usr/bin/env python
# Filename: LogFile.py
version = '0.4'

import numpy
import shutil

print 'Loading LogFile v'+ version

def help():
	print 'LogFile.py currently supports:'
	print 'InitializeHeader: Creates log file header arrays'
	print 'CreateHeader: Writes header to file'
	print 'SaveToNewFile: Saves data and header to new file'
	print 'AppendToFile: Appends data to existing file'

def InitializeHeader():
    #Initialize log file header array
    LogFileHeader = ['$' for i in range(50)]
    LogFileDataFields = ['$' for i in range(50)]
    return [LogFileHeader, LogFileDataFields]

def CreateHeader(FileName, LogFileParamters, LogFileHeader, LogFileDataFields):
    #Remove unused lines
    LogFileHeader=filter((lambda x: x!='$'), LogFileHeader)
    LogFileDataFields=filter((lambda x: x!='$'), LogFileDataFields)

    OutputFile = file(FileName, 'w')
    OutputFile.write("Data acquired using: " + LogFileParamters[0] + "\n")
    OutputFile.write("Acquisition started at: " + LogFileParamters[1] + "\n")
    for j in range(0,len(LogFileHeader)):
       OutputFile.write(LogFileHeader[j]+"\n")
    OutputFile.write("----------------------------------------\n")
    for j in range(0,len(LogFileDataFields)):
       OutputFile.write(LogFileDataFields[j]+"\t")
    OutputFile.write("\n")
    OutputFile.close()
    return

def SaveToNewFile(FileName, LogFileParamters, LogFileHeader, LogFileDataFields, MeasurementData):
    #Remove unused lines
    LogFileHeader=filter((lambda x: x!='$'), LogFileHeader)
    LogFileDataFields=filter((lambda x: x!='$'), LogFileDataFields)
    OutputFile = file(FileName, 'w')
    OutputFile.write("Data acquired using: " + LogFileParamters[0] + "\n")
    OutputFile.write("Acquisition started at: " + LogFileParamters[1] + "\n")
    OutputFile.write("Bandwidth: " + LogFileParamters[2] + "\n")
    for j in range(0,len(LogFileHeader)):
       OutputFile.write(LogFileHeader[j]+"\n")
    OutputFile.write("----------------------------------------\n")
    for j in range(0,len(LogFileDataFields)):
       OutputFile.write(LogFileDataFields[j]+"\t")
    OutputFile.write("\n")
    numpy.savetxt(OutputFile, MeasurementData, fmt="%12.8G")
    OutputFile.close()
    return

def AppendToFile(FileName, MeasurementData):
    shutil.copy(FileName, '.tmp.'+FileName)
    OutputFile = file(FileName, 'a')
    numpy.savetxt(OutputFile, MeasurementData, fmt="%12.8G")
    OutputFile.close()
    return

'''
def info(msg):
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    print '[%s] %s' % (mod.__name__, msg)
'''
# End of LogFile.py