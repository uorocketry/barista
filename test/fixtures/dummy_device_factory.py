import time
import random
import logging

class DummyAccelerometer(object):
    def __init__(self):
        self.sleeping = False

    def read(self):
        if self.sleeping:
            return {
                'x': 0.0,
                'y': 0.0,
                'z': 0.0,
                'time':time()
            }
        else:
            return {
                'x': round(random.uniform(-10,10),4),
                'y': round(random.uniform(-10,10),4),
                'z': round(random.uniform(-10,10),4),
                'time': time()
            }

    def sleep(self):
        self.sleeping = True

    def wake(self):
        self.sleeping = False


class DummyGPS(object):
    def read(self):
        return {
            'fix': True,
            'satelites': 8,
            'time (UTC)': '23:35:19',
            'altitude (ASL)': 545.4,
            'latitude (deg)': 48.0,
            'latitude (min)': 7.038,
            'latitude (dir)': 'N',
            'longitude (deg)': 11.0,
            'longitude (min)': 31.0,
            'longitude (dir)': 'E',
            'ground_speed': 11.514
        }


class DummyGyro(object):
    def __init__(self):
        self.sleeping = False

    def read(self):
        if self.sleeping:
            return {
                'pitch': 0.0,
                'roll': 0.0,
                'yaw': 0.0,
                'time':time()
            }
        else:
            return {
                'pitch': round(random.uniform(0,360),4),
                'roll': round(random.uniform(0,360),4),
                'yaw': round(random.uniform(0,360),4),
                'time': time()
            }

    def sleep(self):
        self.sleeping = True

    def wake(self):
        self.sleeping = False


class DummyParachute(object):
    def __init__(self):
        self.logger = logging.getLogger()

    def deploy_stage_one(self):
        self.logger.info('Deployed Stage One')

    def deploy_stage_two(self):
        self.logger.info('Deployed Stage Two')


class DummyBrakes(object):
    def __init__(self):
        self.logger = logging.getLogger()

    def deploy(self, percentage):
        self.logger.info('Deployed Barkes %f%', percentage)


class DummyDeviceFactory(object):
    def __init__(self):
        self.accelerometer = DummyAccelerometer()
        self.gps = DummyGPS()
        self.gyro = DummyGyro()
        self.parachute = DummyParachute()
