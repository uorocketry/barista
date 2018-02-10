from smbus import SMBus
import numpy as np

class I2C(object):
    def __init__(self, bus_number, device_address):
        self.smbus = SMBus(bus_number)
        self.device_address =  device_address

    def set_bit(self,register, index):
        read_value = self.smbus.read_byte_data(self.device_address, register)
        eight_bit_read_value = list(format(read_value, '08b'))
        eight_bit_read_value[index*(-1)-1] = '1'
        string = bytearray("".join(eight_bit_read_value))

        self.smbus.write_byte_data(self.device_address,register, int(string))


    def clear_bit(self,register, index):
        read_value = self.smbus.read_byte_data(self.device_address, register)
        eight_bit_read_value = list(format(read_value, '08b'))
        eight_bit_read_value[index*(-1)-1] = '0'
        string = bytearray("".join(eight_bit_read_value))

        self.smbus.write_byte_data(self.device_address,register, int(string))


    def read_bit(self,register, index):
        value = self.smbus.read_byte_data(device_address, register)
        eight_bit = format(value, '08b')
        return eight_bit[index*(-1)-1]


    def write_byte(self,register, value):
        self.smbus.write_byte_data(self.device_address,register, int(value))


    def read_byte(self, register):
        return self.smbus.read_byte_data(self.device_address,register)


    def read_block(self,register, number_to_read):
        return self.smbus.read_i2c_block_data(self.device_address, register, number_to_read)
