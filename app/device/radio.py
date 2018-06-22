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
    ACTION_CONNECTING='connecting'

    VALID_ACTIONS=[ACTION_WAKE, ACTION_SLEEP, ACTION_LAUNCH, ACTION_TEST_BRAKES, ACTION_POSITION_REPORT, ACTION_CONNECTING]

    def __init__(self, port='/dev/ttyS4',baud=9600):
        try:
            self.serial = serial.Serial(port,baud,timeout=1)
            logging.info("Radio Initialized")
        except Exception as e:
            self.serial = None
            logging.error('error: {}'.format(e))

    def transmit(self, action, data=None):
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
                raise Exception('Invalid message')
        except Exception as e:
            logging.error('error: {}'.format(e))
            return { 'action': None, 'data': None }

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

    def connected(self):
        return self.serial != None and self.serial.is_open

    def sleep(self):
        #TODO: make it sleep
        return

    def wake(self):
        #TODO: make it wake up from sleep
        return
