""" @file       main_process.py
    @author     Sean Duffie
    @brief      Main Runner for the data processing half of the program.

    This is where the timelapse will be generated, the webpage will be run, and all graphics will
    be drawn. Much of this is computationally expensive. It neither needs to be run in real
    time, nor does it need to be run on the original Raspberry Pi.
"""
import sys

import process


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

    tl = process.Timelapse(DATASET)
    tl.video_from_frames(img_res=IMG_SIZE, fps=FPS)
    #### End Post Processing Video Compilation ####

if __name__ == "__main__":
    sys.exit(process_data())
