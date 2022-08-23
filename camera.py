#!/usr/bin/env python
"""
Docstring for camera.py.
"""

from datetime import datetime
from time import sleep
import os
import glob
from picamera import PiCamera

import cv2

SDIR = os.getcwd()

with PiCamera() as camera:
    # Acquire current time
    NOW = datetime.now()
    H = NOW.strftime("%H")
    IMG_NAME = NOW.strftime("{0}/autocaps/%Y-%m-%d_%Hh%Mm%Ss.jpg".format(SDIR))

    # If during inactive hours, do nothing
    if (int(H) >= 7 or int(H) == 0):
    # if (False):
        ### Start Acquire Image ###
        camera.start_preview()
        sleep(5) # wait for camera to focus
        # Capture image and stop
        camera.capture(IMG_NAME)
        camera.stop_preview()
        #### End Acquire Image ####


        ### TODO: Start Acquire Sensor Measurements ###
        
        #### End Acquire Sensor Measurements ####


        ### Post Processing Video Compilation ###
        # Read in current directory of images
        IMG_ARR = []
        IMG_SIZE = (0, 0)
        for filename in glob.glob('{0}/autocaps/*.jpg'.format(SDIR)):
            # Read in Raw image
            img = cv2.imread(filename)
            height, width, layers = img.shape
            IMG_SIZE = (width, height)                   # image size

            # TODO: Add Timestamp


            # TODO: Append Sensor data somehow


            # Add image to array
            IMG_ARR.append(img)

        # Compile image array into a video
        VID_NAME = '{0}/time-lapse.mp4'.format(SDIR) # video name
        FOURCC = cv2.VideoWriter_fourcc(*'MP4V')    # video format
        FPS = 60                                    # video fps
        OUT = cv2.VideoWriter(VID_NAME, FOURCC, FPS, IMG_SIZE)
        OUT.write(list(enumerate(IMG_ARR))) # writes out each frame to the video file
        OUT.release()
        #### End Post Processing Video Compilation ####
    else:
        print("Inactive hours")
