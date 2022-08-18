#!/usr/bin/env python

from picamera import PiCamera
from datetime import datetime
from time import sleep
import os

import cv2
import numpy as np
import glob

path = os.getcwd()

with PiCamera() as camera:
    # Acquire current time
    now = datetime.now()
    hour = now.strftime("%H")
    imgname = now.strftime("{0}/autocaps/%Y-%m-%d_%H:%M:%S.jpg".format(path))

    # If during inactive hours, do nothing
    if (int(hour) >= 7 or int(hour) == 0):
    # if (False):
        # Start camera and wait to focus
        camera.start_preview()
        sleep(5)
        # Capture image and stop
        camera.capture(imgname)
        camera.stop_preview()

        # Read in current directory of images
        img_array = []
        for filename in glob.glob('{0}/autocaps/*.jpg'.format(path)):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)                   # image size
            img_array.append(img)

        # Compile image array into a video
        vidname = '{0}/time-lapse.mp4'.format(path) # video name
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')    # video format
        fps = 60                                    # video fps
        out = cv2.VideoWriter(vidname, fourcc, fps, size)
        for i in range(len(img_array)):
            out.write(img_array[i]) # writes out each frame to the video file
        out.release()

    pass
