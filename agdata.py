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
        lst = {
            'Iteration': [],
            'Name': [],
            'Month': [],
            'Day': [],
            'Hour': [],
            'Soil Moisture': [],
            'Avg SM': [],
            'Temperature': [],
            'Avg T': [],
            'Humidity': [],
            'Avg H': [],
            'Light Intensity': [],
            'Avg L': [],
            'Watered?': [],
            'Amount Watered': [],
            'Days without water': []
        }
        df = pd.DataFrame(lst)

    return df

def app_dat(img_name: str, m: int, d: int, h: int, df: pd.DataFrame, SENSOR_ARR) -> pd.DataFrame:
    """
    Temp Docstring
    """

    # Process and Store the new data
    print("Appending New Data..")
    new_row = {
        1,
        img_name,
        m,
        d,
        h,
        SENSOR_ARR[0],
        df['Soil Moisture'].mean(),
        SENSOR_ARR[1],
        df['Temperature'].mean(),
        SENSOR_ARR[2],
        df['Humidity'].mean(),
        SENSOR_ARR[3],
        df['Light Intensity'].mean(),
        0,
        0,
        1
    }
    df.append_row(new_row)

    return df
