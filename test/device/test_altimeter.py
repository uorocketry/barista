import pytest
from pytest import approx
from app.device.altimeter import Altimeter

def test_parse_raw_data_all_bits_1():
    raw_data = [255, 255, 255]
    expected_data = -1.0625

    parsed_data = Altimeter.parse_raw_data(raw_data)

    rel_tol = 1e-3
    assert parsed_data == approx(expected_data, rel=rel_tol)

def test_parse_raw_data_all_bits_0():
    raw_data = [0,0,0]
    expected_data = 0

    parsed_data = Altimeter.parse_raw_data(raw_data)

    rel_tol = 1e0
    assert parsed_data == approx(expected_data, rel=rel_tol)

def test_parse_raw_data_1km():
    raw_data[0,62,128]
    expected_data = 1000

    parsed_data = Altimeter.parse_raw_data(raw_data)

    rel_tol = 1e0
    assert parsed_data == approx(expected_data, rel=rel_tol)

def test_parse_raw_data_negative():
    raw_data[255,239,160]
    expected_data = -262

    parsed_data = Altimeter.parse_raw_data(raw_data)
    rel_tol = 1e0

def test_write_barometric_setting_negative():
    new_setting = -1
    old_setting = Altimeter.read_bar_setting()
    Altimeter.write_bar_setting(new_setting)

    new_setting = Altimeter.read_bar_setting()
    assert new_setting == old_setting

def test_write_barometric_setting_integer():
    new_setting = 51727
    Altimeter.write_bar_setting(new_setting)

    new_setting = Altimeter.read_bar_setting()
    assert new_setting == approx(new_setting, rel=1e0)

def test_write_barometric_setting_decimal():
    new_setting = 103454.17/2
    Altimeter.write_bar_setting(new_setting)

    new_setting = Altimeter.read_bar_setting()
    assert new_setting == 103454
