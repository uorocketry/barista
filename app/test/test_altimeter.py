import pytest
import time

from app.device import Altimeter
from test.fixtures.dummy_device_factory import DummyDeviceFactory

Altimeter = Altimeter()

def test_sea_level_1():
    raw_data = [255, 255, 255]
    expected_data = 1

    assert Altimeter.parse_raw_data_altitude(raw_data) == expected_data

def test_sea_level_0():
    raw_data = [0, 0, 0]
    expected_data = 0.0

    assert Altimeter.parse_raw_data_altitude(raw_data) == expected_data

def test_sea_level_rand():
    raw_data = [255, 252, 160]
    expected_data = 4.0625

    assert Altimeter.parse_raw_data_altitude(raw_data) == expected_data


def test_temp_level_1():
    raw_data = [255, 255]
    expected_data = 1.0625

    assert Altimeter.parse_raw_data_temp(raw_data) == expected_data

def test_temp_level_0():
    raw_data = [0, 0]
    expected_data = 0.0

    assert Altimeter.parse_raw_data_temp(raw_data) == expected_data

def test_temp_level_rand():
    raw_data = [23, 144]
    expected_data = 23.4375

    assert Altimeter.parse_raw_data_temp(raw_data) == expected_data
