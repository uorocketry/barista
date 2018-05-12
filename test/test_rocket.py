import pytest
import time
from app.main import Rocket
from test.fixtures.dummy_device_factory import DummyDeviceFactory

@pytest.fixture
def rocket():
    device_factory = DummyDeviceFactory()
    return Rocket(device_factory)

@pytest.yield_fixture(autouse=True)
def run_around_tests(rocket):
    yield
    rocket.kinetics.deactivate()

def test_connecting_transitions_to_ground_when_radio_received_connect(rocket):
    rocket.state_machine.set_state('connecting')
    def mock_radio_receive():
        return { 'action':'connecting', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.during_connecting()

    assert rocket.state == 'ground'

def test_connecting_does_not_transition_to_ground_if_radio_does_not_receive_connect(rocket):
    rocket.state_machine.set_state('connecting')
    def mock_radio_receive():
        return { 'action':'grabage', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.during_connecting()

    assert rocket.state == 'connecting'

def test_sleep_puts_all_devices_to_sleep(rocket):
    rocket.state_machine.set_state('ground')
    assert not rocket.device_factory.altimeter.sleeping
    assert not rocket.device_factory.imu.sleeping
    assert not rocket.device_factory.radio.sleeping

    rocket.sleep()

    assert rocket.device_factory.altimeter.sleeping
    assert rocket.device_factory.imu.sleeping
    assert rocket.device_factory.radio.sleeping


def test_sleep_transitions_to_ground_when_radio_recieves_wake_action(rocket):
    rocket.state_machine.set_state('ground')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 1.4 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration
    def mock_radio_receive():
        return { 'action':'wake', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.sleep()
    rocket.state_data['last_radio_poll'] = time.time() - 10001
    rocket.during_sleep()

    assert rocket.state == 'ground'
    assert not rocket.device_factory.altimeter.sleeping
    assert not rocket.device_factory.imu.sleeping
    assert not rocket.device_factory.radio.sleeping

def test_continue_to_sleep_if_radio_does_not_send_wake(rocket):
    rocket.state_machine.set_state('ground')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 1.4 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration
    def mock_radio_receive():
        return { 'action':'wuba luba dub dub', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.sleep()
    rocket.state_data['last_radio_poll'] = time.time() - 10001
    rocket.during_sleep()

    assert rocket.state == 'sleep'
    assert rocket.device_factory.altimeter.sleeping
    assert rocket.device_factory.imu.sleeping
    assert rocket.device_factory.radio.sleeping

def test_continue_to_sleep_if_polled_within_last_10000_seconds(rocket):
    rocket.state_machine.set_state('ground')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 1.4 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration
    def mock_radio_receive():
        return { 'action':'wake', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.sleep()
    rocket.state_data['last_radio_poll'] = time.time() - 9995
    rocket.during_sleep()

    assert rocket.state == 'sleep'
    assert rocket.device_factory.altimeter.sleeping
    assert rocket.device_factory.imu.sleeping
    assert rocket.device_factory.radio.sleeping

def test_ground_transitions_to_sleep_when_radio_receives_sleep_action(rocket):
    rocket.state_machine.set_state('ground')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 1.4 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration
    def mock_radio_receive():
        return { 'action':'sleep', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.during_ground()

    assert rocket.state == 'sleep'
    assert rocket.device_factory.altimeter.sleeping
    assert rocket.device_factory.imu.sleeping
    assert rocket.device_factory.radio.sleeping


def test_ground_transitions_to_powered_when_radio_receives_launch_action(rocket):
    rocket.state_machine.set_state('ground')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 1.4 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration
    def mock_radio_receive():
        return { 'action':'launch', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.during_ground()

    assert rocket.state == 'powered'

def test_continue_in_ground_transitions_if_radio_does_not_send_launch(rocket):
    rocket.state_machine.set_state('ground')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 1.4 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration
    def mock_radio_receive():
        return { 'action':'lick lick lick my ballz', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.during_ground()

    assert rocket.state == 'ground'

def test_ground_transitions_to_powered_when_acceleration_over_threshold(rocket):
    rocket.state_machine.set_state('ground')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 1.6 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration

    rocket.during_ground()

    assert rocket.state == 'powered'

def test_continue_in_ground_if_acceleration_below_threshold(rocket):
    rocket.state_machine.set_state('ground')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 1.2 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration

    rocket.during_ground()

    assert rocket.state == 'ground'

def test_powered_transitions_to_coast_if_acceleration_falls_below_threshold(rocket):
    rocket.state_machine.set_state('powered')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': -0.2 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration

    rocket.during_powered()

    assert rocket.state == 'coast'

def test_powered_transitions_to_coast_after_3_seconds(rocket):
    rocket.state_machine.set_state('powered')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 0.2 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration

    rocket.during_powered()
    assert rocket.state == 'powered'

    rocket.last_state['time'] -= 3

    rocket.during_powered()
    assert rocket.state == 'coast'

def test_continue_powered_otherwise(rocket):
    rocket.state_machine.set_state('powered')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 0.2 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration

    rocket.during_powered()
    assert rocket.state == 'powered'

    rocket.last_state['time'] -= 2

    rocket.during_powered()
    assert rocket.state == 'powered'

def test_coast_deploys_brakes_based_on_kinetics(rocket):
    rocket.state_machine.set_state('coast')
    def mock_kinetics_velocity():
        return { 'x': 0.0, 'y': 0.0, 'z': 70.6 }
    rocket.kinetics.velocity = mock_kinetics_velocity
    def mock_kinetics_brakes_percentage():
        return 0.321
    rocket.kinetics.compute_brakes_percentage = mock_kinetics_brakes_percentage

    rocket.during_coast()

    assert rocket.device_factory.brakes.percentage == 0.321

def test_coast_retracts_brakes_and_transitions_to_decent_drogue_at_apogee(rocket):
    rocket.state_machine.set_state('coast')
    def mock_kinetics_velocity():
        return { 'x': 0.0, 'y': 0.0, 'z': 3.8 }
    rocket.kinetics.velocity = mock_kinetics_velocity
    def mock_kinetics_brakes_percentage():
        return 0.321
    rocket.kinetics.compute_brakes_percentage = mock_kinetics_brakes_percentage

    rocket.during_coast()

    assert rocket.device_factory.brakes.percentage == 0.0
    assert rocket.state == 'descent_drogue'

def test_descent_drogue_deploys_first_stage_recovery(rocket):
    rocket.state_machine.set_state('coast')
    def mock_kinetics_velocity():
        return { 'x': 0.0, 'y': 0.0, 'z': 3.8 }
    rocket.kinetics.velocity = mock_kinetics_velocity

    rocket.during_coast()

    assert rocket.device_factory.parachute.deployed_stage_one
    assert rocket.state == 'descent_drogue'

def test_descent_drogue_transitions_to_descent_main_when_altitude_below_1700_feet(rocket):
    rocket.state_machine.set_state('descent_drogue')
    def mock_altimeter_read():
        return 1699 #feet
    rocket.device_factory.altimeter.read = mock_altimeter_read

    rocket.during_descent_drogue()

    assert rocket.device_factory.parachute.deployed_stage_two
    assert rocket.state == 'descent_main'

def test_descent_drogue_transitions_to_descent_main_after_100_seconds(rocket):
    rocket.state_machine.set_state('descent_drogue')
    def mock_altimeter_read():
        return 321202 #feet
    rocket.device_factory.altimeter.read = mock_altimeter_read
    rocket.last_state['time'] = time.time() - 101

    rocket.during_descent_drogue()

    assert rocket.device_factory.parachute.deployed_stage_two
    assert rocket.state == 'descent_main'

def test_descent_main_transitions_to_ground_when_velocity_below_threshold(rocket):
    rocket.state_machine.set_state('descent_main')
    def mock_kinetics_velocity():
        return { 'x': 0.0, 'y': 0.0, 'z': 0.0 }
    rocket.kinetics.velocity = mock_kinetics_velocity

    rocket.during_descent_main()

    assert rocket.state == 'ground'

def test_valid_transitions(rocket):
    assert rocket.state == 'connecting'
    rocket.connected()
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
