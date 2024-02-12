""" @file       main_process.py
    @author     Sean Duffie
    @brief      Main Runner for the data processing half of the program.

    This is where the timelapse will be generated, the webpage will be run, and all graphics will
    be drawn. Much of this is computationally expensive. It neither needs to be run in real
    time, nor does it need to be run on the original Raspberry Pi.
"""
import datetime
import os
import sys

import cv2

import process

# from tkinter import filedialog



### Start Initial Setup ###
# Versions
print("Version Diagnostics:")
print("OS type: ", os.name)
print("Platform: ", sys.platform)

# Acquire initial data
NOW = datetime.datetime.now()
M = NOW.strftime("%m")
D = NOW.strftime("%d")
H = NOW.strftime("%H")
TIMESTAMP = NOW.strftime("%Y-%m-%d_%Hh")
print("Current time: ", NOW)
print()

# Define Path names
RTDIR = os.getcwd()
DATASET = RTDIR + "/data/AeroGarden1/"
IMGDIR = DATASET + "/autocaps/"

# If autocaps or data don't exist, create them! They are gitignored...
if not os.path.exists(DATASET):
    os.makedirs(DATASET)
if not os.path.exists(IMGDIR):
    os.makedirs(IMGDIR)

VID_NAME = f"{process.DATASET}time-lapse.mp4"      # video name
FOURCC = cv2.VideoWriter_fourcc(*'mp4v')    # video format
FPS = 24                                    # video fps
RAW_SIZE = (3280, 2465)                     # camera resolution
IMG_SIZE = (1920, 1080)                     # video resolution


def process_data():
    """ Main Runner for the Processing section

        TODO: add more functionality, options, and branches here
        TODO: process.DATASET may be better as a command line argument or a function parameter
    """
    ### Start Post Processing Video Compilation ###
    db = process.Database(process.DATASET)
    ## Start Generate Plots ###
    # Plot Total Light
    db.gen_plot(
        y_label="Light Intensity"
    )

    # Plot Total Soil Moisture
    db.gen_plot(
        y_label="Soil Moisture"
    )

    # Plot Total Temperature
    db.gen_plot(
        y_label="Temperature"
    )

    # Plot Total Humidity
    db.gen_plot(
        y_label="Humidity"
    )
    ## End Generate Plots ##

    tl = process.Timelapse(VID_NAME)
    tl.video_from_frames(img_res=IMG_SIZE, fps=FPS)
    #### End Post Processing Video Compilation ####

if __name__ == "__main__":
    sys.exit(process_data())
