import sys
import logging
from app.device.radio import Radio

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter



class Client(object):
    def __init__(self, radio_port):
        self.completer = WordCompleter(Radio.VALID_ACTIONS, ignore_case=True)
        self.history = InMemoryHistory()
        self.radio = Radio(radio_port)
        self.connected = False
        if self.radio.connected():
            self.connect_with_rocket()
        else:
            print('Could not connect with radio')

    def connect_with_rocket(self):
        print('Estabilishing connection with rocket...')
        while not self.connected:
            message = self.radio.receive()
            if message['action'] is Radio.ACTION_CONNECTING:
                print('Connected to rocket')
                radio.transmit(Radio.ACTION_CONNECTING, True)
                self.connected = True

    def run(self):
        message = self.radio.receive()
        if message['action'] != None:
            print(message)

        action = prompt("> ", history=self.history, completer=self.completer)
        if action in Radio.VALID_ACTIONS:
            self.radio.transmit(action, [])
        elif action == 'help':
            print('The following are availible radio actions: {}'.format(Radio.VALID_ACTIONS))
        else:
            print('INVALID ACTION')

client = Client(sys.argv[1])
while client.connected:
    client.run()
