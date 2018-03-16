from app.utils.i2c import I2C
from time import sleep
import logging

MPL3115A2_ADDRESS = 0x60
STATUS = 0x00
OUT_P_MSB = 0x01
OUT_P_DELTA_CSB = 0x08
OUT_P_DELTA_MSB = 0X07
OUT_T_MSB = 0x04
WHOAMI = 0x0C
CTRL_REG1 = 0x26
PT_DATA_CFG = 0x13
BAR_IN_MSB = 0x14

class Altimeter (object):

    def __init__(self):
        tries = 0;
        while(tries < 5):
            try:
                self.bus = I2C(1, MPL3115A2_ADDRESS)
                #Set oversample rate to 128
                current_setting = self.bus.read_byte(CTRL_REG1)
                new_setting = 0xb8
                self.bus.write_byte(MPL3115A2_ADDRESS, CTRL_REG1, new_setting)
                break

            except IOError:
                logging.error("error: Could not connect to Altimeter.  Retrying.")
                tries++
                sleep(3)

        if(tries >= 5):
            logging.error("error: Could not connect to Altimeter. Max limit of retries reached.")
            raise IOError("Could not connect to the device.")


        # Enable event flags
        self.bus.write_byte(MPL3115A2_ADDRESS, PT_DATA_CFG, OUT_P_DELTA_MSB)

        # Toggel One Shot
        setting = self.bus.read_byte(MPL3115A2_ADDRESS, CTRL_REG1)
        if (setting & 0x02) == 0:
            self.bus.write_byte(MPL3115A2_ADDRESS, CTRL_REG1, (setting | 0x02))



    def read(self):
        raw_data = self.bus.read_block(MPL3115A2_ADDRESS, OUT_P_MSB, 3)
        try:
            return Altimeter.parse_raw_data(raw_data)

        except Exception as e:
            logging.error('error: {}, raw_data: {}'.format(e, raw_data))
            return (-1)



    def read_bar_setting(self):
        setting = self.bus.read_block(MPL3115A2_ADDRESS, BAR_IN_MSB, 2)
        try:
            return (parse_raw_data(setting))*2

    except Exception as e:
        logging.error('error: {}, raw_data: {}'.format(e, raw_data))
        return(-1)



    #Parameter is bar setting/2
    def write_bar_setting(self, input):
        if(input < 0 || input > 131071):
            raise ValueError("Input out of acceptable bounds.")
        else:
            self.bus.write_block(MPL3115A2_ADDRESS, BAR_IN_MSB, int(input))
            setting = read_bar_setting()


    @staticmethod
    def parse_raw_data(raw_data):
        alt_int = 0
        alt_frac = 0
        alt_int_bin = raw_data[0] + raw_data[1] + raw_data[2][0] + raw_data[2][1] + raw_data[2][2] + raw_data[2][3]
        alt_frac_bin = raw_data[2][4] + raw_data[2][5] + raw_data[2][6] + raw_data[2][7]

        alt_frac = int(alt_frac_bin,2)/16

        if(alt_int_bin[0][0] == '1'):
            alt_int = -1*(65536 - int(alt_int_bin, 2))
            alt_frac = -1*alt_frac
        else:
            alt_int = int(alt_int_bin,2)

        alt = alt_int + alt_frac
        return alt
