# Tuesday, Apr 10 2018

## Recap of our 9th meeting this semester! 
### Topic: Real World - Embedded systems and hardware

0. Zero coconut buns and coffee.. but lots of food for thought (read on) :)
1. Microcontrollers are CPUs with in-built memory and input/output (I/O) capabilities for interacting with the real world.
These little chips come in all sorts of shapes and sizes, some are really powerful with lots of memory but most have a limited amount of onboard memory and slow clock speeds. This reduces their cost and energy consumption which means they are ubiquitous - found inside everything from your phones to cars and microwave ovens and vending machines.
2. High-level, interpreted languages like Python *will not* run on a microcontroller (barely enough memeroy for the program let alone the interpreter).
3. The chips interact with the outside world via pins (metal legs sticking out of the chip). You configure them to be either inputs or outputs by assigning 0's and 1's, respectively, to particular memory slots called data direction registers (DDR). 
4. If a pin is an output you turn it on (make it output current) by assigning a 1 and off by assigning a 0 to another memory register that deals with I/O.
5. Datasheets and the instrument manuals are your friend.
6. It's very easy to get a serial interface going in Python. Steps are:


- Install the Python library [pyserial](https://github.com/pyserial/pyserial)
- Setup your device, in this case the Arduino, such that (1) it reads in an analog input, (2) after reading it prints the read value back to the computer via a serial connection. 
The particular code loaded onto the Arduino in the meeting is this (it's a variant of the C language):


 ```
const int analogPin = A0;
int analogVal = 0;

void setup() {
  Serial.begin(9600); // This sets up the Baud rate of the serial comm to 9600 bits/s
}

void loop() {
  analogVal = analogRead(analogPin);
  Serial.println(analogVal);
  delay(1000); // wait for 1 second
}
```

- Then in your Python script you have the following lines:


```
import serial
serialArduino = serial.Serial(port='/dev/Name-of-your-serial-port', baudrate=9600)

while True:
    valueRead = serialArduino.readline()

```

And that's basically it! You can then store the values read, in a Python list for example, and do any analysis you wish on them. These are the essentials for getting serial inputs to Python. The rest of the code in [this more elaborate version](https://github.com/prickly-pythons/prickly-pythons/blob/master/code_from_meetings/real_world/realtime_serial_plotting.py) deals with plotting, timing and handling exceptions.

### Some interesting and potentially useful links:

What is an Arduino?
<br>
https://www.arduino.cc/en/Guide/Introduction

Arduino interfacing with Python:
<br>
https://playground.arduino.cc/Interfacing/Python

Using microcontrollers to help with gardening (and make cool graphs):
<br>
https://www.youtube.com/watch?v=O_Q1WKCtWiA

Lena Heffern's old supervior's website: 
<br>
http://hacks.ayars.org/


<br>

Please visit our [homepage](http://prickly-pythons.github.io) where you can find topics for future meetings and links to the codes presented.
