
import os
from time import sleep
if 'ROCKET_PRODUCTION' in os.environ:
    import RPi.GPIO as GPIO

FREQUENCY = 4000  # Hz


class Buzzer(object):
    def __init__(self, pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, FREQUENCY)
        self.pwm.start(0)

    def buzz(self):
        self.pwm.ChangeDutyCycle(50)
        sleep(0.5)
        self.pwm.ChangeDutyCycle(0)
