import pytest

from app.device.gps import GPS

def test_parse_raw_data_handles_no_fix_data():
    raw_data = {
        'GPGGA': ['015138.800', '', '', '', '', '0', '00', '', '', 'M', '', 'M', '', "*7E\r\n"],
        'GPRMC': ['015138.800', 'V', '', '', '', '', '0.00', '0.00', '060180', '', '', "N*44\r\n"]
    }

    print GPS.parse_raw_data(raw_data)
