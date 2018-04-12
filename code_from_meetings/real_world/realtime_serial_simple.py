"""
Simple script to capture serial readings in real-time in Python.

Date Created: 8 Apr 2018
Last Modified: 11 Apr 2018
Humans Responsible: The Prickly Pythons
"""

import serial

yourDeviceName = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600)

while(1):
	while (yourDeviceName.inWaiting() == 0): # Wait until there is something on the line
		pass

	valueRead = yourDeviceName.readline()
	print(valueRead)