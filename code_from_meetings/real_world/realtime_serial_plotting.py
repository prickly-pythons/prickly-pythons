"""
Script to capture serial readings in real-time in Python and plotting them.
Adapted from http://arduino-er.blogspot.com/2015/04/python-to-plot-graph-of-serial-data.html

Date Created: 8 Apr 2018
Last Modified: 11 Apr 2018
Humans Responsible: The Prickly Pythons
"""

import serial
import matplotlib.pyplot as plt
from drawnow import drawnow


serialArduino = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600)

def plotValues():
    plt.title('Serial value from Arduino')
    plt.grid(True)
    plt.ylabel('Values')
    plt.plot(buffer1, 'bo-', lw=2)



# Make a buffer and initialise it to hold 30 zeroes
buffer1 = []
for i in range(30):
    buffer1.append(0)


while 1:
    while (serialArduino.inWaiting() == 0):
        pass

    valueRead = serialArduino.readline()

    # Do checks to see if valueRead is valid
    try:
        valueReadInt = int(valueRead) # Casting to int

        if valueReadInt < 0:
            print("Invalid value! Too small")

        elif valueReadInt >= 1024:
            print("Invalid value! Too large")

        else:
            print(valueReadInt)

            # Place the value into the buffer
            buffer1.pop(0)
            buffer1.append(valueRead)
            
            # Plot the values on the fly
            drawnow(plotValues)

    except ValueError:
        print("Invalid value! Cannot cast to int")
    