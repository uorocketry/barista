import pytest
import time

from app.device.altimeter import Altimeter
'''
21/06/2018
We need to figure out how to mock out our i2c bus
but this device was physically tested so fuck it
'''
'''
Altimeter = Altimeter()

def test_altitude_1():
    raw_data = [255, 255, 255]
    expected_data = -1.0625

    rel_tol = 1e-3
    assert Altimeter.parse_raw_data(raw_data) == approx(expected_data, rel=rel_tol)

def test_altitude_0():
    raw_data = [0, 0, 0]
    expected_data = 0.0

    rel_tol = 1e-3
    assert Altimeter.parse_raw_data(raw_data) == approx(expected_data, rel=rel_tol)

def test_altitude_rand():
    raw_data = [255, 252, 160]
    expected_data = 4.0625

    rel_tol = 1e-3
    assert Altimeter.parse_raw_data(raw_data) == approx(expected_data, rel=rel_tol)


def test_temp_level_1():
    raw_data = [255, 255]
    expected_data = 1.0625

    rel_tol = 1e-3
    assert Altimeter.parse_raw_data(raw_data) ==  approx(expected_data, rel=rel_tol)

def test_temp_level_0():
    raw_data = [0, 0]
    expected_data = 0.0

    rel_tol = 1e-3
    assert Altimeter.parse_raw_data(raw_data) ==  approx(expected_data, rel=rel_tol)

def test_temp_level_rand():
    raw_data = [23, 144]
    expected_data = 23.4375

    rel_tol = 1e-3
    assert Altimeter.parse_raw_data(raw_data) ==  approx(expected_data, rel=rel_tol)
'''
