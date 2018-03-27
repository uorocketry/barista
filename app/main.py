import logging
import os
import time

from transitions import State, Machine
from threading import Thread
from app.rocket.kinetics import Kinetics


class Rocket(Thread):
    states = [
        State(name='sleep',          on_enter=['enter_state', 'enter_sleep'], on_exit='exit_sleep'),
        State(name='ground',         on_enter=['enter_state']),
        State(name='powered',        on_enter=['enter_state']),
        State(name='coast',          on_enter=['enter_state']),
        State(name='descent_drogue', on_enter=['enter_state', 'on_enter_decent_drogue']),
        State(name='descent_main',   on_enter=['enter_state', 'on_enter_descent_main'])
    ]
    transitions = [
        { 'trigger': 'launch', 'source': 'ground', 'dest': 'powered' },
        { 'trigger': 'burnout', 'source': 'powered', 'dest': 'coast' },
        { 'trigger': 'deploy_drogue', 'source': 'coast', 'dest': 'descent_drogue' },
        { 'trigger': 'deploy_main', 'source': 'descent_drogue', 'dest': 'descent_main' },
        { 'trigger': 'touchdown', 'source': 'descent_main', 'dest': 'ground' },
        { 'trigger': 'sleep', 'source': 'ground', 'dest': 'sleep' },
        { 'trigger': 'wake', 'source': 'sleep', 'dest': 'ground' }
    ]

    def __init__(self, device_factory, log_level=logging.INFO, log_dir='app/logs'):
        self.state_machine = Machine(
            model=self,
            states=Rocket.states,
            transitions=Rocket.transitions,
            initial='ground'
        )
        self.last_state = {
            'name': 'ground',
            'time': time.time()
        }
        logging.info('Initialized Rocket')

        self.kinetics = Kinetics(device_factory)
        self.kinetics.activate()
        self.device_factory = device_factory
        self.active = False

    def activate(self):
        if not self.active:
            Thread.__init__(self)
            self.active = True
            self.start()
            if not self.is_alive():
                raise Exception('Failed to activate rocket model')

    def deactivate(self):
        if self.active:
            self.active = False
            self.join(timeout=6)
            if self.is_alive():
                raise Exception('Failed to deactivate rocekt model')

    def enter_state(self):
        self.last_state = {
            'name': self.state,
            'time': time.time()
        }
        self.state_data = {}
        logging.info('hi')

    def enter_sleep(self):
        self.kinetics.deactivate()
        self.device_factory.sleep_all()
        self.state_data['last_radio_poll'] = time.time()

    def during_sleep(self):
        RADIO_POLLING_RATE = 10000 # seconds
        RADIO_POLL_DURATION = 10

        if time.time() - self.state_data['last_radio_poll'] >= RADIO_POLLING_RATE:
            self.device_factory.radio.wake()
            time.sleep(RADIO_POLL_DURATION)
            action = self.device_factory.radio.receive()['action']
            if action == 'wake':
                self.wake()
            else:
                self.state_data['last_radio_poll'] = time.time()
                self.device_factory.radio.sleep()

    def exit_sleep(self):
        self.device_factory.wake_all()
        self.kinetics.activate()

    def during_ground(self):
        LAUNCH_ACCELERATION_THRESHOLD = 1 # m/s^2
        action = self.device_factory.radio.receive()['action']
        if action == 'launch' or self.kinetics.acceleration()['z'] > LAUNCH_ACCELERATION_THRESHOLD:
            self.launch()
        elif action == 'sleep':
            self.sleep()

    def during_powered(self):
        BURNOUT_ACCELERATION_THRESHOLD = 0.0
        MOTOR_BURN_TIME = 3.0
        if self.kinetics.acceleration()['z'] < BURNOUT_ACCELERATION_THRESHOLD or time.time() - self.last_state['time'] > MOTOR_BURN_TIME:
            self.burnout()

    def during_coast(self):
        APOGEE_VELOCTY_THRESHOLD = 8 # m/s
        self.device_factory.brakes.deploy(self.kinetics.compute_brake_percentage())
        if self.kinetics.velocity()['z'] <= APOGEE_VELOCTY_THRESHOLD:
            self.deploy_drogue()
            self.device_factory.brakes.deploy(0.0)

    def on_enter_decent_drogue(self):
        self.device_factory.parachute.deploy_stage_one()

    def during_descent_drogue(self):
        DECENT_DROGUE_TIME = 100 # sec
        DEPLOY_MAIN_ALTITUDE = 1700 # feet
        if self.device_factory.altimeter.read() < DEPLOY_MAIN_ALTITUDE or time.time() - self.last_state['time'] >= DECENT_DROGUE_TIME:
            self.deploy_main()

    def on_enter_descent_main(self):
        self.device_factory.parachute.deploy_stage_two()

    def during_descent_main(self):
        TOUCHDOWN_VELOCITY_THRESHOLD = 0.0
        if self.kinetics.velocity()['z'] <= TOUCHDOWN_VELOCITY_THRESHOLD:
            self.touchdown()

    def run(self):
        while self.active:
            if self.state == 'sleep':
                self.during_sleep()
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
    from test.fixtures.dummy_device_factory import DummyDeviceFactory
    device_factory = DummyDeviceFactory()
    rocket1 = Rocket(device_factory)
    rocket1.activate()
