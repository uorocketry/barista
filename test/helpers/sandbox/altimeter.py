from time import time
import logging

class SandboxAltimeter(object):
    def __init__(self, altitude_data):
        self.sleeping = False
        self.launch_time = None
        self.launched = False
        self.altitude_data = altitude_data

    def read(self):
        if self.sleeping:
            return{
                'altitude':0.0,
                'time':time()
            }
        elif self.launched:
            sample_time = time()
            simulation_time = sample_time - self.launch_time
            try:
                return {
                    'altitude':self.noise(self.altitude_data.loc[self.altitude_data['# Time (s)'] >= simulation_time].iloc[0].filter(like='Altitude').values[0]),
                    'time': sample_time
                }
            except Exception as e:
                return{
                    'altitude':self.noise(1294),
                    'time': time()
                }

        else:
            return {
                'altitude': self.noise(1294),
                'time': time()
            }

    def sleep(self):
        self.sleeping = True

    def wake(self):
        self.sleeping = False

    def launch(self,start_time):
        self.launched = True
        self.launch_time = start_time

    def reset(self):
        self.launched = False
        self.wake()
        self.launch_time = None

    def noise(self, data):
        return data
