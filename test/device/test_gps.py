import pytest
from app.device.gps import GPS

def test_no_satalites():
    raw_data = {
        'GPGGA': ['015138.800', '', '', '', '', '0', '00', '', '', 'M', '', 'M', '', '*7E\r\n'],
        'GPRMC': ['015138.800', 'V', '', '', '', '', '0.00', '0.00', '060180', '', '', 'N*44\r\n']
    }
    expected_data = {
        'fix': False,
        'satelites': 0
    }

    assert GPS.parse_raw_data(raw_data) == expected_data


def test_random_nmea():
    raw_data = {
        'GPGGA': ['123519', '04807.038', 'N', '01131.000', 'E', '1', '08', '0.9', '545.4', 'M', '46.9', 'M', '', '*47'],
        'GPRMC': ['123519', ' A', '04807.038', 'N', '01131.000', 'E', '022.4', '084.4' , '230394', '003.1', 'W*6A']
    }
    expected_data = {
        'fix': True,
        'satelites': 8,
        'time (UTC)': '23:35:19',
        'altitude (ASL)': 545.4,
        'latitude (deg)': 4.80,
        'latitude (min)': 0.7038,
        'latitude (dir)': 'N',
        'longitude (deg)': 11.0,
        'longitude (min)': 31.0,
        'longitude (dir)': 'E',
        'ground_speed': 11.514
    }

    assert GPS.parse_raw_data(raw_data) == expected_data


def test_empty_strings():
    raw_data = {
        'GPGGA': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        'GPRMC': ['', '', '', '', '', '', '', '' , '', '', '']
    }
    expected_data = {
        'fix': False,
        'satelites': 0
    }

    assert GPS.parse_raw_data(raw_data) == expected_data

def test_log_errors_in_parse_raw_data():
    expected_data = {
        'fix': False,
        'satelites': 0
    }
    # TODO figure out how to stub the serial port
    assert True
