import pytest
from mock import patch

from app.device.brake import Brake
from app.utils.servo import Servo
from app.utils.exceptions import InvalidArguments

@patch.object(Servo, 'write')
@patch.object(Servo, '__init__')
def test_init_creates_servo_on_pin_18(servo_init_mock, servo_write_mock):
    servo_init_mock.return_value = None
    servo_write_mock.return_value = None

    brake = Brake()

    servo_init_mock.assert_called_once_with(18)
    servo_write_mock.assert_called_once_with(0)

@patch.object(Servo, 'write')
@patch.object(Servo, '__init__')
def test_write_percentage_0(servo_init_mock, servo_write_mock):
    servo_init_mock.return_value = None
    servo_write_mock.return_value = None

    brake = Brake()
    brake.deploy(0.0)

    servo_write_mock.assert_called_with(0)
    assert brake.percentage == 0

@patch.object(Servo, 'write')
@patch.object(Servo, '__init__')
def test_write_percentage_100(servo_init_mock, servo_write_mock):
    servo_init_mock.return_value = None
    servo_write_mock.return_value = None

    brake = Brake()
    brake.deploy(100.0)

    servo_write_mock.assert_called_with(180)
    assert brake.percentage == 100.0


@patch.object(Servo, 'write')
@patch.object(Servo, '__init__')
def test_write_invalid_percentage_raises(servo_init_mock, servo_write_mock):
    servo_init_mock.return_value = None
    servo_write_mock.return_value = None

    brake = Brake()
    with pytest.raises(InvalidArguments):
        brake.deploy(-1)
