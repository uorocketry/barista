require 'beaglebone'

class Device::Altim
  include Beaglebone

  P_AT_C = 101325
  temp_cur = 0
  p_cur = = 0

  i2c = I2CDevice.new(:I2C2)
  i2c.write(0x60, [0x26, 0b10000011].pack("C*"))
  i2c.write(0x60, [0x27, 0b00000000]).pack("C*"))

  #Just a test to see if I'm reading/writing correctly
  #Prints out whether or not status is active
  raw = i2c.read(0x60, 9, [0x01].pack("C*"))
  x = raw.unpack("s>*")
  puts x

  def read
    raw = i2c.read(0x60, 9, [0x01].pack("C*"))
    x = raw.unpack("s>*")

    puts x
    alt = (((P_AT_C/p_cur)**(1/5.257) - 1) * (Temp + 273.15))/0.0065
  end

  def write
  end

end

#test
al = Altim.new

al.read()
