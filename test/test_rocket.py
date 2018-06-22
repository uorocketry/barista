import pytest
import time
from app.main import Rocket
from test.fixtures.dummy_device_factory import DummyDeviceFactory

@pytest.fixture
def rocket():
    device_factory = DummyDeviceFactory()
    return Rocket(device_factory)

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
        return { 'action':'position_report', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.during_connecting()
    rocket.kinetics.deactivate()

    assert rocket.state == 'connecting'

def test_auto_arm_after_1500_seconds(rocket):
    rocket.state_machine.set_state('connecting')
    def mock_radio_receive():
        return { 'action':'position_report', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.last_state['time'] -= 1500

    rocket.during_connecting()
    rocket.kinetics.deactivate()

    assert rocket.state == 'armed'

def test_ground_transitions_to_armed_when_radio_receives_arm_action(rocket):
    rocket.state_machine.set_state('ground')
    def mock_radio_receive():
        return { 'action':'arm', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.during_ground()
    rocket.kinetics.deactivate()

    assert rocket.state == 'armed'

def test_remain_in_ground_till_receiving_arm_action(rocket):
    rocket.state_machine.set_state('ground')
    def mock_radio_receive():
        return { 'action':'connecting', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive

    rocket.during_ground()
    rocket.kinetics.deactivate()

    assert rocket.state == 'ground'

def test_armed_transitions_to_powered_when_acceleration_over_threshold(rocket):
    rocket.state_machine.set_state('armed')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 6 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration

    rocket.during_armed()
    rocket.kinetics.deactivate()

    assert rocket.state == 'powered'

def test_continue_in_armed_if_acceleration_below_threshold(rocket):
    rocket.state_machine.set_state('armed')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 1.2 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration

    rocket.during_armed()
    rocket.kinetics.deactivate()

    assert rocket.state == 'armed'

def test_powered_transitions_to_coast_if_acceleration_falls_below_threshold(rocket):
    rocket.state_machine.set_state('powered')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': -0.2 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration

    rocket.during_powered()
    rocket.kinetics.deactivate()

    assert rocket.state == 'coast'

def test_powered_transitions_to_coast_after_3_seconds(rocket):
    rocket.state_machine.set_state('powered')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 0.2 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration

    rocket.during_powered()
    assert rocket.state == 'powered'

    rocket.last_state['time'] -= 3.0

    rocket.during_powered()
    rocket.kinetics.deactivate()

    assert rocket.state == 'coast'

def test_continue_powered_otherwise(rocket):
    rocket.state_machine.set_state('powered')
    def mock_kinetics_acceleration():
        return { 'x': 0.0, 'y': 0.0, 'z': 0.2 }
    rocket.kinetics.acceleration = mock_kinetics_acceleration

    rocket.during_powered()
    assert rocket.state == 'powered'

    rocket.last_state['time'] -= 2.0

    rocket.during_powered()
    rocket.kinetics.deactivate()

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
    rocket.kinetics.deactivate()

    assert rocket.device_factory.brakes.percentage == 0.321

def test_coast_no_brakes_above_250(rocket):
    rocket.state_machine.set_state('coast')
    def mock_kinetics_velocity():
        return { 'x': 0.0, 'y': 0.0, 'z': 251 }
    rocket.kinetics.velocity = mock_kinetics_velocity
    def mock_kinetics_brakes_percentage():
        return 0.321
    rocket.kinetics.compute_brakes_percentage = mock_kinetics_brakes_percentage

    rocket.during_coast()
    rocket.kinetics.deactivate()

    assert rocket.device_factory.brakes.percentage == 0.0

def test_coast_retracts_brakes_and_transitions_to_decent_at_apogee(rocket):
    rocket.state_machine.set_state('coast')
    def mock_kinetics_vertical_velocity():
        return -9.81
    rocket.kinetics.vertical_velocity = mock_kinetics_vertical_velocity
    def mock_kinetics_brakes_percentage():
        return 0.321
    rocket.kinetics.compute_brakes_percentage = mock_kinetics_brakes_percentage

    rocket.during_coast()
    rocket.kinetics.deactivate()

    assert rocket.device_factory.brakes.percentage == 0.0
    assert rocket.state == 'descent'

def test_valid_transitions(rocket):
    assert rocket.state == 'connecting'
    rocket.connected()
    assert rocket.state == 'ground'
    rocket.arm()
    rocket.kinetics.deactivate()
    assert rocket.state == 'armed'
    rocket.launch()
    assert rocket.state == 'powered'
    rocket.burnout()
    assert rocket.state == 'coast'
    rocket.apogee()
    assert rocket.state == 'descent'
    rocket.touchdown()
    assert rocket.state == 'ground'
