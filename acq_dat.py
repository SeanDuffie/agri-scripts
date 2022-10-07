from os.path import exists
from time import sleep
import csv
import json
from typing import Any
import serial
from serial.tools import list_ports

def acq_data(name: str, outdat: str) -> list(list(Any)):
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
    except:
        print("Something went wrong with decoding!")
        pass

    # Read data history
    if (exists(outdat + "dat.json")):
        print("Loading current file...")
        f = open(outdat + "dat.json", encoding="utf-8")
        data = json.load(f)
        f.close()
    elif (exists(outdat + "dat.csv")):
        # reading csv file
        with open(outdat + "dat.csv", 'r', encoding="utf-8") as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            
            # extracting field names through first row
            fields = next(csvreader)
        
            # extracting each data row one by one
            for row in csvreader:
                rows.append(row)
        
            # get total number of rows
            print("Total no. of rows: %d"%(csvreader.line_num))
    else:
        data = {
            "TIME": list(),
            "LIGHT": [],
            "SOIL": [],
            "TEMPC": [],
            "TEMPF": [],
            "HUMID": []
        }
    # Process and Store the new data
    print("Appending New Data..")
    data["TIME"].append(name)
    data["LIGHT"].append(float(SENSOR_ARR[0]))
    data["SOIL"].append(float(SENSOR_ARR[1]))
    data["TEMPC"].append(float(SENSOR_ARR[2]))
    data["TEMPF"].append(float(SENSOR_ARR[2])*(9/5)+32)
    data["HUMID"].append(float(SENSOR_ARR[3]))

    return data