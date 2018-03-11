import pytest
import time
from app.rocket.kinetics import Kinetics

from test.fixtures.dummy_device_factory import DummyDeviceFactory

def test_run_appends_to_acceleration():
    kinetics = Kinetics(DummyDeviceFactory())

def test_run_computes_velocity_using_trapaziod_rule():
    kinetics = Kinetics(DummyDeviceFactory())

def test_run_computes_position_using_trapaziod_rule():
    kinetics = Kinetics(DummyDeviceFactory())

def test_start_asynchonously_updates_acceleration():
    kinetics = Kinetics(DummyDeviceFactory())
    kinetics.activate()
    initial_acceleration = kinetics.acceleration.last()
    time.sleep(1)
    final_acceleration = kinetics.acceleration.last()
    kinetics.deactivate()
    assert initial_acceleration != final_acceleration

def test_start_asynchonously_updates_velocity():
    kinetics = Kinetics(DummyDeviceFactory())
    kinetics.activate()
    initial_velocity = kinetics.velocity.last()
    time.sleep(1)
    final_velocity = kinetics.velocity.last()
    kinetics.deactivate()
    assert initial_velocity != final_velocity

def test_start_asynchonously_updates_position():
    kinetics = Kinetics(DummyDeviceFactory())
    kinetics.activate()
    initial_position = kinetics.position.last()
    time.sleep(1)
    final_position = kinetics.position.last()
    kinetics.deactivate()
    assert initial_position != final_position
