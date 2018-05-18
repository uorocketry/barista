from app.utils.i2c import I2C
from time import sleep
import logging
import numpy as np


MPL3115A2_ADDRESS = 0x60
STATUS_REG = 0x00
OUT_P_MSB = 0x01
OUT_T_MSB = 0x04
CTRL_REG1 = 0x26
OFF_H = 0x2D
PT_DATA_CFG = 0x13


class Altimeter(object):
    def __init__(self):
        self.bus = I2C(1, MPL3115A2_ADDRESS)

        self.bus.write_byte(CTRL_REG1, 0xB8) #OSR = 128 to set to altimeter TODO: delete later

        self.bus.write_byte(PT_DATA_CFG, 0x07)

        self.bus.write_byte(CTRL_REG1, 0xB9) #activate polling
        offset_height = 70 ## Ottawa altitude: 70 m, Las Cruses altitude: 1,189 m
        offset_height = np.binary_repr(-offset_height, width = 8)
        offset_height = int(offset_height, 2)
        self.bus.write_byte(OFF_H, offset_height)

        status = self.read_byte(STATUS_REG)

        while (status & 0x08) == False:
            self.read_byte(STATUS_REG)

    def read_altitude(self):
        raw_data = self.bus.read_block(OUT_P_MSB, 3)
        return Altimeter.parse_raw_data_altitude(raw_data)

    def read_temp(self):
        raw_data = self.bus.read_block(OUT_P_MSB, 2)
        return Altimeter.parse_raw_data_temp(raw_data)


##//MAYBE
    def read_bar_setting(self):
        setting = self.bus.read_block(BAR_IN_MSB, 2)
        try:
            return parse_raw_data(setting)*2
        except Exception as e:
            logging.error('error: %s, raw_data: %s', e, raw_data)
            return(-1)

    #Parameter is bar setting/2
    def write_bar_setting(self, input):
        if input < 0 or input > 131071:
            raise ValueError('Input out of acceptable bounds.')
        else:
            self.bus.write_block(BAR_IN_MSB, int(input))
            setting = read_bar_setting()
##MAYBE

    @staticmethod
    def parse_raw_data_altitude(raw_data):

        str_msb = '{0:08b}'.format(raw_data[0])
        str_csb = '{0:08b}'.format(raw_data[1])
        str_lsb = '{0:08b}'.format(raw_data[2])

        parsed_data = str_msb + str_csb + str_lsb[3] + str_lsb[2] + str_lsb[1] + str_lsb[0]

        parsed_altitude = int(parsed_data, 2)
        parsed_altitude = np.binary_repr(-parsed_altitude, width = 20)
        parsed_altitude = int(parsed_altitude, 2)

        return parsed_altitude

    def parse_raw_data_temp(raw_data):

        str_msb = '{0:08b}'.format(raw_data[0])
        str_lsb = '{0:08b}'.format(raw_data[1])

        parsed_data = str_msb + str_lsb[3] + str_lsb[2] + str_lsb[1] + str_lsb[0]

        parsed_temp = int(parsed_data, 2)
        parsed_temp = np.binary_repr(-parsed_temp, width = 16)
        parsed_temp = int(parsed_temp, 2)

        return parsed_temp
