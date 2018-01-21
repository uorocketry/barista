<<<<<<< HEAD
<<<<<<< HEAD
=======
from time import sleep
from smbus2 import SMBus
from math import log1p
from math import pow 
=======
from smbus import SMBus
from math  import log1p
>>>>>>> 101a9c9... Barometric setting function and updated test

#special char
deg = u'\N{DEGREE SIGN}'
>>>>>>> 54e7821... Big changes to alt

from smbus2 import SMBus
class Altimeter (object):

    MPL3115A2_ADDRESS = 0x60

    #REGISTERS

<<<<<<< HEAD
    STATUS = (0x00)
    OUT_P_MSB = (0x01)
    OUT_P_DELTA_CSB = (0x08)
    OUT_P_DELTA_MSB = (0X07)
    OUT_T_MSB = (0x04)
    WHOAMI = (0x0C)
    CTRL_REG1 = (0x26)
    PT_DATA_CFG = (0x13)
<<<<<<< HEAD


    def __init__(self):
        #
        bus = SMBus(1)

=======
    BAR_IN_MSB = (0x14)
=======
    STATUS = 0x00
    OUT_P_MSB = 0x01
    OUT_P_DELTA_CSB = 0x08
    OUT_P_DELTA_MSB = 0X07
    OUT_T_MSB = 0x04
    WHOAMI = 0x0C
    CTRL_REG1 = 0x26
    PT_DATA_CFG = 0x13
    BAR_IN_MSB = 0x14
>>>>>>> 27133ae... wip

    bus = SMBus(1)
    @staticmethod
    def __init__(self):
>>>>>>> 101a9c9... Barometric setting function and updated test
        #Check if device is connected
        #whois = bus.read_byte_data(self.MPL3115A2_ADDRESS, self.WHOAMI)
        #if(id!=0xc4):
        #    print("Device not connected")
        #    exit(1)

        #Set oversample rate to 128
<<<<<<< HEAD
<<<<<<< HEAD
        current_setting = bus.read_byte_data(self.MPL3115A2_ADDRESS, self.CTRL_REG1)
        new_setting = current_setting | 0x38
        bus.write_byte_data(self.MPL3115A2_ADDRESS, self.CTRL_REG1, new_setting)
=======
        current_setting = self.bus.read_byte_data(self.MPL3115A2_ADDRESS, self.CTRL_REG1)
        new_setting = 0xb8
        self.bus.write_byte_data(self.MPL3115A2_ADDRESS, self.CTRL_REG1, new_setting)
>>>>>>> f79a971... temp commit
=======
        current_setting = self.bus.read_byte_data(self.MPL3115A2_ADDRESS, self.CTRL_REG1)
        #new_setting = 0xb8
        self.bus.write_byte_data(self.MPL3115A2_ADDRESS, self.CTRL_REG1, 0xb8)
>>>>>>> 54e7821... Big changes to alt

        # Enable event flags
        bus.write_byte_data(self.MPL3115A2_ADDRESS, self.PT_DATA_CFG, self.OUT_P_DELTA_MSB)

        # Toggel One Shot
        setting = bus.read_byte_data(self.MPL3115A2_ADDRESS, self.CTRL_REG1)
        if (setting & 0x02) == 0:
<<<<<<< HEAD
            bus.write_byte_data(self.MPL3115A2_ADDRESS, self.CTRL_REG1, (setting | 0x02))
=======
            self.bus.write_byte_data(self.MPL3115A2_ADDRESS, self.CTRL_REG1, (setting | 0x02))
<<<<<<< HEAD

    def temp(self):
=======
    @staticmethod
    def read_temperature(self):
        #print("Waiting for data")
        status = self.bus.read_byte_data(self.MPL3115A2_ADDRESS, self.STATUS)
        while(status & self.OUT_P_DELTA_CSB)==0:
            #print bin(status)
            status = self.bus.read_byte_data(self.MPL3115A2_ADDRESS, self.STATUS)
            time.sleep(0.5)

>>>>>>> 27133ae... wip
        #Reading sensor data
        t_data = self.bus.read_i2c_block_data(self.MPL3115A2_ADDRESS, self.OUT_T_MSB, 2)

        t_msb = t_data[0]
        t_lsb = t_data[1]

        #Temperature in Kelvin
        temp = t_msb + (t_lsb >> 4)/16.0 + 273.15
