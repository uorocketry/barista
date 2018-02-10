from app.utils.i2c import I2C

class Altimeter (object):

    MPL3115A2_ADDRESS = 0x60

    #REGISTERS

    STATUS = 0x00
    OUT_P_MSB = 0x01
    OUT_P_DELTA_CSB = 0x08
    OUT_P_DELTA_MSB = 0X07
    OUT_T_MSB = 0x04
    WHOAMI = 0x0C
    CTRL_REG1 = 0x26
    PT_DATA_CFG = 0x13
    BAR_IN_MSB = 0x14

    bus = I2C(1, MPL3115A2_ADDRESS)

    def __init__(self):

        #Check if device is connected
        #whois = bus.read_byte_data(self.MPL3115A2_ADDRESS, self.WHOAMI)
        #if(id!=0xc4):
        #    print("Device not connected")
        #    exit(1)

        #Set oversample rate to 128
        current_setting = self.bus.read_byte(self.MPL3115A2_ADDRESS, self.CTRL_REG1)
        new_setting = 0xb8
        self.bus.write_byte(self.MPL3115A2_ADDRESS, self.CTRL_REG1, new_setting)

        # Enable event flags
        self.bus.write_byte(self.MPL3115A2_ADDRESS, self.PT_DATA_CFG, self.OUT_P_DELTA_MSB)

        # Toggel One Shot
        setting = self.bus.read_byte(self.MPL3115A2_ADDRESS, self.CTRL_REG1)
        if (setting & 0x02) == 0:
            self.bus.write_byte(self.MPL3115A2_ADDRESS, self.CTRL_REG1, (setting | 0x02))

    # @staticmethod
    # def read_temperature(self):
    #     #print("Waiting for data")
    #     status = self.bus.read_byte_data(self.MPL3115A2_ADDRESS, self.STATUS)
    #     while(status & self.OUT_P_DELTA_CSB)==0:
    #         #print bin(status)
    #         status = self.bus.read_byte_data(self.MPL3115A2_ADDRESS, self.STATUS)
    #         time.sleep(0.5)
    #
    #     #Reading sensor data
    #     t_data = self.bus.read_i2c_block_data(self.MPL3115A2_ADDRESS, self.OUT_T_MSB, 2)
    #
    #     t_msb = t_data[0]
    #     t_lsb = t_data[1]
    #
    #     #Temperature in Kelvin
    #     temp = t_msb + (t_lsb >> 4)/16.0 + 273.15
    #
    #     return temp

    #Reads the altimeter's altitude register
    #Returns byte array
    def read(self):
        raw_data = self.bus.read_block(self.MPL3115A2_ADDRESS, self.OUT_P_MSB, 3)
        return Altimeter.parse_raw_data(raw_data)



    #Reads the altimeter's Barometic Input register
    #Returns byte array
    #Whole function here for testing
    def read_bar_setting(self):
        setting = self.bus.read_block(self.MPL3115A2_ADDRESS, self.BAR_IN_MSB, 2)
        print("Current \t" + str(setting))
        return setting


    #Writes to the altimeter's Barometic Input register
    #Takes number as input
    #Returns boolean, will eventually throw exception
    def write_bar_setting(self, input):
        hex_input = hex(input)

        self.bus.write_block(self.MPL3115A2_ADDRESS, self.BAR_IN_MSB, input)
        setting = self.read_bar_setting()
        print("New: \t" + str(setting))
        return (setting == input)



    #Parse altitude data and return as number
    @staticmethod
    def parse_raw_data(raw_data):
        alt_int_bin = raw_data[0] + raw_data[1] + raw_data[2][0] + raw_data[2][1]
        alt_frac_bin = raw_data[2][2] + raw_data[2][3]

        alt_int = 262144-int(alt_bin,2) + 1
        alt_frac = (3-int(alt_frac_bin,2) +1)/4.0
        #Pressure integer part
        altitude = alt_int + alt_frac
        return altitude
