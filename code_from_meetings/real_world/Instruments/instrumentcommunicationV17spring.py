#!/usr/bin/python
# Filename: InstrumentCommunication.py
version = '5.0, PyVisa 1.8'
__date__ = "Dec2016"

import visa
import string
from struct import unpack
import numpy
import serial

'''
pyvisa is used w/ GPIB connectors (most scopes, powersupplies, etc. in a lab have these
pyserial is used with USB connections, you would talk to arduino or most FPGAs using this
'''

print 'Loading InstrumentCommunication v'+ version
rm = visa.ResourceManager()

class Agilent3561A:
    #Output is Big-Endian
    def __init__(self, Agilent3561AAddresss):
        self.Agilent3561AAddresss = Agilent3561AAddresss
        self.Agilent3561A = rm.open_resource('GPIB0::'+str(Agilent3561AAddresss)+'::INSTR')
        print "Agilent3561A: " + self.Agilent3561A.ask("id?")
    def SingleDisplay(self):
        self.Agilent3561A.write("SNGL")
    def SetRMS(self):
        self.Agilent3561A.write("AVRS")
    def SetSpan(self, Span):
        self.Agilent3561A.write("SP "+str(Span)+ " HZ")
    def SetStart(self, Start):
        self.Agilent3561A.write("SF "+str(Start)+ " HZ")
    def SetCenter(self, Center):
        self.Agilent3561A.write("CF "+str(Center)+ " HZ")
    def SetNumberAverages(self, NumberOfAverages):
        self.Agilent3561A.write("NAVG "+str(NumberOfAverages)+ " ENT")
    def SetCoupling(self, Coupling):
        self.Agilent3561A.write("ICPL "+Coupling)
    def StartMeasurement(self):
        self.Agilent3561A.write("STRT")
    def GetOverloadStatus(self):
        MarkerPosition=self.Agilent3561A.ask_for_values("RDMK")
        return int(MarkerPosition[3])
    def GetStatus(self):
        ParameterString=self.Agilent3561A.ask("DDSA")
        if ParameterString.find('AVERAGE COMPLETE')!=-1:
            return 0
        elif ParameterString.find('AVG IN PROGRESS')!=-1:
            return 1
        elif ParameterString.find('AUTO RANGING')!=-1:
            return 2
        else:
            return ParameterString
    def GetBandwidth(self):
        ParameterString=self.Agilent3561A.ask("DDSA")
        Bandwidth=float(ParameterString[ParameterString.find('BW:')+3:ParameterString.find('Hz',ParameterString.find('BW:'))])
        return Bandwidth
    def GetWaveform(self):
        ParameterString=self.Agilent3561A.ask("DDSA")

        ParameterString=string.replace(ParameterString, ' ','')
        StartFrequency=int(ParameterString[ParameterString.find('START:')+6:ParameterString.find('Hz',ParameterString.find('START:'))])
        EndFrequency=int(ParameterString[ParameterString.find('STOP:')+5:ParameterString.find('Hz',ParameterString.find('STOP:'))])

        a=self.Agilent3561A.ask("DSTB")
        HeaderData=unpack('cc', a[0:2])
        HeaderByteData=unpack('>h', a[2:4])
        EndLineData=unpack('c'*(len(a)-806), a[806:len(a)])
        Data=unpack('>'+'h'*(401), a[4:806])

        ConvertedData=numpy.asarray(Data)*0.005
        ConvertedData=ConvertedData.reshape(len(ConvertedData), 1)
        FrequencyRange=numpy.linspace(StartFrequency,EndFrequency,len(ConvertedData))
        FrequencyRange=FrequencyRange.reshape(len(FrequencyRange), 1)
        CompleteData=numpy.hstack((FrequencyRange[0:len(FrequencyRange)], ConvertedData))
        return CompleteData
    def SaveToFile(self,FileName, Data):
        #Save to file
        OutputFile = file(FileName, 'w')
        OutputFile.write("Frequency (Hz) 	    dBV \n")
        numpy.savetxt(OutputFile, Data, fmt="%12.8G")
        OutputFile.close()
    def GPIBAsk(self, GPIBString):
        GPIBResponse=self.Agilent3561A.ask(GPIBString)
        return GPIBResponse
    def GPIBWrite(self, GPIBString):
        GPIBResponse=self.Agilent3561A.write(GPIBString)

