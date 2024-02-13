""" @file       sensors.py
    @author     Sean Duffie
    @brief      Responsible for collecting the data from sensors, as well as loading existing
                data from database.

    This is configured
    
    TODO: Incorporate SQL into the database interaction
    FIXME: Loading up existing data takes time and only increases as more points are collected,
            figure out a way to do this faster or without loading everthing
"""
import json
import os

import pandas as pd

from .constants import RPI

if RPI:
    import board
    import digitalio
    from adafruit_bme280 import basic as adafruit_bme280

    from .mcp_3008 import MCP3008

    spi = board.SPI()
    cs = digitalio.DigitalInOut(board.D7)
    bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)
    bme280.sea_level_pressure = 1013.4

    adc = MCP3008()

smin = 1024
lmin = 1024
smax = 0
lmax = 0

def acq_sensors() -> list():
    """ Read in sensor data from RPI sensors

    The RPI flag allows this to run on Windows without the sensors.
    This is currently set up for collecting the raw ADC of a capacitive soil moisture sensor and a
    resistive photovoltaic cell, then the Temperature and Humidity from a BME280.

    FIXME: create a dictionary to return so the output type can be documented/predictable

    Returns:
        - list: Array of values acquired from the sensors
    """
    sensor_arr = []

    # Update MCP3008 ADC Values
    if RPI:
        soil_adc = 1024 - adc.read(0)
        light_adc = adc.read(1)

    # # Adjust percentage
    # soil = 100*(soil_adc-smin)/(smax-smin+1)
    # light = 100*(light_adc-lmin)/(lmax-lmin+1)

    # Append to list
    if RPI:
        sensor_arr.append(soil_adc)
        sensor_arr.append(light_adc)
        sensor_arr.append(bme280.temperature)
        sensor_arr.append(bme280.humidity)
    else:
        sensor_arr.append(0)
        sensor_arr.append(0)
        sensor_arr.append(0)
        sensor_arr.append(0)

    # Receive the Response from the sensors
    print(f"{sensor_arr=}")
    print()

    return sensor_arr

def acq_data(dirname: str) -> pd.DataFrame:
    """ Reads in all existing data from database

    NOTE: If there is no database, creates a blank one with headers

    FIXME: Research better database methods (SQL?)

    Args:
        dirname (str): path leading to the dataset directory

    Returns:
        pd.DataFrame: populated pandas dataframe
    """
    # TODO: Add timing and test different methods (pyarrow?)

    # Read data history
    if os.path.exists(dirname + "dat.csv"):
        print("Loading current CSV file...")
        d_frame = pd.read_csv(dirname + 'dat.csv')
    elif os.path.exists(dirname + "dat.json"):
        print("Loading current JSON file...")
        with open(dirname + "dat.json", encoding="utf-8") as json_file:
            d_frame = json.load(json_file)
    else:
        # Pandas Dataframe w/ headers
        d_frame = pd.DataFrame(columns = [
                'Date',
                'Month',
                'Day',
                'Hour',
                'Soil Moisture',
                'Light Intensity',
                'Temperature',
                'Humidity',
                'Watered?',
                'Amount Watered',
                'Days without water'
            ]
        )

    return d_frame

def app_dat(date: str, it: int, m: int, d: int, h: int, w: int, df: pd.DataFrame, new_dat: pd.DataFrame) -> pd.DataFrame:
    """ Process and Store the new data

    FIXME: Research better insertion methods (SQL?)

    Args:
        date (str): Date of the image, filename and/or timestamp
        it (int): iterator
        m (int): month
        d (int): day
        h (int): hour
        w (bool): Whether water was added or not
        df (pd.DataFrame): original dataframe
        new_dat (pd.DataFrame): new dataframe entry

    Returns:
        pd.DataFrame: New dataframe with additional entry appended
    """

    # 
    print("Appending New Data..")
    day_wat: int = 0
    amt_wat: int = 0

    # Load in previous entries if the list isn't empty
    if it > 0:
        day_wat = int(df["Days without water"][it-1])
        amt_wat = int(df["Amount Watered"][it-1])

    # If Pump was activated, iterate the water counter, else iterate dry
    if w:
        amt_wat += 1
    else:
        day_wat += 1

    # Package and append new dataframe entry
    new_row = [
        date,
        m,
        d,
        h,
        new_dat[0],
        new_dat[1],
        new_dat[2],
        new_dat[3],
        w,
        amt_wat,
        day_wat
    ]
    df.loc[len(df.index)] = new_row
    # df = pd.concat([df, new_row], axis=1).reset_index(drop=True)

    return df
