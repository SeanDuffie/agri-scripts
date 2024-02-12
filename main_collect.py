#!/usr/bin/env python3
"""
Docstring for camera.py.
"""

import datetime
import os
import sys

import collect
import cv2
import webhook


def collect_data():
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
    it = len(data["Date"])
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
    collect.post_webhook(URL_ON)                            # Turn on Lamp
    # TODO: USB control
    # https://stackoverflow.com/questions/59772765/how-to-turn-usb-port-power-on-and-off-in-raspberry-pi-4
    cur_img = image.acq_img(IMG_SIZE)                       # Capture Image
    cur_img = image.proc_img(img=cur_img, time=TIMESTAMP)        # Process Image
    cv2.imwrite(IMG_NAME, cur_img)                          # Save Image
    # if int(H) < 7 or int(H) > 19:
    collect.post_webhook(URL_OFF)                       # Turn off Lamp if Night
    #### End Acquire Image ####

if __name__ == "__main__":
    sys.exit(collect_data())
