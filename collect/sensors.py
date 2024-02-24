""" @file       sensors.py
    @author     Sean Duffie
    @brief      Responsible for collecting the data from sensors, as well as loading existing
                data from database.

    This is configured

    TODO: Incorporate SQL into the database interaction
    FIXME: Loading up existing data takes time and only increases as more points are collected,
            figure out a way to do this faster or without loading everthing
"""
import pandas as pd

from .constants import RPI

if RPI:
    import board
    import digitalio
    from adafruit_bme280 import basic as adafruit_bme280

    from .mcp_3008 import MCP3008


def acq_sensors(now: str) -> list():
    """ Read in sensor data from RPI sensors

    The RPI flag allows this to run on Windows without the sensors.
    This is currently set up for collecting the raw ADC of a capacitive soil moisture sensor and a
    resistive photovoltaic cell, then the Temperature and Humidity from a BME280.

    FIXME: create a dictionary to return so the output type can be documented/predictable

    Returns:
        - list: Array of values acquired from the sensors
    """
    # sensor_arr = pd.DataFrame()

    # Update MCP3008 ADC Values
    if RPI:
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.D7)
        bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)
        bme280.sea_level_pressure = 1013.4

        adc = MCP3008()

        soil_adc = 1024 - adc.read(0)
        light_adc = adc.read(1)

        # # Adjust percentage
        # smin = 1024
        # lmin = 1024
        # smax = 0
        # lmax = 0
        # soil = 100*(soil_adc-smin)/(smax-smin+1)
        # light = 100*(light_adc-lmin)/(lmax-lmin+1)

        # Append to list
        sensor_arr = pd.DataFrame([[now, soil_adc, light_adc, bme280.temperature, bme280.humidity]])
    else:
        sensor_arr = pd.DataFrame([[now, 0, 0, 0, 0]])

    # Receive the Response from the sensors
    for row in sensor_arr.itertuples(index=False, name=None):
        return row
