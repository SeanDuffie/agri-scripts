# agri-scripts

## Purpose

Python script to run on Raspberry Pi. Acquires image and serial Arduino measurements on specified intervals, then compiles time-lapse and data.

## How it works
This uses either the PiCamera module or a USB Webcam with OpenCV VideoCapture to acquire frames.
Early on in the project, it used a series of sensors connected to an arduino, then communicated
over a serial connection, however this was later replaced with a local sensors and an MCP3008 ADC.

In the future, I will add controls for a water pump, an ultrasonic sensor to measure water level in reservoir, and webhooks to control the smart plugs connected to the UV light and heating mat.



## How to use it

Hardware setup:
1. Sensors
    1. BME280 - Temperature and Humidity
    2. TODO: HC-SR05 - Ultrasonic distance sensor for water level
    3. MCP3008 - 8 Channel SPI ADC
        1. Photoresistor - Pull Down resistor attached to VCC for better accuracy
        2. Capacitive Soil Moisture Sensor - largest physical sensor, placed in soil.
2. Connections
    - SPI
        - MOSI
        - MISO
        - VCC
        - GND
        - CS (BME280)
        - CS (MCP3008)
    - Camera - Either PiCamera module or USB Webcam
    - Other Peripherals
        - Water pump
            - Output: Trigger a relay or power from GPIO
        - Ultrasonic Sensor
            - Output: Trigger Pin - Instructs sensor to send ultrasonic pulse
            - Input: Echo pin - reads response from sensor, time diff determines distance

Running the Code:

        # Install Requirements
        python3 pip install -r ./requirements_rpi.txt

        # Run once to test
        python3 camera.py
        # After this, it should have taken a picture and created the first csv entry

        # Usually it will be desired to automate the capture process
        crontab -e

        # Add the following line to the crontab file
        0 * * * * python3 /{path-to-project}/camera.py

Flask Server:

        # Launch the server
        python3 server.py

        # Open a browser to the ip of the Raspberry Pi
        # Default="127.0.0.1"; Local_ip=""; URL="sduffie.ddns.net"

        # Launch the server automatically on startup
        # Add this line to crontab -e
        @reboot python3 /{path-to-project}/Flask/server.py

## Profiling

    https://www.turing.com/kb/python-code-with-cprofile
    ```
    python -m cProfile -o program.prof .\main_collect.py
    python -m snakeviz .\program.prof
    ```
