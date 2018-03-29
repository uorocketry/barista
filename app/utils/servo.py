import os
if os.environ.has_key('ROCKET_PRODUCTION'):
    import RPi.GPIO as GPIO

FREQUENCY = 100 # Hz
MINIMUM_DUTY_CYCLE = FREQUENCY * (float(3383)/32400)
MAXIMUM_DUTY_CYCLE = FREQUENCY * (float(1099)/4500)

class Servo(object):
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, FREQUENCY)
        self.pwm.start((MINIMUM_DUTY_CYCLE+MAXIMUM_DUTY_CYCLE)/2)


    def write(self, position):
        duty_cycle = MINIMUM_DUTY_CYCLE + (float(position)/180)*(MAXIMUM_DUTY_CYCLE-MINIMUM_DUTY_CYCLE)
        self.pwm.ChangeDutyCycle(duty_cycle)
