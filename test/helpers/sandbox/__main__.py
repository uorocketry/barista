import logging
import pandas as pd
from app.main import Rocket
from test.helpers.dummy_device_factory import DummyGPS, DummyBrakes, DummyParachute
from gyro import SandboxGyro
from accelerometer import SandboxAccelerometer
from altimeter import SandboxAltimeter


class SandboxDeviceFactory(object):


    def __init__(self, simulation_data):
        self.accelerometer = SandboxAccelerometer(self.filter_dataframe(simulation_data, 'acceleration'))
        self.gyro = SandboxGyro(self.filter_dataframe(simulation_data,'rate (°/s)'))
        self.altimeter = SandboxAltimeter(self.filter_dataframe(simulation_data,'Altitude'))
        self.gps = DummyGPS()
        self.parachute = DummyParachute()


    def filter_dataframe(self,dataframe,columns):
        return pd.concat([dataframe.filter(items=['# Time (s)']), dataframe.filter(like=columns)],axis=1)


class Sandbox(object):
    def __init__(self, source_file='test/helpers/sandbox/simulation.csv'):
        self.simulation_data = pd.read_csv(source_file)
        self.device_factory = SandboxDeviceFactory(self.simulation_data)
        self.rocket = Rocket(self.device_factory)
        self.running = False
        self.launch_time = None


    def start(self):
        print('Starting sandbox')
        self.running = True
        rocket.start()


    def ignition(self):
        print('Engine ignition')
        self.launch_time = time()
        self.device_factory.accelerometer.launch(self.launch_time)
        self.device_factory.gyro.launch(self.launch_time)
        self.device_factory.altimeter.launch(self.launch_time)


    def stop(self):
        print('Stopping sandbox')
        self.running = False
        rocket.stop()


    def reset(self):
        if self.running:
            logging.warn('Sandbox still running')
        else:
            logging.info('Reseting sandbox')
            self.device_factory.accelerometer.reset()
            self.device_factory.gyro.reset()


    def send_comms(self, message):
        # TODO when Xbee implemented create a dummy class
        pass





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
        command = input('>>>')
        if command == 'help':
            print('''
            help            = prints this stuff
            comms <message> = sends a message over comms channel
            start           = starts a simulation
            ignition        = sends ignition signal to rocket
            stop            = stops a simulation
            reset           = resets the simulation
            ''')
        elif command.startswith('comms'):
            pass
        elif command == 'start':
            sandbox.start()
        elif command == 'ingition':
            sandbox.ignition()
        elif command == 'stop':
            sandbox.stop()
        elif command == 'reset':
            sandbox.reset()
