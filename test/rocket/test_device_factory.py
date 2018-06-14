import pytest
from mock import patch

from app.device.imu import IMU
from app.device.altimeter import Altimeter
from app.device.brakes import Brakes

from app.device.gps import GPS
from app.device.parachute import Parachute
<<<<<<< HEAD
from app.device.altimeter import Altimeter

from app.rocket.device_factory import DeviceFactory

@patch.object(Altimeter, '__init__')
@patch.object(Accelerometer, '__init__')
=======
from app.device.radio import Radio

from app.rocket.device_factory import DeviceFactory

@patch.object(IMU, '__init__')
@patch.object(Altimeter, '__init__')
>>>>>>> master
@patch.object(Brakes, '__init__')
@patch.object(GPS, '__init__')
@patch.object(Parachute, '__init__')
<<<<<<< HEAD
def test_init_creates_one_of_each_device(altimeter_mock, accelerometer_mock, brakes_mock, gps_mock, gyro_mock, parachute_mock):
    altimeter_mock.return_value = None
    accelerometer_mock.return_value = None
=======
@patch.object(Radio, '__init__')
def test_init_creates_one_of_each_device(imu_mock, altimeter_mock, brakes_mock, gps_mock, parachute_mock, radio_mock):
    imu_mock.return_value = None
    altimeter_mock.return_value = None
>>>>>>> master
    brakes_mock.return_value = None
    gps_mock.return_value = None
    parachute_mock.return_value = None
    radio_mock.return_value = None

    device_factory = DeviceFactory()

<<<<<<< HEAD
    assert altimeter_mock.called
    assert accelerometer_mock.called
=======
    assert imu_mock.called
    assert altimeter_mock.called
>>>>>>> master
    assert brakes_mock.called
    assert gps_mock.called
    assert parachute_mock.called
    assert radio_mock.called
