import csv
import json
from os.path import exists
from time import sleep
from typing import Any, List, Union
import time
from MCP3008 import MCP3008
import board
import digitalio
from adafruit_bme280 import basic as adafruit_bme280

import pandas as pd
import serial
from serial.tools import list_ports

Num = Union[int, float]

# struct data (headers/rows/cols)
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
    """
    Temp Docstring
    """
    SENSOR_ARR = list()

    # Update MCP3008 ADC Values
    soil_adc = 1024 - adc.read(0)
    light_adc = adc.read(1)

    # # Adjust percentage
    # soil = 100*(soil_adc-smin)/(smax-smin+1)
    # light = 100*(light_adc-lmin)/(lmax-lmin+1)

    # Append to list
    SENSOR_ARR.append(soil_adc)
    SENSOR_ARR.append(light_adc)
    SENSOR_ARR.append(bme280.temperature)
    SENSOR_ARR.append(bme280.humidity)

    # Receive the Response from the sensors
    print(SENSOR_ARR)
    print()

    return SENSOR_ARR

def acq_data(OUTDAT: str) -> pd.DataFrame:
    """
    Temp Docstring
    """
    # TODO: Add timing and test different methods (pyarrow?)

    # Read data history
    if (exists(OUTDAT + "dat.csv")):
        print("Loading current file...")
        df = pd.read_csv(OUTDAT + 'dat.csv')
    elif (exists(OUTDAT + "dat.json")):
        print("Loading current file...")
        f = open(OUTDAT + "dat.json", encoding="utf-8")
        df = json.load(f)
        f.close()
    else:
        df = pd.DataFrame(columns = [
                'Name',
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

    return df

def app_dat(img_name: str, it: int, m: int, d: int, h: int, w: int, df: pd.DataFrame, new_dat: pd.DataFrame) -> pd.DataFrame:
    """
    Temp Docstring
    """

    # Process and Store the new data
    print("Appending New Data..")
    day_wat = 0
    amt_wat = 0
    if w:
        amt_wat += 1
    if it > 0:
        day_wat = int(df["Days without water"][it-1]) + 1
        amt_wat += df["Days without water"][it-1]
    new_row = [
        img_name,
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
