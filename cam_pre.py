#!/usr/bin/env python

from picamera import PiCamera
from datetime import datetime
from time import sleep

with PiCamera() as camera:

    camera.start_preview()
    
    s = ""
    while s != "q":
        # sleep(5)
        s = input("Press q to quit")
    
    camera.stop_preview()
    pass
