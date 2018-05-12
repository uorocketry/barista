import time
import logging

from app.utils.servo import Servo
from app.utils.exceptions import InvalidArguments

SERVO_PIN = 21 # physical pin 12

class Brakes(object):
    def __init__(self):
        self.percentage = 0
        self.servo = Servo(SERVO_PIN)
        self.servo.write(0)

    def deploy(self, percentage):
        if percentage < 0.0 or percentage > 1.0:
            e = "percentage must be in range (0.0, 1.0)"
            logging.error('Brakes deploy error: {}, percentage: {}'.format(e, percentage))
        else:
            self.percentage = percentage
            self.servo.write(percentage)

    def sweep(self):
        self.deploy(0)

        for i in range(0, 100):
            self.deploy(i/100.0)
            time.sleep(0.03)

        for i in reversed(range(0, 100)):
            self.deploy(i/100.0)
            time.sleep(0.03)
