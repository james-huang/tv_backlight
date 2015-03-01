"""
The arduino will take commands per led,
'XRGB'

X: led postiion
R: red intensity
G: green intensity
B: blue intensity
"""

import os
import random
import sys
import serial
import time
import signal

PORT = '/dev/tty.usbmodem1451'
SPEED = 9600

#def send_command(val):
#  connection = serial.Serial(
#      PORT,
#      SPEED,
#      timeout=0,
#      stopbits=serial.STOPBITS_TWO,
#  )
#  connection.write(val)
#  connection.close()

arduino_serial = serial.Serial(
    PORT,
    baudrate=SPEED,
    stopbits=serial.STOPBITS_ONE,
    timeout=1,
)
time.sleep(3) # when a serial port is open the arduino runs reset sleep before sending commands

while True:
  s = ""
  for i in xrange(20):
    s += chr(random.randint(0,255)) + chr(random.randint(0,255)) + chr(random.randint(0,255))
  print "s: ", s
  arduino_serial.write(s)
  time.sleep(0.015)


arduino_serial.close()
#send_command('r')
#
#while 1:
#  #time.sleep(1)
#  #send_command('1')
#  time.sleep(1)
#  #


