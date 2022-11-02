"""

"""
import os
import sys
from time import sleep
import cv2
import numpy as np
from numpy import uint8
from numpy.typing import NDArray
if sys.platform.startswith("linux"):
    if sys.platform.find("64"):
        from picamera2 import Picamera2, Preview        # For 64-bit OS
    else:
        from picamera import PiCamera                   # For 32-bit OS

def acq_img(img_name:str, raw_size, img_size):
    """
    Temp Docstring
    """
    cur_img = np.zeros([img_size[1], img_size[0], 3], dtype = np.uint8)
    cur_img[:,:] = [255, 255, 255]
    print("Starting Camera...\n")
    if sys.platform.find("win") == -1:
        if os.name.find("64"):
            ## If 64 bit system
            picam2 = Picamera2()
            capture_config = picam2.create_still_configuration(
                main={
                    "size": raw_size,
                    "format": "RGB888"
                }
            )
            picam2.start(config=capture_config)
            sleep(3) # wait for camera to focus

            ## Capture image and stop
            # metadata = picam2.capture_metadata()
            cur_img = picam2.capture_array()
            cur_img = cv2.resize(cur_img, img_size)
        else:
            ## If 32 bit system
            with PiCamera() as camera:
                camera.start_preview()
                sleep(3) # wait for camera to focus

                ## Capture image and stop
                camera.capture(img_name)
                camera.stop_preview()
        print("Picture Acquired!\n")
    else:
        print("Windows OS, Saving a blank image...\n")
    return cur_img

def proc_img(img:NDArray[uint8], name:NDArray[uint8]):
    """
    Temp Docstring
    """
    ### Start Post Processing Current Image ###
    print("\nProcessing Image...")
    # Add Timestamp
    off_x, off_y = (50, 50)
    draw_text(img, name, pos=(off_x, off_y))

    # TODO: Append Sensor data somehow

    # Add Day/Night Indicator

    # Add Water Level 'Battery' Indicator [BLUE]
    # Parallel Humidity level Indicator [GREEN]
    # Parallel Temperature Indicator [RED]

    # Add info panel
        # Number of days since last watering

    #### End Post Processing Current Image ####
    return img

def draw_text(img,
            text,
            pos=(5,5),
            font=cv2.FONT_HERSHEY_SIMPLEX,
            font_scale=1,
            font_thickness=2,
            font_color=(255,255,255),
            background_color=(0,0,0)):
    """
    Temp Docstring
    """
    x,y = pos
    print(x,y)
    dim,_ = cv2.getTextSize(text, font, font_scale, font_thickness)
    w,h = dim
    print(w,h)
    cv2.rectangle(img,
                (x-5, y-5),
                (x+w+10, y+h+10),
                background_color,
                -1)
    cv2.putText(img,
                text,
                (x, y+h+(font_scale-1)),
                font,
                font_scale,
                font_color,
                font_thickness,
                cv2.LINE_AA)
