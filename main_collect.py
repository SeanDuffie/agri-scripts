#!/usr/bin/env python3
"""
Docstring for camera.py.
"""

import datetime
import os
import sys

import cv2

import collect

from .database_sql import Database

### Start Initial Setup ###
# Versions
print("Version Diagnostics:")
print("OS type: ", os.name)
print("Platform: ", sys.platform)

# Acquire initial data
NOW = datetime.datetime.now()
M = NOW.strftime("%m")
D = NOW.strftime("%d")
H = NOW.strftime("%H")
TIMESTAMP = NOW.strftime("%Y-%m-%d_%Hh")
asleep = True
if int(H) > collect.ACTIVE_START and int(H) < collect.ACTIVE_STOP:
    asleep = False
print("Current time: ", NOW)
print()

# Define Path names
RTDIR = os.getcwd()
SAMPLE_NAME = "AeroGarden1"
DATASET = f"{RTDIR}/data/{SAMPLE_NAME}/"
IMGDIR = f"{DATASET}/autocaps/"

# If autocaps or data don't exist, create them! They are gitignored...
if not os.path.exists(DATASET):
    os.makedirs(DATASET)
if not os.path.exists(IMGDIR):
    os.makedirs(IMGDIR)

IMG_NAME = f"{IMGDIR}{TIMESTAMP}.jpg"            # image name
IMG_SIZE = (1920, 1080)                     # video resolution

print("Root: ", RTDIR)
print("Current Dataset: ", DATASET)
print("Output Image: ", IMG_NAME)
print()
#### End Initial Setup ####


def collect_data(sensors: bool = True, camera: bool = True):
    """_summary_
    """
    db = Database("dat.db", DATASET)
    db.create_table(t_name=SAMPLE_NAME)

    if sensors:
        ### Start Acquire Sensor Measurements ###
        data = collect.acq_data(DATASET)
        new_dat = collect.acq_sensors()
        it = len(data["Date"])
        # TODO: Add code to process watering
        data = collect.app_dat(TIMESTAMP,it,M,D,H,0,data,new_dat)
        # CSV output
        # Pandas Method
        data.to_csv(path_or_buf=DATASET+"dat.csv",header=True,index=False)
        print(f"{data=}")
        print()
        #### End Acquire Sensor Measurements ####

    if camera:
        ### Start Acquire Image ###
        cur_img = collect.acq_img(raw_size=IMG_SIZE, flash=True, asleep=asleep)     # Capture Image
        cur_img = collect.proc_img(img=cur_img, tstmp=TIMESTAMP)                    # Process Image
        cv2.imwrite(IMG_NAME, cur_img)                                              # Save Image
        #### End Acquire Image ####

# def scheduler():
#     while True:
#         if 
#         time.sleep(1)

if __name__ == "__main__":
    sys.exit(collect_data())
