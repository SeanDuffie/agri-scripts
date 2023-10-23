#!/usr/bin/env python3
"""
Docstring for camera.py.
"""

import datetime
import os
import sys

import cv2

import agdata
import image
import timelapse
import webhook
from database import Database

### Start Initial Setup ###
# Versions
print("Version Diagnostics:")
print("OS type: ", os.name)
print("Platform: ", sys.platform)

OS_MODE: int = -1

if sys.platform.startswith("linux"):
    print("OS: ", os.uname()[0], os.uname()[2])
    print("Architecture: ", os.uname()[4])
    if sys.platform.find("64"):
        OS_MODE = 0
    else:
        print("32-bit System - Using Picamera...")
        from picamera import PiCamera  # For 32-bit OS
        OS_MODE = 1
else:
    print("Not Linux - Ignoring Picamera...")
    OS_MODE = 2

print()

# Acquire initial data
NOW = datetime.datetime.now()
M = NOW.strftime("%m")
D = NOW.strftime("%d")
H = NOW.strftime("%H")
TIMESTAMP = NOW.strftime("%Y-%m-%d_%Hh")
print("Current time: ", NOW)
print()

# Define Path names
RTDIR = os.getcwd()
DATASET = RTDIR + "/data/AeroGarden1/"
IMGDIR = DATASET + "/autocaps/"

# If autocaps or data don't exist, create them! They are gitignored...
if not os.path.exists(DATASET):
    os.makedirs(DATASET)
if not os.path.exists(IMGDIR):
    os.makedirs(IMGDIR)

IMG_NAME = f"{IMGDIR}{TIMESTAMP}.jpg"            # image name
VID_NAME = f"{DATASET}time-lapse.mp4"      # video name
FOURCC = cv2.VideoWriter_fourcc(*'mp4v')    # video format
FPS = 24                                    # video fps
RAW_SIZE = (3280, 2465)                     # camera resolution
IMG_SIZE = (1920, 1080)                     # video resolution

print("Root: ", RTDIR)
print("Current Dataset: ", DATASET)
print("Output Image: ", IMG_NAME)
print("Output Video: ", VID_NAME)
print()

URL_ON = 'https://maker.ifttt.com/trigger/wake_plants/with/key/RKAAitopP0prnKOxsyr-5'
URL_OFF = 'https://maker.ifttt.com/trigger/sleep_plants/with/key/RKAAitopP0prnKOxsyr-5'
#### End Initial Setup ####


### Start Acquire Sensor Measurements ###
data = agdata.acq_data(DATASET)
new_dat = agdata.acq_sensors()
it = len(data["Name"])
# TODO: Add code to process watering
data = agdata.app_dat(TIMESTAMP,it,M,D,H,0,data,new_dat)
# CSV output
# Pandas Method
data.to_csv(path_or_buf=DATASET+"dat.csv",header=True,index=False)
print(f"{data=}")
print()
#### End Acquire Sensor Measurements ####


### Start Acquire Image ###
# If during inactive hours, do nothing
webhook.post_webhook(URL_ON)                            # Turn on Lamp
# TODO: USB control
# https://stackoverflow.com/questions/59772765/how-to-turn-usb-port-power-on-and-off-in-raspberry-pi-4
cur_img = image.acq_img(IMG_SIZE)                       # Capture Image
cur_img = image.proc_img(img=cur_img, time=TIMESTAMP)        # Process Image
cv2.imwrite(IMG_NAME, cur_img)                          # Save Image
# if int(H) < 7 or int(H) > 19:
webhook.post_webhook(URL_OFF)                       # Turn off Lamp if Night
#### End Acquire Image ####


### Start Post Processing Video Compilation ###
if int(H) == 0:
    print("MIDNIGHT")
if True: # Previously I would only compile the video at Midnight, this True does it every hour
    db = Database(f"{DATASET}dat.csv")
    ## Start Generate Plots ###
    # Plot Total Light
    db.gen_plot(
        title="Light Intensity",
        x_label="Name",
        y_label="Light Intensity"
    )

    # Plot Total Soil Moisture
    db.gen_plot(
        title="Soil Moisture",
        x_label="Name",
        y_label="Soil Moisture"
    )

    # Plot Total Temperature
    db.gen_plot(
        title="Temperature",
        x_label="Name",
        y_label="Temperature"
    )

    # Plot Total Humidity
    db.gen_plot(
        title="Humidity",
        x_label="Name",
        y_label="Humidity"
    )
    ## End Generate Plots ##

    tl = timelapse.Timelapse(DATASET)
    tl.video_from_frames(data_path=DATASET, img_res=IMG_SIZE, fps=FPS)
#### End Post Processing Video Compilation ####
