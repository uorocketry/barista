from app.device.accelerometer import Accelerometer
from app.device.altimeter import Altimeter
from app.device.brakes import Brakes

from app.device.gps import GPS
from app.device.gyro import Gyro
from app.device.parachute import Parachute
from app.device.radio import Radio


class DeviceFactory(object):
    def __init__(self):
        self.accelerometer = Accelerometer()
        self.altimeter = Altimeter()
        self.brakes = Brakes()

        self.gps = GPS()
        self.gyro = Gyro()
        self.parachute = Parachute()
        self.radio = Radio()

    def sleep_all(self):
        self.accelerometer.sleep()
        self.accelerometer.sleep()
        self.gyro.sleep()
        self.radio.sleep()

    def wake_all(self):
        self.accelerometer.wake()
        self.accelerometer.wake()
        self.gyro.wake()
        self.radio.wake()
