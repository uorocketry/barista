import pytest
import time

from from app.device import Altimeter
# from test.fixtures.dummy_device_factory import DummyDeviceFactory

Altimeter = Altimeter()

def test_sea_level():
    raw_data = {

    }

    expected_data =

    assert Altimeter.parse_raw_data_altitude(raw_data) == expected_data

def test_temp_level():
    raw_data = {

    }

    expected_data =

    assert Altimeter.parse_raw_data_temp(raw_data) == expected_data
