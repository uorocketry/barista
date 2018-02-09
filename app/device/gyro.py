import smbus

class Gyro:
    'class that represents a gyroscope on a rocket'

    itg_add = (0x68) # ITG3200 address

    ver_id=(0x00) #Used to verify ID
    sam_div=(0x15) #Sample rate divider
    dlp_reg = (0x16) # Select DLPF register
    int_pin=(0x17) #To set configuration of interrupt output pin
    int_pin_stat=(0x1A) #Used to determine status of interrupts
    t_out=(0x1B)	#Temperature
    t_out_l=(0x1C) #
    gx_out=(0x1D) #Gyro x data
    gx_out_l=(0x1E) #
    gy_out=(0x1F) #Gyro y data
    gy_out_l=(0x20) #
    gz_out=(0x21) #Gyro z data
    gz_out_l=(0x22) #
    #Other ones are 2's compliment of one's above.

    pow_reg = (0x3E) # Select Power management register

    data = []

    def __init__ (self):
        self.bus= smbus.SMBus(1)
        self.bus.write_byte_data(self.itg_add, self.pow_reg, 0x01) #PLL with x gyro reference
        self.bus.write_byte_data(self.itg_add, self.dlp_reg, 0x18) #Gyro full scale range +/- 2000 dps 
    def __repr__(self):
        pass

    def __str__(self):
        pass

    def read(self):
    	'does full read of data'
        self.data = self.bus.read_i2c_block_data(self.itg_add, self.gx_out, 6) 
        #READ X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB

    def readable(self):
        x = self.data[0]*256 + self.data[1]
        y = self.data[2]*256 + self.data[3]
        z = self.data[4]*256 + self.data[5]
        if x > 32767 :
            x -= 65536
        if y > 32767 :
            y -= 65536
        if z > 32767 :
            z -= 65536
        return [x,y,z]

    def display_data(self,d = [-1,-1,-1]):
        print "X-Axis of Rotation : "+str(d[0])
        print "Y-Axis of Rotation : "+str(d[1])
        print "Z-Axis of Rotation : "+str(d[2])
		
    def command(self, com1 , com2):
        self.bus.write_byte_data(self.itg_add,com1,com2)

    def sleep(self):
        self.bus.write_byte_data(self.itg_add, pow_reg, 0x40)
