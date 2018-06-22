from app.utils.i2c import I2C
from time import sleep, time
import numpy as np
import logging


ADDRESS = 0x77
ADDR_BYTE = 0xEE


VALID_COMMANDS = {
    'set_axis_directions' :{ 'command':0x74, 'length':1},
    'tare_current_orientation' :{'command':0x60, 'length':0},
    'read_temp_c' :{ 'command':0x2B, 'length':1},
    'read_accel_filtered' :{ 'command':0x27, 'length':3},
    'read_orientation_euler':{'command': 0x01, 'length':3},
}


class IMU(object):
    def __init__(self):
        self.i2c = I2C(1, ADDRESS)
        self.read_length = 0

        self.set_axis_directions_with_tare()

    def set_axis_directions_with_tare(self):
        axis_direction = 0b00000101
        self.send_command('set_axis_directions', axis_direction)
        self.send_command('tare_current_orientation')

    #sample sensor read functions
    def read_temp_c(self):
        self.send_command('read_temp_c')
        temp = self.parse_byte_array(self.read())
        return{
            'temperature':temp[0],
            'time':time()
        }


    def read_orientation_euler(self):
        self.send_command('read_orientation_euler')
        xyz = self.parse_byte_array(self.read())
        return{
            'x':xyz[0],
            'y':xyz[1],
            'z':xyz[2],
            'time':time()
        }


    def read_accel_filtered(self):
        self.send_command('read_accel_filtered')
        xyz = self.parse_byte_array(self.read())
        return{
            'x':xyz[0]*9.81,
            'y':xyz[1]*9.81,
            'z':xyz[2]*9.81,
            'time':time()
        }


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
