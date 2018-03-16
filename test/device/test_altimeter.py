import pytest
from pytest import approx
from app.device.altimeter import Altimeter

def test_prd_all_1():
    raw_data = [255, 255, 255]
    expected_data = -1.0625

    parsed_data = Altimeter.parse_raw_data(raw_data)

    rel_tol = 1e-3
    assert parsed_data == approx(expected_data, rel=rel_tol)

def test_prd_all_0():
    raw_data = [0,0,0]
    expected_data = 0

    parsed_data = Altimeter.parse_raw_data(raw_data)

    rel_tol = 1e0
    assert parsed_data == approx(expected_data, rel=rel_tol)

def test_prd_1km():
    raw_data[0,62,128]
    expected_data = 1000

    parsed_data = Altimeter.parse_raw_data(raw_data)

    rel_tol = 1e0
    assert parsed_data == approx(expected_data, rel=rel_tol)

def test_prd_negative():
    raw_data[255,239,160]
    expected_data = -262

    parsed_data = Altimeter.parse_raw_data(raw_data)
    rel_tol = 1e0

def test_wbs_negvalue():
    user_setting = -1
    old_setting = Altimeter.read_bar_setting()
    Altimeter.write_bar_setting(user_setting)

    new_setting = Altimeter.read_bar_setting()
    assert new_setting == old_setting

def test_wbs_write():
    user_setting = 51727
    Altimeter.write_bar_setting(user_setting)

    new_setting = Altimeter.read_bar_setting()
    assert new_setting == approx(user_setting, rel=1e0)

def test_wbs_decimal():
    user_setting = 103454.17/2
    Altimeter.write_bar_setting(user_setting)

    new_setting = Altimeter.read_bar_setting()
    assert new_setting == 103454
