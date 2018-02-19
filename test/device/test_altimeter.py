import pytest
from pytest import approx
from app.device.altimeter import altimeter

#parse_raw_data test cases
def test_prd_all_1:
    raw_data = [255, 255, 255]
    expected_data = -1.0625

    parsed_data = Altimeter.parse_raw_data(raw_data)

    rel_tol = 1e-3
    assert parsed_data == approx(expected_data, rel=rel_tol)
