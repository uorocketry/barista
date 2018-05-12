from app.utils.i2c import I2C
from time import sleep, time
import numpy as np
import logging


ADDRESS = 0x77
ADDR_BYTE = 0xEE


VALID_COMMANDS = {
    'read_all':{'command' : 0x20, 'length' : 9},
    'read_gyro':{ 'command':0x21, 'length':3},
    'read_accel' :{ 'command':0x22, 'length':3},
    'read_compass' :{ 'command':0x23, 'length':3},
    'read_temp_c' :{ 'command':0x2B, 'length':1},
    'read_temp_f' :{ 'command':0x2C, 'length':3},
    'read_all_filtered' :{ 'command':0x25, 'length':9},
    'read_gyro_filtered' :{ 'command':0x26, 'length':3},
    'read_accel_filtered' :{ 'command':0x27, 'length':3},
    'read_compass_filtered' :{ 'command':0x28, 'length':3},
    'read_linear_accel' :{ 'command':0x29, 'length':3},
    'read_gyro_filtered_rad_s' :{ 'command':0x30, 'length':3},
    'read_accel_filtered_g' :{ 'command': 0x31, 'length':3},
    'read_orientation_euler':{'command': 0x01, 'length':3},
}


class IMU(object):


    def __init__(self):
        self.i2c = I2C(1, ADDRESS)
        self.read_length = 0


    #sample sensor read functions
    def read_temp_c(self):
        self.send_command('read_temp_c')
        return self.parse_byte_array(self.read())


    def read_orientation_euler(self):
        self.send_command('read_orientation_euler')
        return self.parse_byte_array(self.read())


    def read_accel_filtered(self):
        self.send_command('read_accel_filtered')
        return self.parse_byte_array(self.read())


    def send_command(self,command,param=0x00):
        self.i2c.write_byte(ADDR_BYTE, 0x42)
        self.i2c.write_byte(VALID_COMMANDS[command]['command'], param)
        self.read_length = VALID_COMMANDS[command]['length']*4


    def read(self):
        self.i2c.write_byte(ADDR_BYTE, 0x43)
        data = self.i2c.read_block(0x00, self.read_length)
        return data


    def parse_byte_array(self,array):
        a = []
        for i in range(self.read_length/4):
            a.append(array[i*4:(i*4)+4])
        for item in a:
            a[a.index(item)] = float(self.i2c.byte_array_to_float32(item))
        return a