class HP34401A:
    def __init__(self, HP34401AAddress):
        self.HP34401AAddress = HP34401AAddress
        self.HP34401A = rm.open_resource('GPIB0::'+str(HP34401AAddress)+'::INSTR')
        print "HP34401A Multimeter: " + self.HP34401A.ask("*IDN?")
    def VoltageReading(self):
        Voltage=float(self.HP34401A.ask("MEAS:VOLT:DC? DEF,DEF"))
        return Voltage
    def ResistanceReading(self):
        Resistance=float(self.HP34401A.ask("MEAS:RES? DEF,DEF"))
        return Resistance
    def measure(self):
        meas=float(self.HP34401A.ask("MEAS:CURR?"))
        return meas
    def CurrentReading(self):
        current=float(self.HP34401A.ask("MEAS:CURR?"))
        return current

    def GPIBAsk(self, GPIBString):
        GPIBResponse=self.HP34401A.ask(GPIBString)
        return GPIBResponse
    def GPIBWrite(self, GPIBString):
        GPIBResponse=self.HP34401A.write(GPIBString)

class Tektronix644:
    def __init__(self, Tektronix644Address):
        #global Tektronix644
        self.Tektronix644Address = Tektronix644Address
        self.Tektronix644 = rm.open_resource('GPIB0::'+str(Tektronix644Address)+'::INSTR')
        print "Tektronix 644: " + self.Tektronix644.ask("*IDN?")
    def Configure(self, Channel):
        self.Tektronix644.write("SEL:CH"+str(Channel)+" ON;:DAT:SOU CH"+str(Channel)+";ENC ASCI;WID 2")
        [self.Tektronix644.NumberOfPoints, PointOff, self.Tektronix644.XSamplingInterval, \
         self.Tektronix644.YMultiple, self.Tektronix644.YOffset, self.Tektronix644.YZero]= \
                         self.Tektronix644.ask_for_values("WFMP:CH"+str(Channel)+":NR_P?;PT_O?;XIN?;YMU?;YOF?;YZE?")
        self.Tektronix644.NumberOfPreSamples=self.Tektronix644.NumberOfPoints/2
        #Tektronix644.TimeBase=XSamplingInterval
    def GetAcquisitionNumber(self):
        CurrentAcquisition=self.Tektronix644.ask("ACQ:NUMAC?")
        return CurrentAcquisition
    def ForceTrigger(self):
        self.Tektronix644.write("TRIGGER FORC")
    def SetNumberOfSamples(self, NumberOfSamples):
        self.Tektronix644.write("HOR:RECO "+str(NumberOfSamples))
    def AcquireWaveform(self):
        WaveformOutput=self.Tektronix644.ask_for_values("CURV?")
        #Scale the data to volts and add column for time
        ScaledWaveformOutput = numpy.zeros((self.Tektronix644.NumberOfPoints,2), dtype=numpy.float)
        for i in range(0,len(WaveformOutput)):
            ScaledWaveformOutput[i,0]=self.Tektronix644.XSamplingInterval*i
            ScaledWaveformOutput[i,1]=(WaveformOutput[i]-self.Tektronix644.YOffset)*self.Tektronix644.YMultiple+self.Tektronix644.YZero
        return ScaledWaveformOutput
    def AcquireWaveformIGOR(self):
        WaveformTime=[int(math.floor(time.clock()*1000))]
        WaveformOutput=self.Tektronix644.ask_for_values("CURV?")
        #Scale the data to volts and add column for time
        ScaledWaveformOutput = numpy.zeros((len(WaveformOutput),1), dtype=numpy.float)
        for j in range(0,len(WaveformOutput)):
            #Convert to voltage and scale for IGOR
            TempWaveformScaling=(WaveformOutput[j]-self.Tektronix644.YOffset)*self.Tektronix644.YMultiple+self.Tektronix644.YZero+Range
            ScaledWaveformOutput[j,0]=math.ceil((TempWaveformScaling-IgorOffset)/(Range*Polarity)*pow(2,(NumberOfBits-1)))
            
        BinaryWaveformChannel=numpy.array(WaveformChannel, dtype='int8')
        BinaryWaveformTime=numpy.array(WaveformTime, dtype='uint32')
        BinaryWaveformData=numpy.array(ScaledWaveformOutput, dtype='int16')
        return (BinaryWaveformChannel, BinaryWaveformTime, BinaryWaveformData)
    def ZeroPulseWaveformIGOR(self):
        WaveformTime=[int(math.floor(time.clock()*1000))]
        ScaledWaveformOutput = numpy.zeros((Tektronix644.NumberOfPoints,1), dtype=numpy.float)
        BinaryWaveformChannel=numpy.array(WaveformChannel, dtype='int8')
        BinaryWaveformTime=numpy.array(WaveformTime, dtype='uint32')
        BinaryWaveformData=numpy.array(ScaledWaveformOutput, dtype='int16')
        return (BinaryWaveformChannel, BinaryWaveformTime, BinaryWaveformData)
    def GPIBAsk(self, GPIBString):
        GPIBResponse=self.Tektronix644.ask(GPIBString)
        return GPIBResponse
    def GPIBWrite(self, GPIBString):
        GPIBResponse=self.Tektronix644.write(GPIBString)

