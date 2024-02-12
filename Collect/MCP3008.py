from spidev import SpiDev

class MCP3008:
    """ Objectifies the setup and interactions with the MCP3008.

    This will help simplify the usage of the ADC in the future, allowing us to better handle
    errors and also integrate multiple MCP3008 chips - if needed.
    """
    def __init__(self, bus = 0, device = 0):
        """ Initializes the connection with the MCP3008

        Args:
            bus (int, optional): SPI bus will always be zero on RPI. Defaults to 0.
            device (int, optional): SPI dev depends on Chip Enable, will be 0/1. Defaults to 0.
        """
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000 # 1MHz

    def open(self):
        """ Opens the SPI connection with the MCP3008

        NOTE: Should only be called in the init function
        TODO: Add error handling to return a message when MCP3008 is not connected
        """
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz

    def read(self, channel = 0):
        """ Reads the current ADC value for the given channel

        Args:
            channel (int, optional): The channel to read from (0-7). Defaults to 0.

        Returns:
            int: ADC reading from specified channel
        """
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def close(self):
        """ Closes the SPI connection, should only be called on shutdown or interrupts """
        self.spi.close()
