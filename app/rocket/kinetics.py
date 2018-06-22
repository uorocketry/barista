from threading import Thread
from collections import deque

import numpy as np
import logging
import time

WINDOW_SIZE = 50

class Kinetics(Thread):
    def __init__(self, device_factory):
        self.altimeter = device_factory.altimeter
        self.time_series = deque(np.arange(WINDOW_SIZE), maxlen=WINDOW_SIZE)

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

    def vertical_velocity(self):
        return self.vertical_velocity_window.last()

    def vertical_position(self):
        return self.vertical_position_window.last()

    def compute_brakes_percentage(self):
        return 0.0

    def run(self):
        while self.active:
            self.time_series.append(time.time())

            altitude = self.altimeter.read_altitude()

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
