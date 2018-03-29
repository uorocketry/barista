import os
if os.environ.has_key('ROCKET_PRODUCTION'):
    import RPi.GPIO as GPIO

FREQUENCY = 100 # Hz
MINIMUM_DUTY_CYCLE = 8.5576
MAXIMUM_DUTY_CYCLE = 19.606

class Servo(object):
    def __init__(self, pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, FREQUENCY)
        self.pwm.start((MINIMUM_DUTY_CYCLE+MAXIMUM_DUTY_CYCLE)/2.0)


    def write(self, percentage):
        duty_cycle = MAXIMUM_DUTY_CYCLE - percentage * (MAXIMUM_DUTY_CYCLE - MINIMUM_DUTY_CYCLE)
        self.pwm.ChangeDutyCycle(duty_cycle)
