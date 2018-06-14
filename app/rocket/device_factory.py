<<<<<<< HEAD
from app.device.altimeter import Altimeter
from app.device.accelerometer import Accelerometer
=======
from app.device.imu import IMU
from app.device.altimeter import Altimeter
>>>>>>> master
from app.device.brakes import Brakes

from app.device.gps import GPS
from app.device.parachute import Parachute
from app.device.radio import Radio


class DeviceFactory(object):
    def __init__(self):
<<<<<<< HEAD
        self.altimeter = Altimeter()
        self.accelerometer = Accelerometer()
=======
        self.imu = IMU()
        self.altimeter = Altimeter()
>>>>>>> master
        self.brakes = Brakes()

        self.gps = GPS()
        self.parachute = Parachute()
        self.radio = Radio()

    def sleep_all(self):
        self.imu.sleep()
        self.radio.sleep()

    def wake_all(self):
        self.imu.wake()
        self.radio.wake()
