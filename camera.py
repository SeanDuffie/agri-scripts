#!/usr/bin/env python3
"""
Docstring for camera.py.
"""

from datetime import datetime
import os
import json
import cv2
import requests
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import webhook
import agdata
import image

### Start Initial Setup ###
# Versions
print("Version Diagnostics:")
print("OS: ", os.uname()[0], os.uname()[2])
print("Architecture: ", os.uname()[4])
print()

# Acquire initial data
NOW = datetime.now()
H = NOW.strftime("%H")
NAME = NOW.strftime("%Y-%m-%d_%Hh")
print("Current time: ", NOW)
print()

RTDIR = os.getcwd()
IMGDIR = RTDIR + "/autocaps/"
OUTDAT = RTDIR + "/data/"

IMG_NAME = f"{IMGDIR}{NAME}.jpg"            # image name
VID_NAME = f"{RTDIR}/time-lapse.mp4"        # video name
FOURCC = cv2.VideoWriter_fourcc(*'mp4v')    # video format
FPS = 15                                    # video fps
RAW_SIZE = (3280, 2465)                     # camera resolution
IMG_SIZE = (1920, 1080)                     # video resolution

print("Root: ", RTDIR)
print("Data Dir: ", OUTDAT)
print("Output Image: ", IMG_NAME)
print("Output Video: ", VID_NAME)
print()

fields = []
rows = []
URL_ON = 'https://maker.ifttt.com/trigger/wake_plants/with/key/RKAAitopP0prnKOxsyr-5'
URL_OFF = 'https://maker.ifttt.com/trigger/sleep_plants/with/key/RKAAitopP0prnKOxsyr-5'
#### End Initial Setup ####


### Start Acquire Sensor Measurements ###
fields, rows = agdata.acq_data(NAME, OUTDAT)
rows.append(agdata.acq_sensors())
# # JSON output
# with open(OUTDAT + "dat.json", "w", encoding="utf-8") as f:
#     json_object = json.dumps(data, indent=4)
#     f.write(json_object)
# CSV output
with open(OUTDAT + "dat.csv", "w", encoding="utf-8") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
#### End Acquire Sensor Measurements ####


### Start Acquire Image ###
# If during inactive hours, do nothing
webhook.post_webhook(URL_ON)                           # Turn on Lamp
cur_img = image.acq_img(IMG_NAME, H,RAW_SIZE,IMG_SIZE)      # Capture Image
cur_img = image.proc_img(img=cur_img, name=NAME)            # Process Image
cv2.imwrite(IMG_NAME, cur_img)                              # Save Image
if int(H) < 7 and int(H) != 0 or int(H) > 19:
    webhook.post_webhook(URL_OFF)                                   # Turn off Lamp if Night
#### End Acquire Image ####


### Start Post Processing Video Compilation ###
if int(H) == 0:
    ## Start Generate Plots ##
    cnt = 0
    iter = []
    hrs = []
    for stamp in data["TIME"]:
        cnt += 1
        iter.append(cnt)
        hrs.append(int(stamp[11:13]))
    print(hrs)

    # Plot Total Light
    plt.plot(iter, data["LIGHT"])
    plt.xlabel("Time (Hours)")
    plt.ylabel("Light Exposure")
    plt.savefig("data/Light_Exposure.png")
    plt.close()

    # Plot average light per hour

    # Plot Total Soil Moisture
    plt.plot(iter, data["SOIL"])
    plt.xlabel("Time (Hours)")
    plt.ylabel("Soil Moisture")
    plt.savefig("data/Soil_Moisture.png")
    plt.close()

    # Plot average moisture per hour

    # Plot Total Soil Moisture
    plt.plot(iter, data["TEMPF"])
    plt.xlabel("Time (Hours)")
    plt.ylabel("Temperature in F")
    plt.savefig("data/TempF.png")
    plt.close()
    
    # Plot average temperature per hour

    # Plot Total Soil Moisture
    plt.plot(iter, data["HUMID"])
    plt.xlabel("Time (Hours)")
    plt.ylabel("Air Humidity (Percentage)")
    plt.savefig("data/Humidity.png")
    plt.close()
    
    # Plot average humidity per hour

    ### End Generate Plots ###


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
#### End Post Processing Video Compilation ####
