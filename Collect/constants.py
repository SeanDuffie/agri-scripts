""" @file       constants.py
    @author     Sean Duffie
    @brief      Stores all constant variables that are shared throughout the "Collect" module
"""

import sys

RPI = False
BIT64 = False
SET_NAME = "English_Ivy"

# Determine if the OS platform is Linux (if so then probably is a Raspberry Pi)
if sys.platform.startswith("linux"):
    RPI = True

    # Determine if RPI has 64 bit OS, necessary for the different version of picamera
    if sys.platform.find("64"):
        BIT64 = True
