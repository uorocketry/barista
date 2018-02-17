# Replace libraries by fake ones
import sys
import fake_rpi

sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)


from smbus import SMBus
import numpy as np


class I2C(object):
    def __init__(self, bus_number, device_address):
        self.smbus = SMBus(bus_number)
        self.device_address =  device_address


    def set_bit(self,register, index):
        read_value = np.uint8(self.smbus.read_byte_data(self.device_address, register))
        bit_array = np.unpackbits(read_value)
        bit_array[index*-1-1] = 1
        self.smbus.write_byte_data(self.device_address,register, np.packbits(bit_array))


    def clear_bit(self,register, index):
        read_value = np.uint8(self.smbus.read_byte_data(self.device_address, register))
        bit_array = np.unpackbits(read_value)
        bit_array[index*-1-1] = 0
        self.smbus.write_byte_data(self.device_address,register, np.packbits(bit_array))


    def read_bit(self,register, index):
        value = self.smbus.read_byte_data(device_address, register)
        eight_bit = format(value, '08b')
        return eight_bit[index*(-1)-1]


    def write_byte(self,register, value):
        self.smbus.write_byte_data(self.device_address,register, int(value))


    def read_byte(self, register):
        return self.smbus.read_byte_data(self.device_address,register)


    def read_block(self, register, number_to_read):
        return self.smbus.read_i2c_block_data(self.device_address, register, number_to_read)

    def write_block(self, register, data_to_read):
        return self.smbus.write_i2c_block_data(self.device_address, register, data_to_read)