class LakeShore340:
    def __init__(self, LakeShore340Address):
        #global LakeShore340
        self.LakeShore340Address = LakeShore340Address
        self.LakeShore340 = rm.open_resource('GPIB0::'+str(LakeShore340Address)+'::INSTR')
        print "LakeShore 340: " + self.LakeShore340.query("*IDN?")
    def ResistanceReading(self, Channel=0):
        Resistance=float(self.LakeShore340.query("SRDG? "+str(Channel)))
        return Resistance
    def CelsiusReading(self, Channel=0):
        Resistance = float(self.LakeShore340.query("CRDG? " + str(Channel)))
        return Resistance
    def KelvinReading(self, Channel=0):
        Resistance = float(self.LakeShore340.query("KRDG? " + str(Channel)))
        return Resistance
    def SetChannelStatus(self, Channel, Status):
        self.LakeShore340.write("INSET "+str(Channel)+", "+str(Status)+", "+str(Status))
    def GetChannelStatus(self, Channel):
        Status=self.LakeShore340.query("INSET? "+str(Channel))
        return Status
    def GPIBAsk(self, GPIBString):
        GPIBResponse=self.LakeShore340.query(GPIBString)
        return GPIBResponse
    def GPIBWrite(self, GPIBString):
        GPIBResponse=self.LakeShore340.write(GPIBString)

