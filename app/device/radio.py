import serial
from time import sleep
import logging
import json

class Radio(object):
    def __init__(self,baud=9600, port='/dev/ttyUSB0'):
        try:
            self.serial = serial.Serial(port,baud,timeout=1)
            logging.info("Radio Initialized")
        except Exception as e:
            logging.error('error: {}'.format(e))

    def transmit(self, acion, data):
        message = json.dumps({ 'action': action, 'data': data })
        try:
            self.serial.write(message + '\n')
            logging.info('Radio transmit message: {}'.format(message))
        except Exception as e:
            logging.error('Radio transmit error: {}, message: {}'.format(e, message))

    def receive(self):
        try:
            message = self.serial.readline()
            if message == '':
                return None
            else:
                logging.info('Radio received message: {}'.format(message))
                return json.loads(message)
        except Exception as e:
            logging.error('error: {}'.format(e))
            return None

    def set_port(port):
        original_port = self.serial.port
        self.serial.close()
        self.serial.port = port
        try:
            self.serial.open()
            if not self.serial.is_open:
                raise
            else:
                logging.info('Radio switch port: {}'.format(port))
        except Exception as e:
            self.serial.port = original_port
            self.serial.open()
            logging.error('Radio reverting to original port: {}'.format(original_port))


    def sleep(self):
        #TODO: make it sleep
        return

    def wake(self):
        #TODO: make it wake up from sleep
        return
