import logging
import pandas as pd
from app.main import Rocket
from test.helpers.dummy_device_factory import DummyGPS, DummyBrakes, DummyParachute, DummyRadio
from gyro import SandboxGyro
from accelerometer import SandboxAccelerometer
from altimeter import SandboxAltimeter
from app.rocket.kinetics import Kinetics,TimeWindow
from time import time

class SandboxDeviceFactory(object):
    def __init__(self, simulation_data):
        self.accelerometer = SandboxAccelerometer(self.filter_dataframe(simulation_data, 'acceleration'))
        self.gyro = SandboxGyro(self.filter_dataframe(simulation_data,'rate (deg/s)'))
        self.altimeter = SandboxAltimeter(self.filter_dataframe(simulation_data,'Altitude'))
        self.radio = DummyRadio()
        self.gps = DummyGPS()
        self.parachute = DummyParachute()

    def filter_dataframe(self, dataframe, columns):
        return pd.concat([dataframe.filter(items=['# Time (s)']), dataframe.filter(like=columns)],axis=1)


class Sandbox(object):
    def __init__(self, source_file='test/helpers/sandbox/simulation.csv'):
        self.simulation_data = pd.read_csv(source_file)
        self.device_factory = SandboxDeviceFactory(self.simulation_data)
        self.rocket = Rocket(self.device_factory)
        self.active = False
        self.launch_time = None

    def start(self):
        print('Starting sandbox')
        self.active = True
        self.rocket.activate()

    def launch(self):
        self.launch_time = time()
        self.rocket.device_factory.accelerometer.launch(self.launch_time)
        self.rocket.device_factory.gyro.launch(self.launch_time)
        self.rocket.device_factory.altimeter.launch(self.launch_time)

    def stop(self):
        self.active = False
        self.rocket.deactivate()

    def reset(self):
        if self.active:
            logging.warn('Sandbox still running')
        else:
            logging.info('Reseting sandbox')
            self.device_factory.accelerometer.reset()
            self.device_factory.altimeter.reset()
            self.device_factory.gyro.reset()

    def send_comms(self, action=None, data=None):
        self.rocket.device_factory.radio.mock_message(action,data)

if __name__ == '__main__':
    sandbox = Sandbox()
    print('''
     .oooooo..o                             .o8   .o8
    d8P'    `Y8                            "888  "888
    Y88bo.       .oooo.   ooo. .oo.    .oooo888   888oooo.   .ooooo.  oooo    ooo
     `"Y8888o.  `P  )88b  `888P"Y88b  d88' `888   d88' `88b d88' `88b  `88b..8P'
         `"Y88b  .oP"888   888   888  888   888   888   888 888   888    Y888'
    oo     .d8P d8(  888   888   888  888   888   888   888 888   888  .o8"'88b
    8""88888P'  `Y888""8o o888o o888o `Y8bod88P"  `Y8bod8P' `Y8bod8P' o88'   888o
    ''')

    while True:
        command = raw_input('>>>')
        if command == 'help':
            print('''
            help            = prints this stuff
            comms <message> = sends a message over comms channel
            start           = starts a simulation
            launch          = sends ignition signal to rocket
            stop            = stops a simulation
            reset           = resets the simulation
            ''')
        elif command.startswith('comms'):
            args = command.split("\"")
            sandbox.send_comms(args[1], args[3])
        elif command == 'start':
            sandbox.start()
        elif command == 'launch':
            sandbox.launch()
        elif command == 'stop':
            sandbox.stop()
        elif command == 'reset':
            sandbox.reset()
        
