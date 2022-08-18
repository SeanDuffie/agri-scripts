#!/usr/bin/env python

from picamera import PiCamera
from datetime import datetime
from time import sleep
import os

path = os.getcwd()

with PiCamera() as camera:
    # Acquire current time
    now = datetime.now()
    hour = now.strftime("%H")
    fname = now.strftime("{0}/autocaps/%Y-%m-%d_%H:%M:%S.jpg".format(path))

    # If during inactive hours, do nothing
    if (int(hour) >= 7 or int(hour) == 0):
    # if (False):
        # Start camera and wait to focus
        camera.start_preview()
        sleep(5)
        # Capture image and stop
        camera.capture(fname)
        camera.stop_preview()




    pass
