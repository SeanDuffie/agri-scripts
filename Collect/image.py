"""

"""
import time

import cv2
import numpy as np
from constants import BIT64, RPI
from numpy.typing import NDArray

if RPI:
    if BIT64:
        print("64-bit System - Using Picamera2...")
        from picamera2 import Picamera2  # For 64-bit OS
    else:
        print("32-bit System - Using Picamera...")
        from picamera import PiCamera  # For 32-bit OS
else:
    print("Not Linux - Ignoring Picamera...")


def acq_img(raw_size: tuple = (3280, 2465), img_size: tuple = (1920, 1080)):
    """ Grabs the image from the local camera system

    This function has support for the old 32 bit PiCamera library, 64 bit PiCamera2, and the
    default opencv2 library. It will grab a picture and resize it to the desired resolution.

    Args:
        - raw_size (tuple, optional): Native camera resolution - only PiCamera2. Default (3280, 2465)
        - img_size (tuple, optional): Output Resolution - Defaults to (1920, 1080).

    Returns:
        NDArray: The current - size adjusted - image from the camera
    """
    cur_img = np.zeros([img_size[1], img_size[0], 3], dtype = np.uint8)
    cur_img[:,:] = [255, 255, 255]
    print("Starting Camera...")

    # If 64 bit Raspberry Pi
    if RPI:
        if BIT64:
            print("Using 64 bit PiCamera2")
            picam2 = Picamera2()
            capture_config = picam2.create_still_configuration(
                main={
                    "size": raw_size,
                    "format": "RGB888"
                }
            )
            picam2.start(config=capture_config)
            time.sleep(2) # wait for camera to focus

            ## Capture image and stop
            # metadata = picam2.capture_metadata()
            cur_img = picam2.capture_array()
            cur_img = cv2.resize(cur_img, img_size)
        # If 32 bit Raspberry Pi
        else:
            print("Using 32 bit PiCamera")
            with PiCamera() as camera:
                camera.resolution = img_size
                camera.framerate = 24
                # camera.start_preview()
                time.sleep(2) # wait for camera to focus

                ## Capture image and stop
                camera.capture(cur_img, 'rgb')
                # camera.stop_preview()
    # If using USB camera (Windows)
    else:
        print("Using OpenCV VideoCapture")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[1])
        cap.set(cv2.CAP_PROP_EXPOSURE, 3.0)
        time.sleep(2)
        ret, cur_img = cap.read()
        cap.release()

    print("Picture Acquired!\n")
    return cur_img

def proc_img(img: NDArray, time: str):
    """ Processes the image and applies edits

    Args:
        img (NDArray): input image
        time (str): timestamp of the image being taken

    Returns:
        NDArray: edited image with overlay applied
    """
    ### Start Post Processing Current Image ###
    print("\nProcessing Image...")
    # Add Timestamp
    off_x, off_y = (50, 50)
    draw_text(img, time, pos=(off_x, off_y))

    # TODO: Append Sensor data somehow

    # Add Day/Night Indicator

    # Add Water Level 'Battery' Indicator [BLUE]
    # Parallel Humidity level Indicator [GREEN]
    # Parallel Temperature Indicator [RED]

    # Add info panel
        # Number of days since last watering

    #### End Post Processing Current Image ####
    return img

def draw_text(img: NDArray,
            text: str,
            pos: tuple = (5,5),
            font = cv2.FONT_HERSHEY_SIMPLEX,
            font_scale: int = 1,
            font_thickness: int = 2,
            font_color: tuple = (255,255,255),
            background_color: tuple = (0,0,0)):
    """ Wrapper function that I made to help me standardize putting text on the image

    Args:
        img (NDArray): original input image
        text (str): text to be added to the image
        pos (tuple, optional): Top left corner of the text. Defaults to (5,5).
        font (cv2 font, optional): Style of Font. Defaults to cv2.FONT_HERSHEY_SIMPLEX.
        font_scale (int, optional): Font size. Defaults to 1.
        font_thickness (int, optional): Font Thickness. Defaults to 2.
        font_color (tuple, optional): RGB color of font. Defaults to (255,255,255).
        background_color (tuple, optional): RGB color of background. Defaults to (0,0,0).
    """
    x,y = pos
    # This is necessary to outline the background, must be larger than text to prevent jumping
    (w,h),_ = cv2.getTextSize(text, font, font_scale, font_thickness)
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
