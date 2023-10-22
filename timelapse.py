""" timelapse.py

    Handles interactions with the timelapse video
    TODO: Localize Image class to here (even if separate file)
    TODO: Grab new frame and construct a new timelapse with a single call
    TODO: Save raw frames and apply overlay modifications only when adding to timelapse
"""
import logging
import os
import sys
import time
from tkinter import filedialog

import cv2
import numpy as np
from numpy.typing import NDArray

OS_MODE: int = -1

if sys.platform.startswith("linux"):
    if sys.platform.find("64"):
        print("64-bit System - Using Picamera2...")
        from picamera2 import Picamera2  # For 64-bit OS
        OS_MODE = 0
    else:
        print("32-bit System - Using Picamera...")
        from picamera import PiCamera  # For 32-bit OS
        OS_MODE = 1
else:
    print("Not Linux - Ignoring Picamera...")
    OS_MODE = 2

# ONLY SET THIS IF BLANK IMAGE DESIRED
# OS_MODE = 3

RTDIR = os.getcwd()
FOURCC = cv2.VideoWriter_fourcc(*'mp4v')

class Image:
    """_summary_
    """
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
        if OS_MODE == 0:
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
        elif OS_MODE == 1:
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
        elif OS_MODE == 2:
            print("Using OpenCV VideoCapture")
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[0])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[1])
            cap.set(cv2.CAP_PROP_EXPOSURE, 3.0)
            time.sleep(2)
            ret, cur_img = cap.read()
            cap.release()
        else:
            print("Bad OS MODE!")
            # sys.exit(1)

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

    def draw_text(self,
                img: NDArray,
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


class Timelapse:
    """_summary_
    """
    def __init__(self, path: str = ""):
        # Initial Logger Settings
        fmt_main: str = "%(asctime)s | %(levelname)s\t| ImgMod:\t%(message)s"
        logging.basicConfig(format=fmt_main, level=logging.INFO,
                        datefmt="%Y-%m-%D %H:%M:%S")

        # Validate Path
        if path == "" or not os.path.exists(path):
            logging.info("Path blank, use tkinter dialog to pick.")
            path = filedialog.askdirectory(
                title="Select Current Data File",
                initialdir=f"{os.getcwd()}\\data\\")
            if path == "":
                logging.error("Tkinter Filedialog cancelled.")
                sys.exit(1)

        # If autocaps or data don't exist, create them! They are gitignored...
        if not os.path.exists(path):
            logging.warning("Prompted directory doesn't exist, creating new one:\t%s", path)
            os.makedirs(path)

    def append_frames(self, existing_video_path, new_frames):
        """_summary_

        Args:
            existing_video_path (_type_): _description_
            new_frames (_type_): _description_
        """
        cap = cv2.VideoCapture(existing_video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        new_video_path = 'appended_video.avi'
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(new_video_path, fourcc, fps, (width, height))
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            writer.write(frame)
        for new_frame in new_frames:
            writer.write(new_frame)
        cap.release()
        writer.release()
        os.remove(existing_video_path)
        os.rename(new_video_path, existing_video_path)

    def video_from_frames(self, img_dir, vid_path, fps, img_res):
        # Read in current directory of images
        logging.info("Reading in Images...")
        images = [img for img in os.listdir(img_dir) if img.endswith(".jpg")]
        images.sort()
        # Compile image array into a video
        logging.info("Compiling video...%s", vid_path)
        vid_writer = cv2.VideoWriter(vid_path, FOURCC, fps, img_res)
        for filename in images:
            img = cv2.imread(img_dir + filename)  # Read in Raw image
            vid_writer.write(img)              # writes out each frame to the video file
        vid_writer.release()
        print("Time-Lapse Released!\n")

if __name__ == "__main__":# Define Path names
    IMGDIR = RTDIR + "/autocaps/"
    OUTDAT = RTDIR + "/data/"
    VID_DIR = RTDIR + "/Flask/static"
    tl = Timelapse()


    VID_NAME = f"{VID_DIR}/time-lapse.mp4"      # video name
    FOURCC = cv2.VideoWriter_fourcc(*'mp4v')    # video format
    FPS = 24                                    # video fps
    RAW_SIZE = (3280, 2465)                     # camera resolution
    IMG_SIZE = (1920, 1080)                     # video resolution

    tl.gen_timelapse(img_dir=IMGDIR, vid_path=VID_NAME, fps=FPS, img_res=IMG_SIZE)
    