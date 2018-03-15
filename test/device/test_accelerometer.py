import pytest
from pytest import approx
from app.device.accelerometer import Accelerometer


def test_not_moving():
    raw_data = [18, 0, 4, 0, 234, 0]

    expected_data ={
        'x': 0.0702,
        'z': 0.9828,
        'y': 0.0156,
    }

    parsed_data = Accelerometer.parse_raw_data(raw_data)

    rel_tol = 1e-3
    assert parsed_data['x'] == approx(expected_data['x'], rel = rel_tol)
    assert parsed_data['z'] == approx(expected_data['z'], rel = rel_tol)
    assert parsed_data['y'] == approx(expected_data['y'], rel = rel_tol)



def test_all_zeros():
    raw_data = [0, 0, 0, 0, 0, 0]

    expected_data ={
        'x': 0.0000,
        'y': 0.0000,
        'z': 0.0000
    }

    parsed_data = Accelerometer.parse_raw_data(raw_data)
    #0.0 special case, uses absolute tolenance of 1e-12 strictly    TODO: Delete later
    assert parsed_data['x'] == approx(expected_data['x'])
    assert parsed_data['z'] == approx(expected_data['z'])
    assert parsed_data['y'] == approx(expected_data['y'])


def test_all_ones():
    raw_data = [255, 255, 255, 255, 255, 255]

    expected_data ={
        'x': -0.0039,
        'y': -0.0039,
        'z': -0.0042
    }

    parsed_data = Accelerometer.parse_raw_data(raw_data)

    rel_tol = 5e-2
    assert parsed_data['x'] == approx(expected_data['x'], rel = rel_tol)
    assert parsed_data['z'] == approx(expected_data['z'], rel = rel_tol)
    assert parsed_data['y'] == approx(expected_data['y'], rel = rel_tol)
