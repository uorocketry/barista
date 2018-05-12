import serial
from time import sleep
import logging
import json

class Radio(object):
    ACTION_WAKE='wake'
    ACTION_SLEEP='sleep'
    ACTION_LAUNCH='launch'
    ACTION_TEST_BRAKES='test_brakes'
    ACTION_POSITION_REPORT='position_report'

    VALID_ACTIONS=[ACTION_WAKE, ACTION_SLEEP, ACTION_LAUNCH, ACTION_TEST_BRAKES, ACTION_POSITION_REPORT]

    def __init__(self,baud=9600, port='/dev/ttyUSB0'):
        try:
            self.serial = serial.Serial(port,baud,timeout=1)
            logging.info("Radio Initialized")
        except Exception as e:
            logging.error('error: {}'.format(e))

    def transmit(self, action, data):
        message = json.dumps({ 'action': action, 'data': data })
        try:
            encoded_message = bytearray(message, 'ascii')
            self.serial.write(encoded_message + b'\n')
            logging.info('Radio transmit message: {}'.format(message))
        except Exception as e:
            logging.error('Radio transmit error: {}, message: {}'.format(e, message))

    def receive(self):
        try:
            message = self.serial.readline()
            logging.info('Radio received message: {}'.format(message))
            message = json.loads(message) # unicode string
            if message['action'] in Radio.VALID_ACTIONS:
                return message
            else:
                raise Expection('Invalid message')
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
