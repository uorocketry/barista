'''

modified from : https://pypi.python.org/pypi/fake-rpi
should replace: /usr/local/lib/python2.7/dist-packages/fake_rpi/smbus/smbus.py

'''

from fake_rpi.wrappers import printf
from random import randint
from fake_rpi.Base import Base

# randint(0,1024)

data = {}

class SMBus(Base):

	@printf
	def __init__(self, bus=None, force=False):

		Base.__init__(self, self.__class__)

	@printf
	def write_byte_data(self, i2c_addr, register, value):
		pass

	@printf
	def write_byte(self, i2c_addr, register, value):                  # changed
		# pass
        data.update(register:value)

	@printf
	def read_byte_data(self, i2c_addr, register):
		return randint(0, 2**8)

	@printf
	def read_byte(self, i2c_addr, register):                         # changed
        if not bool(data): # bool of data = {} is false
            return data[register]
        else:
            return randint(0, 2**8)

	@printf
	def read_word_data(self, i2c_addr, register):
		return [randint(0, 2**8)]*2

	@printf
	def write_word_data(self, i2c_addr, register, value):
		pass

	@printf
	def read_i2c_block_data(self, i2c_addr, register, length):      # changed
        if not bool(data): # bool of data = {} is false
            read_data = []
            i = 0
            for i < length:
                read_data.append(data[register])
                i += 1
                register += 1
            return read_data
        else:
		    return [randint(0, 2**8)]*length

	@printf
	def write_i2c_block_data(self, i2c_addr, register, data):      # changed
		# pass
        i = 0
        for i < len(data):
            value = data[i]
            data.update(register:value)
            i += 1
            register += 1

	@printf
	def open(self, bus):
		pass

	@printf
	def close(self):
		pass
