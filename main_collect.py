#!/usr/bin/env python3
"""
Docstring for camera.py.
"""

import datetime
import logging
import os
import sys
import time

import collect

# Initial Logger Settings
FMT_MAIN = "%(asctime)s\t| %(levelname)s\t| Main_Collect:\t%(message)s"
logging.basicConfig(format=FMT_MAIN, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")

# Define Path names
RTDIR = os.getcwd()
DATASET = RTDIR + "/data/AeroGarden1/"
IMGDIR = DATASET + "/autocaps/"
IMG_SIZE = (1920, 1080)                     # video resolution

# If autocaps or data don't exist, create them! They are gitignored...
if not os.path.exists(DATASET):
    os.makedirs(DATASET)
if not os.path.exists(IMGDIR):
    os.makedirs(IMGDIR)


def collect_data(now: datetime.datetime, sensors: bool = True, camera: bool = True):
    """_summary_
    """
    # Acquire initial data
    logging.info("Current time: %s", now)
    timestamp = now.strftime("%Y-%m-%d_%Hh")
    img_name = f"{IMGDIR}{timestamp}.jpg"            # image name

    logging.info("Output Image: %s", img_name)

    if sensors:
        ### Start Acquire Sensor Measurements ###
        data = collect.acq_data(DATASET)
        new_dat = collect.acq_sensors()
        it = len(data["Date"])
        # TODO: Add code to process watering
        data = collect.app_dat(now,it,0,data,new_dat)
        # CSV output
        # Pandas Method
        # TODO: Replace with SQL
        data.to_csv(path_or_buf=DATASET+"dat.csv",header=True,index=False)
        logging.info(f"{data=}")
        #### End Acquire Sensor Measurements ####

    if camera:
        collect.acq_img(tstmp=now,
                        raw_size=IMG_SIZE,
                        flash=True,
                        name=img_name)  # Capture Image

    logging.info("Scan Finished for %s", timestamp)

def scheduler(camera: bool = True,
              sensors: bool = True,
              interval: datetime.timedelta = None,
              round_down: bool = True) -> bool:
    """_summary_

    Args:
        camera (bool, optional): _description_. Defaults to True.
        sensors (bool, optional): _description_. Defaults to True.
        interval (datetime.timedelta | None, optional): _description_. Defaults to None.
        round_down (bool, optional): _description_. Defaults to True.

    Returns:
        bool: _description_
    """
    # Set the default time interval between collections
    if interval is None:
        interval = datetime.timedelta(hours=1)

    # Set the time of the last scan
    last_scan = datetime.datetime.now()
    # If the scan happend part way through the hour, determine if it should be rounded down
    if round_down:
        last_scan = last_scan.replace(minute=0, second=0, microsecond=0)
    collect_data(last_scan, camera=camera, sensors=sensors)

    # Main program loop
    while True:
        if datetime.datetime.now() > last_scan + interval:
            # Update the most recent timestamp
            last_scan = datetime.datetime.now()
            collect_data(last_scan, camera=camera, sensors=sensors)
        else:
            time.sleep(1)

if __name__ == "__main__":
    logging.info("Version Diagnostics:")
    logging.info("OS type: %s", os.name)
    logging.info("Platform: %s\n", sys.platform)

    logging.info("Root Directory: %s", RTDIR)
    logging.info("Current Dataset: %s", DATASET)

    sys.exit(scheduler(sensors=False))
