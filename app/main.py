import logging
import os
import time
import json

from transitions import State, Machine
from threading import Thread
from app.rocket.kinetics import Kinetics


class Rocket(object):
    states = [
        State(name='connecting',     on_enter=['enter_state']),
        State(name='ground',         on_enter=['enter_state']),
        State(name='powered',        on_enter=['enter_state']),
        State(name='coast',          on_enter=['enter_state']),
        State(name='descent_drogue', on_enter=['enter_state', 'on_enter_decent_drogue']),
        State(name='descent_main',   on_enter=['enter_state', 'on_enter_descent_main'])
    ]
    transitions = [
        { 'trigger': 'connected', 'source': 'connecting', 'dest': 'ground' },
        { 'trigger': 'launch', 'source': 'ground', 'dest': 'powered' },
        { 'trigger': 'burnout', 'source': 'powered', 'dest': 'coast' },
        { 'trigger': 'deploy_drogue', 'source': 'coast', 'dest': 'descent_drogue' },
        { 'trigger': 'deploy_main', 'source': 'descent_drogue', 'dest': 'descent_main' },
        { 'trigger': 'touchdown', 'source': 'descent_main', 'dest': 'ground' },
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
        self.kinetics.activate()
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
        RADIO_CONNECTION_TIMEOUT = 15
        self.device_factory.radio.transmit(self.device_factory.radio.ACTION_CONNECTING)
        time.sleep(RADIO_CONNECTION_TIMEOUT)
        message = self.device_factory.radio.receive()
        if message['action'] == self.device_factory.radio.ACTION_CONNECTING:
            logging.info('Connected to client')
            self.connected()

    def during_ground(self):
        LAUNCH_ACCELERATION_THRESHOLD = 1.5 # m/s^2
        message = self.device_factory.radio.receive()
        if message['action'] == self.device_factory.radio.ACTION_LAUNCH or self.kinetics.acceleration()['z'] > LAUNCH_ACCELERATION_THRESHOLD:
            self.launch()
        elif message['action'] == self.device_factory.radio.ACTION_SLEEP:
            self.sleep()
        elif message['action'] == self.device_factory.radio.ACTION_TEST_BRAKES:
            self.device_factory.brakes.sweep()

    def during_powered(self):
        BURNOUT_ACCELERATION_THRESHOLD = 0.0
        MOTOR_BURN_TIME = 3.0
        if self.kinetics.acceleration()['z'] < BURNOUT_ACCELERATION_THRESHOLD or time.time() - self.last_state['time'] > MOTOR_BURN_TIME:
            self.burnout()

    def during_coast(self):
        APOGEE_VELOCTY_THRESHOLD = 8 # m/s
        COAST_TIME = 24.5 # s
        self.device_factory.brakes.deploy(self.kinetics.compute_brakes_percentage())
        if self.kinetics.velocity()['z'] <= APOGEE_VELOCTY_THRESHOLD or time.time() - self.last_state['time'] > COAST_TIME:
            self.deploy_drogue()
            self.device_factory.brakes.deploy(0.0)

    def on_enter_decent_drogue(self):
        self.device_factory.parachute.deploy_stage_one()

    def during_descent_drogue(self):
        DECENT_DROGUE_TIME = 100 # sec
        DEPLOY_MAIN_ALTITUDE = 1700 # feet
        if self.device_factory.altimeter.read_altitude() < DEPLOY_MAIN_ALTITUDE or time.time() - self.last_state['time'] >= DECENT_DROGUE_TIME:
            self.deploy_main()

    def on_enter_descent_main(self):
        self.device_factory.parachute.deploy_stage_two()

    def during_descent_main(self):
        TOUCHDOWN_VELOCITY_THRESHOLD = 0.0
        if self.kinetics.velocity()['z'] <= TOUCHDOWN_VELOCITY_THRESHOLD:
            self.touchdown()

    def parse_radio(self):
        radio_receive = self.device_factory.radio.receive()
        if (radio_receive == '') or (radio_receive == None):
            e = "empty string received"
            logging.error('Radio receive error: {}, received: {}'.format(e, radio_receive))
        else:
            self.radio_msg = {
                'action': radio_receive['action'].encode('ascii'),
                'data': radio_receive['data'].encode('ascii')
            }

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
            elif self.state == 'descent_drogue':
                self.during_descent_drogue()
            elif self.state == 'descent_main':
                self.during_descent_main()


if __name__ == '__main__':
    device_factory = None
    if os.environ.has_key('ROCKET_PRODUCTION'):
        from app.rocket.device_factory import DeviceFactory
        device_factory = DeviceFactory()
    else:
        from test.fixtures.dummy_device_factory import DummyDeviceFactory
        device_factory = DummyDeviceFactory()

    rocket = Rocket(device_factory)
    try:
        rocket.activate()
    except KeyboardInterrupt:
        rocket.deactivate()
