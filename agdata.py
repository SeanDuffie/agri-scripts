from os.path import exists
from time import sleep
import csv
import json
import pandas as pd
from typing import Any, Union, List
import serial
from serial.tools import list_ports

Num = Union[int, float]

# struct data (headers/rows/cols)

def acq_sensors() -> list():
    """
    Temp Docstring
    """
    PORT_LIST = list(list_ports.comports())
    # for p in PORT_LIST:
    #     print("  - ", p.device)
    # print()

    # Setting up Serial connection
    ser = serial.Serial(
        # port='/dev/ttyACM0', # use this to manually specify port
        port=PORT_LIST[0].device,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=10
    )

    # Send out requests until a response is received
    while ser.in_waiting == 0:
        print("Waiting for sensors...")
        ser.write('1'.encode('utf-8'))
        sleep(.5)
    print()

    # Receive the Response from the sensors
    SENSOR_ARR = list()
    try:
        print("Reading Response...")
        FEEDBACK = ser.readline()
        SENSOR_READ = FEEDBACK.decode("Ascii")
        SENSOR_ARR = SENSOR_READ.split(",")
        print(SENSOR_ARR)
        print()
        return SENSOR_ARR
    except:
        print("Something went wrong with decoding!")

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
                'Light Intensity',
                'Avg L',
                'Soil Moisture',
                'Avg SM',
                'Temperature',
                'Avg T',
                'Humidity',
                'Avg H',
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
        df['Light Intensity'].mean(),
        new_dat[1],
        df['Soil Moisture'].mean(),
        new_dat[2],
        df['Temperature'].mean(),
        new_dat[3],
        df['Humidity'].mean(),
        w,
        amt_wat,
        day_wat
    ]
    df.loc[len(df.index)] = new_row
    # df = pd.concat([df, new_row], axis=1).reset_index(drop=True)

    return df
