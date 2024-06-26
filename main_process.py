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
import logging

import cv2

import process
from database import Database
import pandas as pd
import logFormat

# from tkinter import filedialog
logFormat.format_logs(logger_name="Process")
logger = logging.getLogger("Process")


### Start Initial Setup ###
# Versions
logger.info("Version Diagnostics:")
logger.info("OS type: %s", os.name)
logger.info("Platform: %s", sys.platform)

# Acquire initial data
NOW = datetime.datetime.now()
M = NOW.strftime("%m")
D = NOW.strftime("%d")
H = NOW.strftime("%H")
TIMESTAMP = NOW.strftime("%Y-%m-%d_%Hh")
logger.info("Current time: %s\n", NOW)


# Define Path names
RTDIR = os.path.dirname(__file__)

options = [os.path.basename(filename) for filename in os.listdir(f"{RTDIR}/data")]
logger.info("Dataset options:")
for key, dat in enumerate(options):
    logger.info("(%d) %s", key, dat)
sel = int(input("Which dataset do you want to process? "))

DATASET = f"{RTDIR}/data/{options[sel]}/"
IMGDIR = DATASET + "/autocaps/"

# If autocaps or data don't exist, create them! They are gitignored...
if not os.path.exists(DATASET):
    os.makedirs(DATASET)
if not os.path.exists(IMGDIR):
    os.makedirs(IMGDIR)

FPS = 24                                    # video fps
IMG_SIZE = (1920, 1080)                     # video resolution

logger.info("Root: %s", RTDIR)
logger.info("Current Dataset: %s\n", DATASET)
#### End Initial Setup ####

def process_data():
    """ Main Runner for the Processing section

        TODO: add more functionality, options, and branches here
        TODO: process.DATASET may be better as a command line argument or a function parameter
    """
    ### Start Post Processing Video Compilation ###
    logger.info("Loading Database")
    db = Database(db_name="dat.db", db_path=DATASET)
    try:
        df = db.get_df(options[sel])

        logger.info("Starting Graphs")
        vis = process.Vizualizer(dframe=df, out_path=DATASET)

        ## Start Generate Plots ###
        # Plot Total Light
        vis.gen_plot(
            y_label="Light_Intensity"
        )

        # Plot Total Soil Moisture
        vis.gen_plot(
            y_label="Soil_Moisture"
        )

        # Plot Total Temperature
        vis.gen_plot(
            y_label="Temperature"
        )

        # Plot Total Humidity
        vis.gen_plot(
            y_label="Humidity"
        )
    ## End Generate Plots ##
    except pd.errors.DatabaseError as e:
        logger.error("Failed to open table")
        logger.error(e)


    logger.info("Starting Timelapse")
    tl = process.Timelapse(path=DATASET)
    # TODO: Append frames to save time instead of compiling the whole video
    # if os.path.exists(f"{DATASET}")
    tl.video_from_frames(img_res=IMG_SIZE, fps=FPS)
    #### End Post Processing Video Compilation ####

if __name__ == "__main__":
    sys.exit(process_data())
