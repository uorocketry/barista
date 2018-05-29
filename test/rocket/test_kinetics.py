import pytest
import time
import numpy as np
from app.rocket.kinetics import Kinetics

from test.fixtures.dummy_device_factory import DummyDeviceFactory

@pytest.fixture
def kinetics():
    device_factory = DummyDeviceFactory()
    return Kinetics(DummyDeviceFactory())

def test_start_asynchonously_updates_acceleration(kinetics):
    kinetics.activate()
    initial_acceleration = kinetics.acceleration()
    time.sleep(1)
    final_acceleration = kinetics.acceleration()
    kinetics.deactivate()
    assert initial_acceleration != final_acceleration

def test_start_asynchonously_updates_velocity(kinetics):
    kinetics.activate()
    initial_velocity = kinetics.velocity()
    time.sleep(1)
    final_velocity = kinetics.velocity()
    kinetics.deactivate()
    assert initial_velocity != final_velocity

def test_start_asynchonously_updates_position(kinetics):
    kinetics.activate()
    initial_position = kinetics.position()
    time.sleep(1)
    final_position = kinetics.position()
    kinetics.deactivate()
    assert initial_position != final_position

def test_matrix_conversion(kinetics):
    dict = {'x': 1, 'y': 2, 'z': 3 }
    matrix = kinetics.dict_to_matrix(dict)
    assert matrix is np.array([[1],
                               [2],
                               [3]])
