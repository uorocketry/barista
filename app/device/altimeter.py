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

        self.bus.write_byte(CTRL_REG1, 0xB8) #OSR = 128 to set to altimeter
        self.bus.write_byte(PT_DATA_CFG, 0x07)
        self.bus.write_byte(CTRL_REG1, 0xB9) #activate polling

        status = self.bus.read_byte(STATUS_REG)
        while (status & 0x08) == False:
            status = self.bus.read_byte(STATUS_REG)
            sleep(0.5)

    def read_altitude(self):
        raw_data = self.bus.read_block(OUT_P_MSB, 3)
        return Altimeter.parse_raw_data_altitude(raw_data)

    def read_temp(self):
        raw_data = self.bus.read_block(OUT_P_MSB, 2)
        return Altimeter.parse_raw_data_temp(raw_data)


##//MAYBE
    # def read_bar_setting(self):
    #     setting = self.bus.read_block(BAR_IN_MSB, 2)
    #     try:
    #         return parse_raw_data(setting)*2
    #     except Exception as e:
    #         logging.error('error: %s, raw_data: %s', e, raw_data)
    #         return(-1)
    #
    # #Parameter is bar setting/2
    # def write_bar_setting(self, input):
    #     if input < 0 or input > 131071:
    #         raise ValueError('Input out of acceptable bounds.')
    #     else:
    #         self.bus.write_block(BAR_IN_MSB, int(input))
    #         setting = read_bar_setting()
##MAYBE

    @staticmethod
    def parse_raw_data_altitude(raw_data):

        str_msb = '{0:08b}'.format(raw_data[0])
        str_csb = '{0:08b}'.format(raw_data[1])
        str_lsb = '{0:08b}'.format(raw_data[2])

        parsed_data = str_msb + str_csb
        parsed_data_fractions = str_lsb[4] + str_lsb[5] + str_lsb[6] + str_lsb[7]

        parsed_altitude = int(parsed_data, 2)
        if str_msb[0] == '1':
            parsed_altitude = np.binary_repr(-1*parsed_altitude, width = 15)
            parsed_altitude = int(parsed_data, 2)

        parsed_altitude_fractions = int(parsed_data_fractions, 2)/16
        if str_lsb[4] == '1':
            parsed_altitude_fractions = -1*parsed_altitude_fractions

        final_altitude = parsed_altitude + parsed_altitude_fractions
        return final_altitude

    def parse_raw_data_temp(raw_data):

        str_msb = '{0:08b}'.format(raw_data[0])
        str_lsb = '{0:08b}'.format(raw_data[1])

        parsed_data = str_msb
        parsed_data_fractions = str_lsb[4] + str_lsb[5] + str_lsb[6] + str_lsb[7]

        parsed_temp = int(parsed_data, 2)
        if str_msb[0] == '1':
            parsed_altitude = np.binary_repr(-1*parsed_altitude, width = 13)
            parsed_altitude = int(parsed_data, 2)

        parsed_temp_fractions = int(parsed_temp_fractions, 2)/16
        if str_lsb[4] == '1':
            parsed_temp_fractions =  -1*parsed_temp_fractions

        final_temp = parsed_temp + parsed_temp_fractions
        return final_temp
