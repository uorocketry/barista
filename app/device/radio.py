import serial
from time import sleep
import logging
import json

class Radio(object):
    def __init__(self,baud=9600,port='/dev/ttyUSB0'):
        try:
            self.ser = serial.Serial(port,baud,timeout=None)
            logging.info("Radio Initialized")
        except Exception as e:
            logging.error('error:{}'.format(e))

    def write(self, raw_data):
        logging.info(json.dumps(raw_data))
        try:
            return self.ser.write(json.dumps(raw_data)+'\n')
        except Exception as e:
            logging.error('error: {}, data: {}'.format(e, raw_data))

    def read(self):
        try:
            return self.ser.readline()
        except Exception as e:
            logging.error('error: {}'.format(e))
            return "ERROR"

    def sleep(self):
        #TODO: make it sleep
        return

    def wake(self):
        #TODO: make it wake up from sleep
        return