>>>>>>> 54e7821... Big changes to alt

<<<<<<< HEAD
    def altitude():
        #print("Waiting for data")
<<<<<<< HEAD
        status = bus.read_byte_data(self.MPL3115A2_ADDRESS, self.STATUS)
        while(status & OUT_P_DELTA_MSB_CSB)==0:
            #print bin(status)
            status = bus.read_byte_data(self.MPL3115A2_ADDRESS, self.STATUS)
            time.sleep(0.5)

        #print("Reading sensor data...")
        p_data = bus.read_i2c_block_data(self.MPL3115A2_ADDRESS, self.OUT_P_MSB, 3)
        t_data = bus.read_i2c_block_data(self.MPL3115A2_ADDRESS, self.OUT_T_MSB, 2)
        status = bus.read_byte_data(self.MPL3115A2_ADDRESS, self.STATUS)
        #print "Status: " + bin(status)
=======
        return temp
    @staticmethod
    def read_altitude(self):
        a_data = self.bus.read_i2c_block_data(self.MPL3115A2_ADDRESS, self.OUT_P_MSB, 3)
>>>>>>> 254c232... Altimeter code now reads directly from device

        alt_int_bin = a_data[0] + a_data[1] + a_data[2][0] + a_data[2][1]
        alt_frac_bin = a_data[2][2] + a_data[2][3]

<<<<<<< HEAD
        #t_msb = t_data[0]
        #t_lsb = t_data[1]

=======
        #status = self.bus.read_byte_data(self.MPL3115A2_ADDRESS, self.STATUS)
        #while(status & self.OUT_P_DELTA_CSB)==0:
        #    status = self.bus.read_byte_data(self.MPL3115A2_ADDRESS, self.STATUS)
        #    sleep(0.5)
        #Reading sensor data
        p_data = self.bus.read_i2c_block_data(self.MPL3115A2_ADDRESS, self.OUT_P_MSB, 3)
       
        p_msb = p_data[0]
        p_csb = p_data[1]
        p_lsb = p_data[2]
        print(p_msb)
        print(p_csb)
        print(p_lsb)
>>>>>>> 54e7821... Big changes to alt
        #Pressure integer part
        #pressure = (p_msb << 10) | (p_csb << 2) | (p_lsb >> 6)
        #Pressure add fraction part
       # pressure += ((p_lsb & 0x30) >> 4)/4.0

<<<<<<< HEAD
        celsius = t_msb + (t_lsb >> 4)/16.0
        fahrenheit = (celsius * 9)/5 + 32

        print "Pressure and Temperature at "+time.strftime('%m/%d/%Y %H:%M:%S%z')
        print str(pressure+p_decimal)+" Pa"
        print str(celsius)+deg+"C"
        print str(fahrenheit)+deg+"F"
=======
       # return pressure

    def altitude(self):
        #temp = self.temp()
        #temp = 266
        #pressure = self.pressure()
        #altitude = ((pow((101930/pressure), (1/5.257)) -1)*temp)/0.0065
=======
        alt_int = 262144-int(alt_bin,2) + 1
        alt_frac = (3-int(alt_frac_bin,2) +1)/4.0
        #Pressure integer part
        altitude = alt_int + alt_frac

>>>>>>> 254c232... Altimeter code now reads directly from device
        return altitude
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 54e7821... Big changes to alt
=======

=======
    @staticmethod
>>>>>>> 27133ae... wip
    def read_bar_setting(self):
        setting = self.bus.read_i2c_block_data(self.MPL3115A2_ADDRESS, self.BAR_IN_MSB, 2)
        print("Barometric setting: \t " + str(setting))
    @staticmethod
    def write_bar_setting(self, input):
        #Will write 16 bits, starting at BAR_IN_MSB(8 bit) and over into
        #BAR_IN_LSB (not defined in this program)
        self.bus.write_i2c_block_data(self.MPL3115A2_ADDRESS, self.BAR_IN_MSB, input)
        #TODO: Add check and logging
        print("Barometric setting configured successfully")
>>>>>>> 101a9c9... Barometric setting function and updated test
