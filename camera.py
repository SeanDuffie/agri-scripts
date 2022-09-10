#!/usr/bin/env python
"""
Docstring for camera.py.
"""

from datetime import datetime
from time import sleep
import os
from os.path import exists
import cv2
import json
# import numpy
import serial
from serial.tools import list_ports
# from picamera import PiCamera

# Versions
# print("Package Versions for Diagnostics: ")

# Acquire initial data
RTDIR = os.getcwd()
IMGDIR = RTDIR + "/autocaps/"
OUTDAT = RTDIR + "/data/"
print("Root: ", RTDIR)
print("Image Dir: ", IMGDIR)
print("Data Dir: ", OUTDAT)
print("Output Video: ", RTDIR + "/time-lapse.mp4")
print()

VID_NAME = '{0}/time-lapse.mp4'.format(RTDIR)   # video name
FOURCC = cv2.VideoWriter_fourcc(*'mp4v')        # video format
FPS = 60                                        # video fps
IMG_SIZE = (1920, 1080)

NOW = datetime.now()
H = NOW.strftime("%H")
print("Current time: ", NOW)
print()


# If during inactive hours, do nothing
if (int(H) >= 7 or int(H) == 0):
# if (True):
    # FIXME: 64-bit PiCamera does not work yet...
    # ### Start Acquire Image ###
    # with PiCamera() as camera:
    #     print("Starting Camera...")
    #     camera.start_preview()
    #     sleep(5) # wait for camera to focus
    #     ## Capture image and stop
    #     IMG_NAME = NOW.strftime("{0}/autocaps/%Y-%m-%d_%Hh%Mm%Ss.jpg".format(RTDIR))
    #     camera.capture(IMG_NAME)
    #     camera.stop_preview()
    #     print("Picture Acquired!")
    #     print()
    # #### End Acquire Image ####


    ### Start Acquire Sensor Measurements ###
    # Identifying ports...
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
        timeout=1
    )

    # Send out requests until a response is received
    while ser.in_waiting == 0:
        print("Waiting for sensors...")
        ser.write('1'.encode('utf-8'))
        sleep(1)
    print()

    # Receive the Response from the sensors
    SENSOR_ARR = list()
    try:
        FEEDBACK = ser.readline()
        SENSOR_READ = FEEDBACK.decode("Ascii")
        SENSOR_ARR = SENSOR_READ.split(",")
        print(SENSOR_READ)
        print(SENSOR_ARR)
        print()
    except:
        print("Something went wrong with decoding!")
        pass

    # Read data history
    data = {}
    if (exists(OUTDAT + "dat.json")):
        f = open(OUTDAT + "dat.json")
        data = json.load(f)
        f.close()

    # Process and Store the new data
    data["TIME"].append(NOW.strftime("%Y-%m-%d_%Hh%Mm%Ss"))
    data["LIGHT"].append(float(SENSOR_ARR[0]))
    data["SOIL"].append(float(SENSOR_ARR[1]))
    data["TEMPC"].append(float(SENSOR_ARR[2]))
    data["TEMPF"].append(float(SENSOR_ARR[2])*(9/5)+32)
    data["HUMID"].append(float(SENSOR_ARR[3]))

    json_object = json.dumps(data, indent=4)
    print(json_object)
    with open(OUTDAT + "dat.json", "w") as f:
        f.write(json_object)

    #### End Acquire Sensor Measurements ####


    # ### Post Processing Video Compilation ###
    # IMG_ARR = []
    # # Read in current directory of images
    # print("Reading in Images...")
    # images = [img for img in os.listdir(IMGDIR) if img.endswith(".jpg")]
    # images.sort()
    # # Compile image array into a video FIXME: This is a broken video
    # print("Apply Modifications and compile video")
    # OUT = cv2.VideoWriter(VID_NAME, FOURCC, FPS, IMG_SIZE)
    # for filename in images:
    #     img = cv2.imread(IMGDIR + filename)  # Read in Raw image

    #     # TODO: Add Timestamp

    #     # TODO: Append Sensor data somehow

    #     IMG_ARR.append(img)         # Add image to array
    #     OUT.write(img)              # writes out each frame to the video file
    # OUT.release()
    # print("Released!")
    # #### End Post Processing Video Compilation ####
else:
    print("Inactive hours")
