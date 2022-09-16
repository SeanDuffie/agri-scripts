#!/usr/bin/env python3
"""
Docstring for camera.py.
"""

from datetime import datetime
from time import sleep
import os
from os.path import exists
import cv2
import json
import requests
# import numpy
import serial
from serial.tools import list_ports
# from picamera import PiCamera                   # For 32-bit OS
from picamera2 import Picamera2, Preview        # For 64-bit OS


### Start Initial Setup ###
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


if int(H) == 7:
    webhook_url = 'https://maker.ifttt.com/trigger/wake_plants/with/key/RKAAitopP0prnKOxsyr-5'
    data = { 'name': 'This is an example for webhook' }
    # requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'}) #leaving this in in case I decide to use json configurations later
    requests.post(webhook_url)
#### End Initial Setup ####





### Start Acquire Sensor Measurements ###
## Identifying ports...
# print("Identifying current ports... ")
PORT_LIST = list(list_ports.comports())
# for p in PORT_LIST:
#     print("  - ", p.device)
# print()

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
    ser.write('1'.encode('utf-8'))
    sleep(.5)
print()

# Receive the Response from the sensors
SENSOR_ARR = list()
try:
    print("Reading Response...")
    FEEDBACK = ser.readline()
    SENSOR_READ = FEEDBACK.decode("Ascii")
    SENSOR_ARR = SENSOR_READ.split(",")
    print(SENSOR_ARR)
    print()
except:
    print("Something went wrong with decoding!")
    pass

# Read data history
if (exists(OUTDAT + "dat.json")):
    print("Loading current file...")
    f = open(OUTDAT + "dat.json")
    data = json.load(f)
    f.close()
else:
    data = {
        "TIME": list(),
        "LIGHT": [],
        "SOIL": [],
        "TEMPC": [],
        "TEMPF": [],
        "HUMID": []
    }
# Process and Store the new data
print("Appending New Data..")
data["TIME"].append(NOW.strftime("%Y-%m-%d_%Hh%Mm%Ss"))
data["LIGHT"].append(float(SENSOR_ARR[0]))
data["SOIL"].append(float(SENSOR_ARR[1]))
data["TEMPC"].append(float(SENSOR_ARR[2]))
data["TEMPF"].append(float(SENSOR_ARR[2])*(9/5)+32)
data["HUMID"].append(float(SENSOR_ARR[3]))

json_object = json.dumps(data, indent=4)
# print(json.dumps(data, indent=-1))
with open(OUTDAT + "dat.json", "w") as f:
    f.write(json_object)
#### End Acquire Sensor Measurements ####

# If during inactive hours, do nothing
if int(H) >= 7 or int(H) == 0 or True:
    ### Start Acquire Image ###

    ## If 32 bit system
    # with PiCamera() as camera:
    #     print("Starting Camera...")
    #     camera.start_preview()
    #     sleep(1) # wait for camera to focus
    #     ## Capture image and stop
    #     IMG_NAME = NOW.strftime("{0}/autocaps/%Y-%m-%d_%Hh%Mm%Ss.jpg".format(RTDIR))
    #     camera.capture(IMG_NAME)
    #     camera.stop_preview()

    ## If 64 bit system
    picam2 = Picamera2()
    capture_config = picam2.create_still_configuration(main={"size": (3280, 1845), "format": "RGB888"})
    picam2.start(config=capture_config, show_preview=False)
    sleep(1) # wait for camera to focus

    ## Capture image and stop
    IMG_NAME = NOW.strftime("autocaps/%Y-%m-%d_%Hh%Mm%Ss.jpg".format(RTDIR))
    metadata = picam2.capture_metadata()
    picam2.capture_file(IMG_NAME)
    cur_img = picam2.switch_mode_and_capture_array(IMG_NAME)

    print("Picture Acquired!")
    print()
    #### End Acquire Image ####
else:
    print("Inactive hours")
print(cur_img[0][0])


### Start Post Processing Current Image ###
#     # TODO: Add Timestamp

#     # TODO: Append Sensor data somehow

#### End Post Processing Current Image ####


### Start Post Processing Video Compilation ###
if int(H) == 0:
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
    #     IMG_ARR.append(img)         # Add image to array
    #     OUT.write(img)              # writes out each frame to the video file
    # OUT.release()
    # print("Released!")
    webhook_url = 'https://maker.ifttt.com/trigger/sleep_plants/with/key/RKAAitopP0prnKOxsyr-5'
    data = { 'name': 'This is an example for webhook' }
    # requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    requests.post(webhook_url)
#### End Post Processing Video Compilation ####
