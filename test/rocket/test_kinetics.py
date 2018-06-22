import pytest
import time
import numpy
from app.rocket.kinetics import Kinetics, TimeWindow

from test.fixtures.dummy_device_factory import DummyDeviceFactory

@pytest.fixture
def kinetics():
    device_factory = DummyDeviceFactory()
    return Kinetics(DummyDeviceFactory())

def test_start_asynchonously_updates_vertical_position(kinetics):
    kinetics.activate()
    initial_vertical_position = kinetics.vertical_position()
    time.sleep(1)
    final_vertical_position = kinetics.vertical_position()
    kinetics.deactivate()
    assert initial_vertical_position != final_vertical_position

def test_start_asynchonously_updates_vertical_velocity(kinetics):
    kinetics.activate()
    initial_vertical_velocity = kinetics.vertical_velocity()
    time.sleep(1)
    final_vertical_velocity = kinetics.vertical_velocity()
    kinetics.deactivate()
    assert initial_vertical_velocity != final_vertical_velocity

def test_time_window_computes_correct_integration():
    window = TimeWindow()
    window.append(1.0)
    window.append(4.0)
    res = window.integrate_last(0.0, 1.0)
    assert res == 2.5

def test_time_window_computes_correct_derivative():
    window = TimeWindow()
    window.append(4.0)
    window.append(1.0)
    res = window.derive_last(0.0, 1.0)
    assert res == -3.0
