import pytest
import time
import numpy
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

def test_acceleration_is_read_directly_from_imu(kinetics):
    def mock_accleration():
        return { 'x': 1.0, 'y': 2.0, 'z': 3.0, 'time': 0 }
    kinetics.imu.read_accel_filtered = mock_accleration

    kinetics.run()

    assert { 'x': 1.0, 'y': 2.0, 'z': 3.0 } == kinetics.acceleration()

def test_velocity_is_computed_from_imu_and_altimeter(kinetics):
    def mock_accleration():
        return { 'x': 1.0, 'y': 2.0, 'z': 3.0, 'time': 0 }
    kinetics.imu.read_accel_filtered = mock_accleration
    def mock_altitude():
        return 100
    kinetics.altimeter.read = mock_altitude

    kinetics.run()
    def mock_accleration():
        return { 'x': 1.0, 'y': 2.0, 'z': 3.0, 'time': 1 }
    kinetics.imu.read_accel_filtered = mock_accleration
    def mock_altitude():
        return 110
    kinetics.altimeter.read = mock_altitude

    kinetics.run()
    assert { 'x': 1.0, 'y': 2.0, 'z': 6.5 } == kinetics.acceleration()
