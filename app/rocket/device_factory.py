from app.device.altimeter import Altimeter
from app.device.accelerometer import Accelerometer
from app.device.brakes import Brakes
from app.device.gps import GPS
from app.device.gyro import Gyro
from app.device.parachute import Parachute

class DeviceFactory(object):
    def __init__(self):
        self.altimeter = Altimeter()
        self.accelerometer = Accelerometer()
        self.brakes = Brakes()
        self.gps = GPS()
        self.gyro = Gyro()
        self.parachute = Parachute()
