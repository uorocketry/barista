from app.utils.i2c import I2C
from time import sleep
import numpy as np
import logging


MPL3115A2_ADDRESS = 0x60
STATUS_REG = 0x00
OUT_P_MSB = 0x01
OUT_T_MSB = 0x04
CTRL_REG1 = 0x26
OFF_H = 0x2D
PT_DATA_CFG = 0x13
BAR_IN_MSB = 0x14
BAR_IN_LSB = 0x15


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

        logging.info('Altimeter Initialized')
        self.reset_bar_input()


    def read_altitude(self):
        raw_data = self.bus.read_block(OUT_P_MSB, 3)
        try:
            return (Altimeter.parse_raw_data(raw_data)-self.init_height) # m
        except Exception as e:
            logging.error('error: {}, raw_data: {}'.format(e, raw_data))
            return -999.999

    def read_temp(self):
        raw_data = self.bus.read_block(OUT_T_MSB, 2)
        return Altimeter.parse_raw_data(raw_data) # degrees C


    def reset_bar_input(self):
        self.bus.write_byte(0x14, 0xC5)
        self.bus.write_byte(0x15, 0xE7)

        self.init_height = self.read_altitude()
        if self.init_height == -999.999:
            self.init_height = 1400 # m

    def read_bar_setting(self):
        setting = self.bus.read_block(BAR_IN_MSB, 2)

        str_msb = '{0:08b}'.format(setting[0])
        str_lsb = '{0:08b}'.format(setting[1])
        parsed_setting = str_msb + str_lsb
        parsed_setting = int(parsed_setting, 2) *2 #Parameter is bar setting/2
        return parsed_setting

    def write_bar_setting(self, input):
        #Parameter is bar setting/2
        if input < 0 or input > 131071:
            raise ValueError('ERROR: Input out of acceptable bounds.')
        else:
            equiv_pressure = input/2             ## 101950 for Ottawa, 109975 for Las Cruces
            equiv_pressure = np.binary_repr(equiv_pressure, width = 16)
            equiv_pressure = equiv_pressure[-16:]
            equiv_pressure_msb = int(equiv_pressure[0:8], 2)
            equiv_pressure_lsb = int(equiv_pressure[8:], 2)

            self.bus.write_byte(BAR_IN_MSB, equiv_pressure_msb)
            self.bus.write_byte(BAR_IN_LSB, equiv_pressure_lsb)


    @staticmethod
    def parse_raw_data(raw_data):
        if len(raw_data) == 3:
            str_msb = '{0:08b}'.format(raw_data[0])
            str_csb = '{0:08b}'.format(raw_data[1])
            str_lsb = '{0:08b}'.format(raw_data[2])

            parsed_data = str_msb + str_csb
            str_length = 16
        else:
            str_msb = '{0:08b}'.format(raw_data[0])
            str_lsb = '{0:08b}'.format(raw_data[1])

            parsed_data = str_msb
            str_length = 8

        data_fractions = str_lsb[0] + str_lsb[1] + str_lsb[2] + str_lsb[3]

        data = int(parsed_data, 2)
        data_fractions = int(data_fractions, 2)

        if str_msb[0] == '1':
            data = np.binary_repr(-data, width = str_length)
            data = data[-str_length:]
            data = -1*int(data, 2)

            data_fractions = np.binary_repr(-data_fractions, width = 4)
            data_fractions = data_fractions[-4:]
            data_fractions = -1*int(data_fractions, 2)

        data_fractions = float(data_fractions)/16

        final_data = data + data_fractions
        return final_data # meters OR degrees C
