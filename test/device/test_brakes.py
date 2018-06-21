import pytest
from mock import patch

from app.device.brakes import Brakes
from app.utils.servo import Servo
from app.utils.exceptions import InvalidArguments

@patch.object(Servo, 'write')
@patch.object(Servo, '__init__')
def test_init_creates_servo_on_pin_21(servo_init_mock, servo_write_mock):
    servo_init_mock.return_value = None
    servo_write_mock.return_value = None

    brakes = Brakes()

    servo_init_mock.assert_called_once_with(21)
    servo_write_mock.assert_called_once_with(0)

@patch.object(Servo, 'write')
@patch.object(Servo, '__init__')
def test_write_full_close_is_20_precent(servo_init_mock, servo_write_mock):
    servo_init_mock.return_value = None
    servo_write_mock.return_value = None

    brakes = Brakes()
    brakes.deploy(0)

    servo_write_mock.assert_called_with(0.2)
    assert brakes.percentage == 0

@patch.object(Servo, 'write')
@patch.object(Servo, '__init__')
def test_write_full_open(servo_init_mock, servo_write_mock):
    servo_init_mock.return_value = None
    servo_write_mock.return_value = None

    brakes = Brakes()
    brakes.deploy(1.0)

    servo_write_mock.assert_called_with(1.0)
    assert brakes.percentage == 1.0
