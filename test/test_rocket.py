import pytest
import time
from app.main import Rocket
from test.fixtures.dummy_device_factory import DummyDeviceFactory

@pytest.fixture
def rocket():
    device_factory = DummyDeviceFactory()
    return Rocket(device_factory)

def test_sleep_puts_all_devices_to_sleep(rocket):
    assert not rocket.device_factory.altimeter.sleeping
    assert not rocket.device_factory.accelerometer.sleeping
    assert not rocket.device_factory.gyro.sleeping
    assert not rocket.device_factory.radio.sleeping

    rocket.sleep()

    assert rocket.device_factory.altimeter.sleeping
    assert rocket.device_factory.accelerometer.sleeping
    assert rocket.device_factory.gyro.sleeping
    assert rocket.device_factory.radio.sleeping


def test_sleep_transitions_to_ground_when_radio_recieves_wake_action(rocket):
    def mock_radio_receive():
        return { 'action':'wake', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.sleep()
    rocket.state_data['last_radio_poll'] = time.time() - 10001
    rocket.during_sleep()

    assert rocket.state == 'ground'
    assert not rocket.device_factory.altimeter.sleeping
    assert not rocket.device_factory.accelerometer.sleeping
    assert not rocket.device_factory.gyro.sleeping
    assert not rocket.device_factory.radio.sleeping

def test_continue_to_sleep_if_radio_does_not_send_wake(rocket):
    def mock_radio_receive():
        return { 'action':'wuba luba dub dub', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.sleep()
    rocket.state_data['last_radio_poll'] = time.time() - 10001
    rocket.during_sleep()

    assert rocket.state == 'sleep'
    assert rocket.device_factory.altimeter.sleeping
    assert rocket.device_factory.accelerometer.sleeping
    assert rocket.device_factory.gyro.sleeping
    assert rocket.device_factory.radio.sleeping

def test_continue_to_sleep_if_polled_within_last_10000_seconds(rocket):
    def mock_radio_receive():
        return { 'action':'wake', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.sleep()
    rocket.state_data['last_radio_poll'] = time.time() - 9995
    rocket.during_sleep()

    assert rocket.state == 'sleep'
    assert rocket.device_factory.altimeter.sleeping
    assert rocket.device_factory.accelerometer.sleeping
    assert rocket.device_factory.gyro.sleeping
    assert rocket.device_factory.radio.sleeping

def test_ground_transitions_to_sleep_when_radio_receives_sleep_action(rocket):
    def mock_radio_receive():
        return { 'action':'sleep', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.during_ground()

    assert rocket.state == 'sleep'
    assert rocket.device_factory.altimeter.sleeping
    assert rocket.device_factory.accelerometer.sleeping
    assert rocket.device_factory.gyro.sleeping
    assert rocket.device_factory.radio.sleeping


def test_ground_transitions_to_powered_when_radio_receives_launch_action(rocket):
    def mock_radio_receive():
        return { 'action':'launch', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.during_ground()

    assert rocket.state == 'powered'

def test_continue_in_ground_transitions_if_radio_does_not_send_launch(rocket):
    def mock_radio_receive():
        return { 'action':'lick lick lick my ballz', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.during_ground()

    assert rocket.state == 'ground'

def test_ground_transitions_to_powered_when_acceleration_over_threshold(rocket):
    rocket.kinetics.acceleration = { 'x': 0.0, 'y': 0.0, 'z': 2.2 }

    rocket.during_ground()

    assert rocket.state == 'powered'

def test_continue_in_ground_if_acceleration_below_threshold(rocket):
    rocket.kinetics.acceleration = { 'x': 0.0, 'y': 0.0, 'z': 1.2 }

    rocket.during_ground()

    assert rocket.state == 'ground'

def test_powered_transitions_to_coast_if_acceleration_falls_below_threshold(rocket):
    rocket.kinetics.acceleration = { 'x': 0.0, 'y': 0.0, 'z': -0.2 }
    rocket.launch()

    rocket.during_powered()

    assert rocket.state == 'coast'

def test_powered_transitions_to_coast_after_3_seconds(rocket):
    rocket.kinetics.acceleration = { 'x': 0.0, 'y': 0.0, 'z': 0.2 }
    rocket.launch()
    rocket.during_powered()
    assert rocket.state == 'powered'

    rocket.last_state['time'] -= 3

    rocket.during_powered()
    assert rocket.state == 'coast'

def test_continue_powered_otherwise(rocket):
    rocket.kinetics.acceleration = { 'x': 0.0, 'y': 0.0, 'z': 0.2 }
    rocket.launch()
    rocket.during_powered()
    assert rocket.state == 'powered'

    rocket.last_state['time'] -= 2

    rocket.during_powered()
    assert rocket.state == 'powered'

def test_coast_deploys_brakes_based_on_kinetics(rocket):
    rocket.state_machine.set_state('coast')
    rocket.kinetics.brake_percentage = 0.321
    rocket.kinetics.velocity['z'] = 70.6

    rocket.during_coast()

    assert rocket.device_factory.brakes.percentage == 0.321

def test_coast_retracts_brakes_and_transitions_to_decent_drogue_at_apogee(rocket):
    def mock_kinetics_brake_percentage():
        return 0.321
    rocket.kinetics.brake_percentage = mock_kinetics_brake_percentage
    rocket.kinetics.velocity['z'] = 3.8
    rocket.state_machine.set_state('coast')

    rocket.during_coast()

    assert rocket.device_factory.brakes.percentage == 0.0
    assert rocket.state == 'descent_drogue'

def test_descent_drogue_deploys_first_stage_recovery(rocket):
    rocket.kinetics.velocity['z'] = 3.8
    rocket.kinetics.brake_percentage = 0.321
    rocket.state_machine.set_state('coast')

    rocket.during_coast()

    assert rocket.device_factory.parachute.deployed_stage_one
    assert rocket.state == 'descent_drogue'

def test_descent_drogue_transitions_to_descent_main_when_altitude_below_1700_feet(rocket):
    def mock_altimeter_read():
        return 1699 #feet
    rocket.device_factory.altimeter.read = mock_altimeter_read
    rocket.state_machine.set_state('descent_drogue')

    rocket.during_descent_drogue()

    assert rocket.device_factory.parachute.deployed_stage_two
    assert rocket.state == 'descent_main'

def test_descent_drogue_transitions_to_descent_main_after_100_seconds(rocket):
    def mock_altimeter_read():
        return 321202 #feet
    rocket.device_factory.altimeter.read = mock_altimeter_read
    rocket.state_machine.set_state('descent_drogue')
    rocket.last_state['time'] = time.time() - 101

    rocket.during_descent_drogue()

    assert rocket.device_factory.parachute.deployed_stage_two
    assert rocket.state == 'descent_main'

def test_descent_main_transitions_to_ground_when_velocity_below_threshold(rocket):
    rocket.kinetics.velocity['z'] = 0
    rocket.state_machine.set_state('descent_main')

    rocket.during_descent_main()

    assert rocket.state == 'ground'

def test_valid_transitions(rocket):
    assert rocket.state == 'ground'
    rocket.sleep()
    assert rocket.state == 'sleep'
    rocket.wake()
    assert rocket.state == 'ground'
    rocket.launch()
    assert rocket.state == 'powered'
    rocket.burnout()
    assert rocket.state == 'coast'
    rocket.deploy_drogue()
    assert rocket.state == 'descent_drogue'
    rocket.deploy_main()
    assert rocket.state == 'descent_main'
    rocket.touchdown()
    assert rocket.state == 'ground'
    rocket.sleep()
    assert rocket.state == 'sleep'
    rocket.wake()
    assert rocket.state == 'ground'
