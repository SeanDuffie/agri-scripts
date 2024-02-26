#!/usr/bin/env python3

import sys
import time

import cv2

raw_size: tuple = (3280, 2465)
# img_size: tuple = (1920, 1080)
img_size: tuple = (1280, 720)

RPI = False
BIT_64 = True

if sys.platform.startswith("linux"):
    RPI = True
    if sys.platform.find("64"):
        print("64-bit System - Using Picamera2...")
        from picamera2 import Picamera2, Preview  # For 64-bit OS
        BIT_64 = True
    else:
        print("32-bit System - Using Picamera...")
        from picamera import PiCamera  # For 32-bit OS
        BIT_64 = False
else:
    print("Not Linux - Ignoring Picamera...")

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)        # Windows
cap = cv2.VideoCapture(0)                       # Linux

# If 64 bit Raspberry Pi
if RPI:
    if BIT_64:
        print("Using 64 bit PiCamera2")
        picam2 = Picamera2()
        camera_config = picam2.create_preview_configuration(
            main={
                "size": raw_size,
                "format": "RGB888"
            }
        )
        capture_config = picam2.create_still_configuration(
            main={
                "size": raw_size,
                "format": "RGB888"
            }
        )
        picam2.configure(camera_config)
        picam2.start_preview(Preview.DRM)
        picam2.start()
        # picam2.start(config=capture_config)
        # time.sleep(2) # wait for camera to focus

        ## Capture image and stop
        # metadata = picam2.capture_metadata()
        # cur_img = picam2.capture_array()
        # cur_img = cv2.resize(cur_img, img_size)
    # If 32 bit Raspberry Pi
    else:
        print("Using 32 bit PiCamera")
        with PiCamera() as camera:
            camera.resolution = img_size
            camera.framerate = 24
            camera.start_preview()
            # time.sleep(2) # wait for camera to focus

            ## Capture image and stop
            # camera.capture(cur_img, 'rgb')
            # camera.stop_preview()
# If using USB camera (Windows)
else:
    print("Using OpenCV VideoCapture")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[1])
    # cap.set(cv2.CAP_PROP_EXPOSURE, 3.0)
    # time.sleep(2)
    ret, cur_img = cap.read()

    while cv2.waitKey(17) != ord("q"):
        # time.sleep(5)
        cv2.imshow("cv2", cur_img)
        ret,cur_img = cap.read()

    cap.release()
