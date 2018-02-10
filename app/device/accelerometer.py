from app.utils.i2c import I2C
from time import sleep
from time import time
import numpy as np


ADDRESS = 0x53
#REGISTERS
DEVID = 0x00
BW_RATE = 0x2C # Data rate and power mode control
POWER_CTL = 0x2D # Power-saving features control
DATA_FORMAT = 0x31
DATAX0 = 0x32
DATAX1 = 0x33
DATAY0 = 0x34
DATAY1 = 0x35
DATAZ0 = 0x36
DATAZ1 = 0x37


class Accelerometer(object):


    def __init__(self):
        self.i2c = I2C(1, ADDRESS)
        #clearing DATA_FORMAT register
        self.i2c.write_byte(DATA_FORMAT,0b00000000)
        #set range to plusminus 8g
        self.i2c.set_bit(DATA_FORMAT, 1)
        self.i2c.set_bit(DATA_FORMAT, 0)
        #right justify with sign extension
        self.i2c.clear_bit(DATA_FORMAT, 2)
        #set maximum resolution mode (4mg/LSB)
        self.i2c.set_bit(DATA_FORMAT, 3)
        #set data rate to 3200Hz
        self.i2c.write_byte(BW_RATE, 0b00001111)
        #setting the device to measure
        self.i2c.set_bit(POWER_CTL, 3)


    def read(self):
        return Accelerometer.parse_raw_data(self.i2c.read_block(DATAX0,6))


    def sleep(self):
        self.i2c.set_bit(POWER_CTL, 2)


    def wake(self):
        self.i2c.clear_bit(POWER_CTL, 3)
        self.i2c.clear_bit(POWER_CTL, 2)
        self.i2c.set_bit(POWER_CTL, 3)


    @staticmethod
    def parse_raw_data(raw_data):

        xyz = np.int16([
            raw_data[1] << 8 | raw_data[0],
            raw_data[3] << 8 | raw_data[2],
            raw_data[5] << 8 | raw_data[4]
        ])

        return {
            'x': round(xyz[0]*0.0039,4),
            'y': round(xyz[1]*0.0039,4),
            'z': round(xyz[2]*0.0042,4),
            'time':time()
        }


if __name__ == '__main__':
        accelerometer = Accelerometer()
        sleep(1)
        print accelerometer.read()
