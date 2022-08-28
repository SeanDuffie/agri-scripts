#!/usr/bin/env python
"""
Docstring for camera.py.
"""

from datetime import datetime
from time import sleep
import os
import cv2
import glob
import numpy
from serial.tools import list_ports
# from picamera import PiCamera

# Acquire initial data
RTDIR = os.getcwd()
IMGDIR = RTDIR + "/autocaps/autocaps/"
print("Root: ", RTDIR)
print("Images: ", IMGDIR)

VID_NAME = '{0}/time-lapse.mp4'.format(RTDIR)   # video name
FOURCC = cv2.VideoWriter_fourcc(*'mp4v')        # video format
FPS = 60                                        # video fps
IMG_SIZE = (1920, 1080)

NOW = datetime.now()
H = NOW.strftime("%H")

# If during inactive hours, do nothing
if (int(H) >= 7 or int(H) == 0):
# if (True):
    # ### Start Acquire Image ###
    # with PiCamera() as camera:
    #     camera.start_preview()
    #     sleep(5) # wait for camera to focus
    #     # ## Capture image and stop
    #     IMG_NAME = NOW.strftime("{0}/autocaps/%Y-%m-%d_%Hh%Mm%Ss.jpg".format(RTDIR))
    #     camera.capture(IMG_NAME)
    #     camera.stop_preview()
    # #### End Acquire Image ####


    ### TODO: Start Acquire Sensor Measurements ###
    # Identifying ports...
    port = list(list_ports.comports())
    for p in port:
        print(p.device)
    #### End Acquire Sensor Measurements ####


    ### Post Processing Video Compilation ###
    IMG_ARR = []
    # Read in current directory of images
    print("Reading in Images...")
    images = [img for img in os.listdir(IMGDIR) if img.endswith(".jpg")]
    images.sort()
    # Compile image array into a video FIXME: This is a broken video
    print("Apply Modifications and compile video")
    OUT = cv2.VideoWriter(VID_NAME, FOURCC, FPS, IMG_SIZE)
    for filename in images:
        img = cv2.imread(IMGDIR + filename)  # Read in Raw image

        # TODO: Add Timestamp

        # TODO: Append Sensor data somehow

        IMG_ARR.append(img)         # Add image to array
        OUT.write(img)              # writes out each frame to the video file
    OUT.release()
    print("Released!")
    #### End Post Processing Video Compilation ####
else:
    print("Inactive hours")
