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
    IMG_NAME = NOW.strftime("{0}/autocaps/%Y-%m-%d_%H:%M:%S.jpg".format(SDIR))

    # If during inactive hours, do nothing
    if (int(H) >= 7 or int(H) == 0):
    # if (False):
        # Start camera and wait to focus
        camera.start_preview()
        sleep(5)
        # Capture image and stop
        camera.capture(IMG_NAME)
        camera.stop_preview()

        # Read in current directory of images
        IMG_ARR = []
        IMG_SIZE = (0, 0)
        for filename in glob.glob('{0}/autocaps/*.jpg'.format(SDIR)):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            IMG_SIZE = (width, height)                   # image size
            IMG_ARR.append(img)

        # Compile image array into a video
        VID_NAME = '{0}/time-lapse.mp4'.format(SDIR) # video name
        FOURCC = cv2.VideoWriter_fourcc(*'MP4V')    # video format
        FPS = 60                                    # video fps
        OUT = cv2.VideoWriter(VID_NAME, FOURCC, FPS, IMG_SIZE)
        # for i in range(len(IMG_ARR)):
        #     OUT.write(IMG_ARR[i]) # writes out each frame to the video file
        OUT.write(list(enumerate(IMG_ARR))) # writes out each frame to the video file
        OUT.release()
    else:
        print("Inactive hours")