class AVS47:
    def __init__(self, AVS47IBAddress):
        #global AVS47IB
        self.AVS47IBAddress = AVS47IBAddress
        AVS47IB = rm.open_resource('GPIB0::'+str(AVS47IBAddress)+'::INSTR')
        print "AVS47IB:" + self.AVS47IB.ask("*IDN?")
    def PrintInput(self):
        return self.AVS47IB.ask("INP?")
    def PrintChannel(self):
        return self.AVS47IB.ask("MUX?")
    def PrintRange(self):
        return self.AVS47IB.ask("RAN?")
    def PrintExcitation(self):
        return self.AVS47IB.ask("EXC?")
    def PrintResistance(self):
        self.AVS47IB.ask("ADC")
        return AVS47IB.ask("RES?")
    def SetChannel(self, NewChannel):
        self.AVS47IB.ask("REM 1")
        self.AVS47IB.ask("MUX "+ str(NewChannel))
        self.AVS47IB.ask("REM 0")
    def SetExcitation(self, NewExcitation):
        self.AVS47IB.ask("REM 1")
        self.AVS47IB.ask("EXC "+ str(NewExcitation))
        self.AVS47IB.ask("REM 0")
    def SetInput(self, NewInput):
        self.AVS47IB.ask("REM 1")
        self.AVS47IB.ask("INP "+ str(NewInput))
        self.AVS47IB.ask("REM 0")
    def ConvertOutputToNumber(AVS47Output):
        if AVS47Output.find('RAN')==0:
            Range=int(AVS47Output[4:])
            RangeValues=['Open','2','20','200','2K','20K','200K','2M']
            return RangeValues[Range]
        if AVS47Output.find('INP')==0:
            Input=int(AVS47Output[4:])
            InputValues=['Zero','Measure','Calibrate']
            return InputValues[Input]
        if AVS47Output.find('MUX')==0:
            MuxChannel=int(AVS47Output[4:])
            return MuxChannel
        if AVS47Output.find('EXC')==0:
            Exc=int(AVS47Output[4:])
            ExcValues=['0V','3uV','10uV','30uV','100uV','300uV','1mV','3mV']
            return ExcValues[Exc]
        if AVS47Output.find('RES')==0:
            Res=float(AVS47Output[4:])
            return Res
        return

    def GPIBAsk(self, GPIBString):
        GPIBResponse=self.AVS47IB.ask(GPIBString)
        return GPIBResponse
    def GPIBWrite(self, GPIBString):
        GPIBResponse=self.AVS47IB.write(GPIBString)

    def ConvertOutputToText(AVS47Output):
        if AVS47Output.find('RAN')==0:
            Range=int(AVS47Output[4:])
            RangeValues=['Open','2','20','200','2K','20K','200K','2M']
            return RangeValues[Range]
        if AVS47Output.find('INP')==0:
            Input=int(AVS47Output[4:])
            InputValues=['Zero','Measure','Calibrate']
            return InputValues[Input]
        if AVS47Output.find('MUX')==0:
            MuxChannel=int(AVS47Output[4:])
            MuxChannelValues=['Channel 0','Channel 1','Channel 2','Channel 3','Channel 4','Channel 5','Channel 6','Channel 7']
            return MuxChannelValues[MuxChannel]
        if AVS47Output.find('EXC')==0:
            Exc=int(AVS47Output[4:])
            ExcValues=['0V','3uV','10uV','30uV','100uV','300uV','1mV','3mV']
            return ExcValues[Exc]
        if AVS47Output.find('RES')==0:
            Res=float(AVS47Output[4:])
            ResValues= str(Res)+'Ohm'
            return ResValues
        return

class Keithley2010:
    """
    Keithley 2401 Source Measurement unit
    """
    def __init__(self, KEITHAddress):
        self.KEITHAddress = KEITHAddress
        self.Keithley2010 = rm.open_resource('GPIB0::'+str(KEITHAddress)+'::INSTR')
        print "E3632 DC Power Supply: " + self.Keithley2010.ask("*IDN?")
    def Measure(self):
        return float(self.Keithley2010.ask("MEAS?"))

class HPE3632:
    def __init__(self, HPE3632Address):
        #global HPE3632
        self.HPE3632Address = HPE3632Address
        self.HPE3632 = rm.open_resource('GPIB0::'+str(HPE3632Address)+'::INSTR')
        print "E3632 DC Power Supply: " + self.HPE3632.ask("*IDN?")
    def VoltageReading(self):
        Voltage=float(self.HPE3632.ask("MEAS:VOLT?"))
        return Voltage
    def CurrentReading(self):
        Voltage=float(self.HPE3632.ask("MEAS:CURR?"))
        return Voltage
    def SetVoltage(self, Voltage):
        self.HPE3632.write("VOLT "+str(Voltage))
    def SetStatus(self, Status):
        if Status==0:
           self.HPE3632.write("OUTPUT OFF")
        if Status==1:
           self.HPE3632.write("OUTPUT ON")
    def GPIBAsk(self, GPIBString):
        GPIBResponse=self.HPE3632.ask(GPIBString)
        return GPIBResponse
    def GPIBWrite(self, GPIBString):
        GPIBResponse=self.HPE3632.write(GPIBString)

