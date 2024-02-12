""" @file       constants.py
    @author     Sean Duffie
    @brief      Stores all constant variables that are shared throughout the "Collect" module
"""

import sys

RPI = False
BIT64 = False
SET_NAME = "English_Ivy"

if sys.platform.startswith("linux"):
    RPI = True
    import board
    import digitalio
    from adafruit_bme280 import basic as adafruit_bme280
    from MCP3008 import MCP3008

    # Determine if RPI has 64 bit OS, necessary for the different version of picamera
    if sys.platform.find("64"):
        BIT64 = True
