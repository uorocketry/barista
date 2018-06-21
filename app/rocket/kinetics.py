from threading import Thread
from collections import deque

import numpy as np
import logging

WINDOW_SIZE = 50

class Kinetics(Thread):
    def __init__(self, device_factory):
        self.imu = device_factory.imu
        self.altimeter = device_factory.altimeter
        self.time_series = deque(np.arange(WINDOW_SIZE), maxlen=WINDOW_SIZE)

        self.acceleration_window = TimeWindow3()
        self.velocity_window = TimeWindow3()
        self.position_window = TimeWindow3()

        self.vertical_velocity_window = TimeWindow()
        self.vertical_position_window = TimeWindow()

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

    def vertical_velocity(self):
        return self.vertical_velocity_window.last()

    def vertical_position(self):
        return self.vertical_position_window.last()

    def compute_brakes_percentage(self):
        return 0.0

    def run(self):
        while self.active:
            acceleration = self.imu.read_accel_filtered()
            altitude = self.altimeter.read_altitude()

            self.time_series.append(acceleration['time'])
            self.acceleration_window.append(x=acceleration['x'], y=acceleration['y'], z=acceleration['z'])

            prev_velocity = self.velocity_window.last()
            delta_velocity = self.acceleration_window.integrate_last(self.time_series[-2], self.time_series[-1])

            self.velocity_window.append(
                x=prev_velocity['x'] + delta_velocity['x'],
                y=prev_velocity['y'] + delta_velocity['y'],
                z=prev_velocity['z'] + delta_velocity['z'])

            prev_position = self.position_window.last()
            delta_position = self.velocity_window.integrate_last(self.time_series[-2], self.time_series[-1])
            self.position_window.append(
                x=prev_position['x'] + delta_position['x'],
                y=prev_position['y'] + delta_position['y'],
                z=prev_position['z'] + delta_position['z'])

            logging.debug("Acceleration x: {}, y: {}, z: {}".format(acceleration['x'], acceleration['y'], acceleration['z']))
            velocity = self.velocity()
            logging.debug("Velocity x: {}, y: {}, z: {}".format(velocity['x'], velocity['y'], velocity['z']))
            position = self.position()
            logging.debug("Position x: {}, y: {}, z: {}".format(position['x'], position['y'], position['z']))

            self.vertical_position_window.append(altitude)
            logging.debug("Vertical Position: {}".format(altitude))
            self.vertical_velocity_window.append(
                self.vertical_position_window.derive_last(
                    self.time_series[-2], self.time_series[-1]
                )
            )
            logging.debug("Vertical Velocity: {}".format(self.vertical_position_window.last()))


class TimeWindow(object):
    def __init__(self, size=WINDOW_SIZE):
        self.data = deque(np.zeros(size), maxlen=size)

    def append(self, value):
        self.data.append(value)

    def integrate_last(self, t0, t1):
        return np.trapz(
            [self.data[-2], self.data[-1]],
            [t0, t1]
        )
    def derive_last(self, t0, t1):
        return (self.data[-1] - self.data[-2]) / (t1 - t0)

    def last(self, count=1):
        if count == 1:
            return self.data[-1]
        else:
            return self.x[-1:-1*count]

class TimeWindow3(object):
    def __init__(self, size=WINDOW_SIZE):
        self.x = TimeWindow(size=size)
        self.y = TimeWindow(size=size)
        self.z = TimeWindow(size=size)

    def append(self, **values):
        self.x.append(values['x'])
        self.y.append(values['y'])
        self.z.append(values['z'])

    def integrate_last(self, t0, t1):
        return {
            'x': self.x.integrate_last(t0, t1),
            'y': self.z.integrate_last(t0, t1),
            'z': self.y.integrate_last(t0, t1)
        }

    def last(self, count=1):
        return {'x': self.x.last(count), 'y': self.y.last(count), 'z': self.z.last(count) }
