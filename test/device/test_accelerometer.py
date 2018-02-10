import pytest
from pytest import approx
from app.device.accelerometer import Accelerometer


def test_not_moving():
#sample data while not moving
    raw_data = [18, 0, 4, 0, 234, 0]

#parsed sample data
    expected_data ={
        'x': 0.0702,
        'z': 0.9828,
        'y': 0.0156,
        'time': 1518136213.101481
    }

    parsed_data = Accelerometer.parse_raw_data(raw_data)
    #approx default: relative tolerance of 1e-6; absolute tolerance of 1e-12   TODO: Delete later
    rel_tol = 1e-3
    assert parsed_data["x"] == approx(expected_data["x"], rel = rel_tol)
    assert parsed_data["z"] == approx(expected_data["z"], rel = rel_tol)
    assert parsed_data["y"] == approx(expected_data["y"], rel = rel_tol)



def test_all_zeros():
#sample data while all registers are "0"s
    raw_data = [0, 0, 0, 0, 0, 0]

#parsed sample data
    expected_data ={
        'x': 0.0000,
        'z': 0.0000,
        'y': 0.0000,
        'time': 1518136213.101481
    }

    parsed_data = Accelerometer.parse_raw_data(raw_data)
    #0.0 special case, uses absolute tolenance of 1e-12 strictly    TODO: Delete later
    assert parsed_data["x"] == approx(expected_data["x"])
    assert parsed_data["z"] == approx(expected_data["z"])
    assert parsed_data["y"] == approx(expected_data["y"])


def test_all_ones():
#sample data while all registers are "1"s
    raw_data = [255, 255, 255, 255, 255, 255]

#parsed sample data
    expected_data ={
        'x': 255.5865,
        'z': 275.2470,
        'y': 255.5865,
        'time': 1518136213.101481 #TODO
    }

    parsed_data = Accelerometer.parse_raw_data(raw_data)
    rel_tol = 5e-2
    assert parsed_data["x"] == approx(expected_data["x"], rel = rel_tol)
    assert parsed_data["z"] == approx(expected_data["z"], rel = rel_tol)
    assert parsed_data["y"] == approx(expected_data["y"], rel = rel_tol)
