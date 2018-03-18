import os
if os.environ.has_key('ROCKET_PRODUCTION'):
    import RPi.GPIO as GPIO

STAGE_ONE_TRIGGER_PIN = 4 # physical pin 7
STAGE_TWO_TRIGGER_PIN = 17 # physical pin 11

class Parachute(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(STAGE_ONE_TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(STAGE_TWO_TRIGGER_PIN, GPIO.OUT)

        GPIO.output(STAGE_ONE_TRIGGER_PIN, GPIO.LOW)
        GPIO.output(STAGE_TWO_TRIGGER_PIN, GPIO.LOW)


    def deploy_stage_one(self):
        GPIO.output(STAGE_ONE_TRIGGER_PIN, GPIO.HIGH)


    def deploy_stage_two(self):
        GPIO.output(STAGE_TWO_TRIGGER_PIN, GPIO.HIGH)

    # TODO make this an asynchronous callback after deploy
    def cut_power(self):
        GPIO.output(STAGE_ONE_TRIGGER_PIN, GPIO.LOW)
        GPIO.output(STAGE_TWO_TRIGGER_PIN, GPIO.LOW)
