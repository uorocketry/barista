import logging
import os
import time
import json

from transitions import State, Machine
from threading import Thread
from app.rocket.kinetics import Kinetics


class Rocket(object):
    states = [
        State(name='connecting', on_enter=['enter_state']),
        State(name='ground',     on_enter=['enter_state']),
        State(name='armed',      on_enter=['enter_state', 'before_arm']),
        State(name='powered',    on_enter=['enter_state']),
        State(name='coast',      on_enter=['enter_state']),
        State(name='descent',    on_enter=['enter_state']),
    ]
    transitions = [
        { 'trigger': 'connected', 'source': 'connecting',             'dest': 'ground' },
        { 'trigger': 'arm',       'source': ['ground', 'connecting'], 'dest': 'armed',   'after': 'notify_armed'     },
        { 'trigger': 'launch',    'source': 'armed',                  'dest': 'powered', 'after': 'notify_launch'    },
        { 'trigger': 'burnout',   'source': 'powered',                'dest': 'coast',   'after': 'notify_burnout'   },
        { 'trigger': 'apogee',    'source': 'coast',                  'dest': 'descent', 'after': 'notify_apogee'    },
        { 'trigger': 'touchdown', 'source': 'descent',                'dest': 'ground',  'after': 'notify_touchdown' },
    ]

    def __init__(self, device_factory, log_level=logging.INFO, log_dir='app/logs'):
        self.state_machine = Machine(
            model=self,
            states=Rocket.states,
            transitions=Rocket.transitions,
            initial='connecting'
        )
        self.last_state = {
            'name': 'ground',
            'time': time.time()
        }
        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d | [%(levelname)s] | %(message)s',
            datefmt='%m/%d/%Y %I:%M:%-S',
            filename='{}/{}.log'.format(log_dir, int(time.time())),
            level=log_level
        )
        logging.info('Initialized Rocket')

        self.kinetics = Kinetics(device_factory)
        self.device_factory = device_factory
        self.active = False

    def activate(self):
        self.active = True
        self.run()

    def deactivate(self):
        logging.info('Shutting down rocket')
        self.kinetics.deactivate()
        self.active = False

    def enter_state(self):
        self.last_state = {
            'name': self.state,
            'time': time.time()
        }
        self.state_data = {}

    def during_connecting(self):
        RADIO_AUTOARM = 1498
        RADIO_CONNECTION_TIMEOUT = 10
        if time.time() - self.last_state['time'] > RADIO_AUTOARM:
            logging.info('Auto arming')
            self.arm()

        self.device_factory.radio.transmit(self.device_factory.radio.ACTION_CONNECTING)
        time.sleep(RADIO_CONNECTION_TIMEOUT)
        message = self.device_factory.radio.receive()
        if message['action'] == self.device_factory.radio.ACTION_CONNECTING:
            logging.info('Connected to client')
            self.connected()

    def during_ground(self):
        message = self.device_factory.radio.receive()
        if message['action'] == self.device_factory.radio.ACTION_TEST_BRAKES:
            self.device_factory.brakes.sweep()
        elif message['action'] == self.device_factory.radio.ACTION_ARM:
            self.arm()

        self.position_report()
        time.sleep(0.5)

    def before_arm(self):
        self.device_factory.altimeter.reset_bar_input()
        self.kinetics.activate()

    def during_armed(self):
        LAUNCH_ACCELERATION_THRESHOLD = 5 # m/s^2
        if self.device_factory.imu.acceleration()['z'] > LAUNCH_ACCELERATION_THRESHOLD:
            self.launch()

    def during_powered(self):
        BURNOUT_ACCELERATION_THRESHOLD = 0.0
        MOTOR_BURN_TIME = 3.0
        if self.kinetics.acceleration()['z'] < BURNOUT_ACCELERATION_THRESHOLD or time.time() - self.last_state['time'] > MOTOR_BURN_TIME:
            self.burnout()
        self.position_report()

    def during_coast(self):
        BRAKE_VELOCTY_THRESHOLD = 250 # m/s
        DESCENT_VELOCITY_THRESHOLD = -4
        if self.kinetics.velocity()['z'] <= BRAKE_VELOCTY_THRESHOLD:
            error = 3048 - self.predicted_apogee(self.device_factory.brakes.percentage)
            new_percentage = self.device_factory.brakes.percentage + 0.001 * error
            if new_percentage > 1.0
                new_percentage = 1.0
            elif new_percentage < 0.0
                new_percentage = 0.0

            self.device_factory.brakes.deploy(new_percentage)
        else:
            self.device_factory.brakes.deploy(0.0)

        if self.kinetics.vertical_velocity() <= DESCENT_VELOCITY_THRESHOLD:
            self.apogee()

    def during_descent(self):
        self.position_report()
        time.sleep(1)

    def notify_armed(self):
        self.device_factory.radio.transmit(
            self.device_factory.radio.ACTION_TRANSITION,
            data= {
                'last_state': self.last_state,
                'event': 'armed',
                'time': time.time()
            }
        )

    def notify_launch(self):
        self.device_factory.radio.transmit(
            self.device_factory.radio.ACTION_TRANSITION,
            data= {
                'last_state': self.last_state,
                'event': 'launch',
                'time': time.time()
            }
        )

    def notify_burnout(self):
        self.device_factory.radio.transmit(
            self.device_factory.radio.ACTION_TRANSITION,
            data= {
                'last_state': self.last_state,
                'event': 'burnout',
                'time': time.time()
            }
        )

    def notify_apogee(self):
        self.device_factory.radio.transmit(
            self.device_factory.radio.ACTION_TRANSITION,
            data= {
                'last_state': self.last_state,
                'event': 'apogee',
                'time': time.time()
            }
        )

    def notify_touchdown(self):
        self.device_factory.radio.transmit(
            self.device_factory.radio.ACTION_TRANSITION,
            data= {
                'last_state': self.last_state,
                'event': 'touchdown',
                'time': time.time(),
            }
        )

    def position_report(self):
        self.device_factory.radio.transmit(
            self.device_factory.radio.ACTION_POSITION_REPORT,
            data={
                'gps': self.device_factory.gps.read(),
                'acceleration': self.device_factory.imu.read_accel_filtered(),
                'velocity': self.kinetics.vertical_velocity(),
                'altitude': self.kinetics.vertical_position(),
        )

    def run(self):
        while self.active:
            if self.state == 'connecting':
                self.during_connecting()
            elif self.state == 'ground':
                self.during_ground()
            elif self.state == 'powered':
                self.during_powered()
            elif self.state == 'coast':
                self.during_coast()
            elif self.state == 'descent':
                self.during_descent()

if __name__ == '__main__':
    from app.rocket.device_factory import DeviceFactory
    device_factory = DeviceFactory()

    rocket = Rocket(device_factory)
    try:
        rocket.activate()
    except KeyboardInterrupt:
        rocket.deactivate()
