from threading import Thread
from collections import deque

import numpy as np
import logging

WINDOW_SIZE = 50

class Kinetics(Thread):
    def __init__(self, device_factory):
        self.accelerometer = device_factory.accelerometer

        self.time_series = deque(np.arange(WINDOW_SIZE), maxlen=WINDOW_SIZE)

        self.acceleration_window = TimeWindow()
        self.velocity_window = TimeWindow()
        self.position_window = TimeWindow()
        self.active = False

    def activate(self):
        if not self.active:
            Thread.__init__(self)
            self.active = True
            self.start()
            if not self.is_alive():
                raise Exception('Failed to activate kinetics model')

    def deactivate(self):
        if self.active:
            self.active = False
            self.join(timeout=1)
            if self.is_alive():
                raise Exception('Failed to deactivate Kinetics Model')

    def predicted_apogee(self):
        return 0

    def acceleration(self):
        return self.acceleration_window.last()

    def velocity(self):
        return self.velocity_window.last()

    def position(self):
        return self.position_window.last()

    def compute_brake_percentage(self):
        return 1.0

    def run(self):
        while self.active:
            measurement = self.accelerometer.read()
            self.time_series.append(measurement['time'])
            self.acceleration_window.append(x=measurement['x'], y=measurement['y'], z=measurement['z'])

            prev_velocity = self.velocity_window.last()
            delta_velocity = self.acceleration_window.integrate_last(self.time_series[-2], self.time_series[-1])
            self.velocity_window.append(
                x=prev_velocity['x'] + delta_velocity[0],
                y=prev_velocity['y'] + delta_velocity[1],
                z=prev_velocity['z'] + delta_velocity[2])


            prev_position = self.position_window.last()
            delta_position = self.velocity_window.integrate_last(self.time_series[-2], self.time_series[-1])
            self.position_window.append(
                x=prev_position['x'] + delta_position[0],
                y=prev_position['y'] + delta_position[1],
                z=prev_position['z'] + delta_position[2])


class TimeWindow(object):
    def __init__(self, size=WINDOW_SIZE):
        self.x = deque(np.zeros(size), maxlen=size)
        self.y = deque(np.zeros(size), maxlen=size)
        self.z = deque(np.zeros(size), maxlen=size)

    def append(self, **values):
        self.x.append(values['x'])
        self.y.append(values['y'])
        self.y.append(values['z'])

    def integrate_last(self, t0, t1):
        return np.trapz(
            [[self.x[-2], self.x[-1]],
             [self.y[-2], self.y[-1]],
             [self.z[-2], self.z[-1]]],
            [t0, t1])

    def last(self, count=1):
        if count == 1:
            return {'x': self.x[-1], 'y': self.y[-1], 'z': self.z[-1] }
        else:
            return {'x': self.x[-1:-1*count], 'y': self.y[-1:-1*count], 'z': self.z[-1:-1*count] }
