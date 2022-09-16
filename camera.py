#!/usr/bin/env python3
"""
Docstring for camera.py.
"""

from datetime import datetime
from time import sleep
import os
from os.path import exists
import struct
import cv2
import json
import requests
# import numpy
import serial
from serial.tools import list_ports
if os.name.find("64"):
    from picamera2 import Picamera2, Preview        # For 64-bit OS
else:
    from picamera import PiCamera                   # For 32-bit OS


### Start Initial Setup ###
# Versions
print("Version Diagnostics:")
print("OS: ", os.uname()[0], os.uname()[2])
print("Architecture: ", os.uname()[4])
print()


# Acquire initial data
NOW = datetime.now()
H = NOW.strftime("%H")
NAME = NOW.strftime("%Y-%m-%d_%Hh%Mm%Ss")
print("Current time: ", NOW)
print()

RTDIR = os.getcwd()
IMGDIR = RTDIR + "/autocaps/"
OUTDAT = RTDIR + "/data/"

IMG_NAME = "{0}{1}.jpg".format(IMGDIR, NAME)
VID_NAME = '{0}/time-lapse.mp4'.format(RTDIR)   # video name
FOURCC = cv2.VideoWriter_fourcc(*'mp4v')        # video format
FPS = 60                                        # video fps
RAW_SIZE = (3280, 2465)                         # camera resolution
IMG_SIZE = (1920, 1080)                         # video resolution

print("Root: ", RTDIR)
print("Data Dir: ", OUTDAT)
print("Output Image: ", IMG_NAME)
print("Output Video: ", VID_NAME)
print()



if int(H) == 7:
    URL = 'https://maker.ifttt.com/trigger/wake_plants/with/key/RKAAitopP0prnKOxsyr-5'
    # data = { 'name': 'This is an example for webhook' }
    # requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'}) #leaving this in in case I decide to use json configurations later
    requests.post(URL)
#### End Initial Setup ####


### Start Acquire Sensor Measurements ###
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
data["TIME"].append(NAME)
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


### Start Acquire Image ###
# If during inactive hours, do nothing
if int(H) >= 7 or int(H) == 0:
    print("Starting Camera...\n")
    if os.name.find("64"):
        ## If 64 bit system
        picam2 = Picamera2()
        capture_config = picam2.create_still_configuration(main={"size": RAW_SIZE, "format": "RGB888"})
        picam2.start(config=capture_config)
        sleep(1) # wait for camera to focus

        ## Capture image and stop
        # metadata = picam2.capture_metadata()
        cur_img = picam2.capture_array()
        cur_img = cv2.resize(cur_img, IMG_SIZE)
    else:
        ## If 32 bit system
        with PiCamera() as camera:
            camera.start_preview()
            sleep(1) # wait for camera to focus

            ## Capture image and stop
            camera.capture(IMG_NAME)
            camera.stop_preview()

    ### Start Post Processing Current Image ###
    print("\nProcessing Image...")
    # Add Timestamp
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = (255, 255, 255)
    thickness = 2
    cv2.putText(cur_img, NAME, (50,50), font, fontScale, color, thickness, cv2.LINE_AA)

    # TODO: Append Sensor data somehow

    cv2.imwrite(IMG_NAME, cur_img)
    #### End Post Processing Current Image ####

    print("Picture Acquired!\n")
else:
    print("Inactive hours\n")
#### End Acquire Image ####


### Start Post Processing Video Compilation ###
if int(H) == 0:
    IMG_ARR = []
    # Read in current directory of images
    print("Reading in Images...")
    images = [img for img in os.listdir(IMGDIR) if img.endswith(".jpg") and img.find("_02h")]
    images.sort()
    # Compile image array into a video
    print("Compiling video...")
    OUT = cv2.VideoWriter(VID_NAME, FOURCC, FPS, IMG_SIZE)
    for filename in images:
        img = cv2.imread(IMGDIR + filename)  # Read in Raw image
        IMG_ARR.append(img)         # Add image to array
        OUT.write(img)              # writes out each frame to the video file
    OUT.release()
    print("Time-Lapse Released!\n")

    ## Turn of Lamp
    webhook_url = 'https://maker.ifttt.com/trigger/sleep_plants/with/key/RKAAitopP0prnKOxsyr-5'
    data = { 'name': 'This is an example for webhook' }
    # requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    requests.post(webhook_url)
    print("Goodnight!")
#### End Post Processing Video Compilation ####
