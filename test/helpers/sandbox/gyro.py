from time import time


class SandboxGyro(object):
    def __init__(self, gyro_data):
        self.sleeping = False
        self.launch_time = None
        self.launched = False
        self.gyro_data = gyro_data

    def read(self):
        if self.sleeping:
            return {
                'pitch': 0.0,
                'roll': 0.0,
                'yaw': 0.0,
                'time': time()
            }
        elif self.launched:
            sample_time = time()
            simulation_time = sample_time - self.launch_time
            return {
                'pitch': self.noise(self.gyro_data.loc[self.gyro_data['# Time (s)'] >= simulation_time].iloc[0].filter(like='Pitch').values[0]),
                'roll': self.noise(self.gyro_data.loc[self.gyro_data['# Time (s)'] >= simulation_time].iloc[0].filter(like='Roll').values[0]),
                'yaw': self.noise(self.gyro_data.loc[self.gyro_data['# Time (s)'] >= simulation_time].iloc[0].filter(like='Yaw').values[0]),
                'time': time()
            }
        else:
            return {
                'pitch': self.noise(0.0),
                'roll': self.noise(0.0),
                'yaw': self.noise(0.0),
                'time':time()
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

    def noise(self, value):
        return value
