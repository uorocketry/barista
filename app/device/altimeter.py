from app.utils.i2c import I2C
from time import sleep
import logging

MPL3115A2_ADDRESS = 0x60
STATUS_REG = 0x00
OUT_P_MSB = 0x01
OUT_P_DELTA_CSB = 0x08
OUT_P_DELTA_MSB = 0X07
OUT_T_MSB = 0x04
WHOAMI = 0x0C
CTRL_REG1 = 0x26
PT_DATA_CFG = 0x13
BAR_IN_MSB = 0x14


class Altimeter(object):
    def __init__(self):
        self.bus = I2C(1, MPL3115A2_ADDRESS)

        self.bus.write_byte(CTRL_REG1, 0xB8)

        self.bus.write_byte(PT_DATA_CFG, 0x07)

        self.bus.write_byte(CTRL_REG1, 0xB9) #activate polling

        status = self.bus.read_byte(STATUS_REG)
        while (status & 0x08) == False:
            self.bus.read_byte(STATUS_REG)
            ## self.bus.write_byte(MCTRL_REG1, (setting | 0x02))

    def read_pressure(self):
        raw_data = self.bus.read_block(OUT_P_MSB, 3)

        return Altimeter.parse_raw_data(raw_data)

    def read_temp(self):
        raw_data = self.bus.read_block(OUT_P_MSB, 3)

        return Altimeter.parse_raw_data(raw_data)

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

    @staticmethod
    def parse_raw_data(raw_data):
        alt_int = 0
        alt_frac = 0
        str_msb = '{0:08b}'.format(raw_data[0])
        str_csb = '{0:08b}'.format(raw_data[1])
        str_lsb = '{0:08b}'.format(raw_data[2])

        alt_int_bin = str_msb + str_csb + str_lsb[0] + str_lsb[1] + str_lsb[2] + str_lsb[3]
        alt_frac_bin = str_lsb[4] + str_lsb[5] + rstr_lsb[6] + str_lsb[7]

        alt_frac = int(alt_frac_bin,2)/16

        if(alt_int_bin[0] == '1'):
            alt_int = -1*(32768 - int(alt_int_bin, 2))
            alt_frac = -1*alt_frac
        else:
            alt_int = int(alt_int_bin,2)

        alt = alt_int + alt_frac
        return alt
