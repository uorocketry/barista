from app.device.imu import IMU
from app.device.altimeter import Altimeter
from app.device.brakes import Brakes

from app.device.gps import GPS
from app.device.parachute import Parachute
from app.device.radio import Radio


class DeviceFactory(object):
    def __init__(self):
        self.imu = IMU()
        self.altimeter = Altimeter()
        self.brakes = Brakes()

        self.gps = GPS()
        self.radio = Radio()

    def sleep_all(self):
        self.imu.sleep()
        self.radio.sleep()

    def wake_all(self):
        self.imu.wake()
        self.radio.wake()
