#!/usr/bin/env python3
"""
Docstring for test_serial.py.
"""

from time import sleep
import serial
from serial.tools import list_ports

print("Identifying current ports... ")
PORT_LIST = list(list_ports.comports())
for p in PORT_LIST:
    print("  - ", p.device)
print()

# Setting up Serial connection
ser = serial.Serial(
    # port='/dev/ttyACM0', # use this to manually specify port
    port=PORT_LIST[0].device,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=10
)

# Send out requests until a response is received
while ser.in_waiting == 0:
    print("Waiting for sensors...")
    ser.write('3'.encode('utf-8'))
    sleep(5)
print()

print(ser.readline())
print()

com = input("Enter 'q' to stop pumping water: ")
while com != "q":
    com = input("Enter 'q': ")

while ser.in_waiting == 0:
    print("Waiting for sensors...")
    ser.write('4'.encode('utf-8'))
    sleep(5)
print()