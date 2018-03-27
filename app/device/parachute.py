import os
import logging
if os.environ.has_key('ROCKET_PRODUCTION'):
    import RPi.GPIO as GPIO

STAGE_ONE_TRIGGER_PIN = 4 # physical pin 7
STAGE_TWO_TRIGGER_PIN = 17 # physical pin 11

class Parachute(object):
    def __init__(self):
        self.deployed_stage_one = False
        self.deployed_stage_two = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(STAGE_ONE_TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(STAGE_TWO_TRIGGER_PIN, GPIO.OUT)

        GPIO.output(STAGE_ONE_TRIGGER_PIN, GPIO.LOW)
        GPIO.output(STAGE_TWO_TRIGGER_PIN, GPIO.LOW)

    def deploy_stage_one(self):
        if not self.deployed_stage_one:
            self.deployed_stage_one = True
            GPIO.output(STAGE_ONE_TRIGGER_PIN, GPIO.HIGH)
        else:
            raise

    def deploy_stage_two(self):
        if not self.deployed_stage_two and self.deployed_stage_one:
            self.deployed_stage_two = True
            GPIO.output(STAGE_TWO_TRIGGER_PIN, GPIO.HIGH)
        else:
            raise

    # TODO make this an asynchronous callback 2s after deploy
    def cut_power(self):
        GPIO.output(STAGE_ONE_TRIGGER_PIN, GPIO.LOW)
        GPIO.output(STAGE_TWO_TRIGGER_PIN, GPIO.LOW)