class Tektronix654:
    def __init__(self, Tektronix654Address):
        self.Tektronix654Address = Tektronix654Address
        self.Tektronix654 = rm.open_resource('GPIB0::'+str(Tektronix654Address)+'::INSTR')
        print "Tektronix 644: " + self.Tektronix654.ask("*IDN?")
    def Configure(self, Channel):
        # needs to force parse based on ;'s here... re-write to work
        self.Tektronix654.write("SEL:CH"+str(Channel)+" ON;:DAT:SOU CH"+str(Channel)+";ENC ASCI;WID 2")
        self.Tektronix654.NumberOfPoints = int(self.Tektronix654.ask("WFMP:CH"+str(Channel)+":NR_P?"))
        PointOff = int(self.Tektronix654.ask("WFMP:CH"+str(Channel)+":PT_O?"))
        self.Tektronix654.XSamplingInterval = float(self.Tektronix654.ask("WFMP:CH"+str(Channel)+":XIN?"))
        self.Tektronix654.YMultiple = float(self.Tektronix654.ask("WFMP:CH"+str(Channel)+":YMU?"))
        self.Tektronix654.YOffset = float(self.Tektronix654.ask("WFMP:CH"+str(Channel)+":YOF?"))
        self.Tektronix654.YZero = float(self.Tektronix654.ask("WFMP:CH"+str(Channel)+":YZE?"))
        self.Tektronix654.NumberOfPreSamples=float(self.Tektronix654.NumberOfPoints)/2
        return [self.Tektronix654.NumberOfPoints, PointOff, self.Tektronix654.XSamplingInterval, self.Tektronix654.YMultiple, self.Tektronix654.YOffset, self.Tektronix654.YZero, self.Tektronix654.NumberOfPreSamples]
        #Tektronix644.TimeBase=XSamplingInterval
    def GetAcquisitionNumber(self):
        CurrentAcquisition=self.Tektronix654.ask("ACQ:NUMAC?")
        return CurrentAcquisition
    def ForceTrigger(self):
        self.Tektronix654.write("TRIGGER FORC")
    def SetNumberOfSamples(self, NumberOfSamples):
        self.Tektronix654.write("HOR:RECO "+str(NumberOfSamples))
    def AcquireWaveform(self):
        WaveformOutput=self.Tektronix654.ask("CURV?")
        # ERROR here, need to parse into array based on ,'s ewwwwwwwwww
        WaveformOutput2=[]
        for jj in range(0,self.Tektronix654.NumberOfPoints):
            WaveformOutput2.append(float(WaveformOutput.split(',')[jj]))
        #Scale the data to volts and add column for time
        ScaledWaveformOutput = numpy.zeros((self.Tektronix654.NumberOfPoints,2), dtype=numpy.float)
        for i in range(0,len(WaveformOutput2)):
            ScaledWaveformOutput[i,0]=float(self.Tektronix654.XSamplingInterval)*float(i)
            ScaledWaveformOutput[i,1]=(WaveformOutput2[i]-self.Tektronix654.YOffset)*self.Tektronix654.YMultiple+self.Tektronix654.YZero
        return WaveformOutput2
    def GPIBAsk(self, GPIBString):
        GPIBResponse=self.Tektronix654.ask(GPIBString)
        return GPIBResponse
    def GPIBWrite(self, GPIBString):
        GPIBResponse=self.Tektronix654.write(GPIBString)

''' ===================================================
serial for Cryotel
===================================================='''
import time
class CryoTel:
    def __init__(self, com_port):
        self.com_port=com_port
        # self.cryotel.flushInput()
        self.power=0.0
        self.temperature=0.0
        self.open_serial()

    def open_serial(self):
        self.cryotel = serial.Serial(self.com_port,4800, timeout=0.25)

    def close_serial(self):
        self.cryotel.close()

    def query(self, command):
        num_lines=self.write(command)
        value=self.read_reply(command, num_lines)
        return value

    def write(self, command):
        num_lines=self.cryotel.write(str(command))
        return num_lines

    def read_reply(self, command, num_lines):
        line_part='null'
        line=''
        while line_part != '':
            line_part=self.cryotel.readline()
            if command in line_part:
                # Parse line for result
                line_part=self.cryotel.readline()
                line=float(line_part)
        return line

    def read_power(self):
        self.power=self.query('P\r')

    def read_temperature(self):
        self.temperature=self.query('TC\r')

    def update(self):
        self.read_power()
        self.read_temperature()


# End of InstrumentCommunication.py				
