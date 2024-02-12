""" timelapse.py

    Handles interactions with the timelapse video
    TODO: Localize Image class to here (even if separate file)
    TODO: Grab new frame and construct a new timelapse with a single call
    TODO: Save raw frames and apply overlay modifications only when adding to timelapse
"""
import logging
import os
import sys
from tkinter import filedialog
import image

import cv2
import numpy as np
from numpy.typing import NDArray

FOURCC = cv2.VideoWriter_fourcc(*'mp4v')

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

        self.path = path
        self.set_name = os.path.relpath(path, os.getcwd() + "/data/")
        logging.info("Path: %s", self.path)
        logging.info("Set: %s", self.set_name)

    def append_frames(self, existing_video_path, new_frames) -> None:
        """ Read in an existing video, then append one or more frames from a list.

        Args:
            existing_video_path (str): the path to the video to be modified
            new_frames (list(NDArray)): list of frames to be appended
        """
        # Extract parameters from existing video
        cap = cv2.VideoCapture(existing_video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Create a new, temporary video
        new_video_path = os.path.dirname(existing_video_path) + "appended_video.avi"
        writer = cv2.VideoWriter(new_video_path, FOURCC, fps, (width, height))

        # Loop through the old video
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            writer.write(frame)

        # Append the new frames
        for new_frame in new_frames:
            writer.write(new_frame)

        # Clean up
        cap.release()
        writer.release()

        # Overwrite the old video
        os.remove(existing_video_path)
        os.rename(new_video_path, existing_video_path)

    def video_from_frames(self, img_res, fps = 24) -> None:
        """ Generates a video from existing frames, can be a custom resolution or custom framerate.

        Args:
            img_res (tuple): resolution of the output video, (x,y)
            fps (int, optional): FPS of the output video, higher is smoother but shorter. Defaults to 24.
        """
        # Read in current directory of images
        img_dir = f"{self.path}/autocaps/"
        vid_name = f"{self.path}/{self.set_name}_timelapse_{fps}fps.mp4"
        logging.info("Reading in Images:\t%s", img_dir)

        # Generate a list of all the frames in the image directory, then sort chronologically
        images = [img for img in os.listdir(img_dir) if img.endswith(".jpg")]
        images.sort()

        # Compile image array into a video
        logging.info("Compiling video:\t%s", vid_name)
        vid_writer = cv2.VideoWriter(vid_name, FOURCC, fps, img_res)
        for filename in images:
            img = cv2.imread(img_dir + filename)  # Read in Raw image
            vid_writer.write(img)              # writes out each frame to the video file
        vid_writer.release()
        logging.info("Time-Lapse Released!\n")

if __name__ == "__main__":# Define Path names
    tl = Timelapse()

    FPS = 48                                    # video fps
    IMG_SIZE = (1920, 1080)                     # video resolution

    # Using Default FPS (24). 1sec/day
    tl.video_from_frames(img_res=IMG_SIZE)
    # Using Custom FPS (48, faster). 0.5sec/day
    tl.video_from_frames(img_res=IMG_SIZE, fps=FPS)
