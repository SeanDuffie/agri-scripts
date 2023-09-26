import time
from MCP3008 import MCP3008
import board
import digitalio
from adafruit_bme280 import basic as adafruit_bme280

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D7)
bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)
bme280.sea_level_pressure = 1013.4

adc = MCP3008()

smin = 1024
lmin = 1024
smax = 0
lmax = 0

values = [0,0,0,0,0,0,0,0]
while True:
    # Update MCP3008 ADC Values
    for i in range(2):
        values[i] = adc.read( channel = i ) # You can of course adapt the channel to be read out
    
    rawsoil = 1024-values[0]
    rawlight = values[1]

    # Refresh range
    if rawsoil < smin:
        smin = rawsoil
    if rawsoil > smax:
        smax = rawsoil
    if rawlight < lmin:
        lmin = rawlight
    if rawlight > lmax:
        lmax = rawlight

    # Adjust percentage
    soil = 100*(rawsoil-smin)/(smax-smin+1)
    light = 100*(rawlight-lmin)/(lmax-lmin+1)

    # Print results
    print(f"Soil Moisture: {soil}%\t({smin}-{smax})")
    print(f"Light Intensity: {light}%\t({lmin}-{lmax})")
    print("Temperature: %0.1f C" % bme280.temperature)
    print("Humidity: %0.1f %%\n" % bme280.humidity)
    # print("Pressure: %0.1f hPa" % bme280.pressure)
    # print("Altitude = %0.2f meters" % bme280.altitude)
    # print("Applied voltage: %.2f" % (value / 1023.0 * 3.3) )
    time.sleep(1)