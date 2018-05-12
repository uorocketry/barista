import pytest

import json
from app.device.radio import Radio
from test.fixtures.dummy_serial import DummySerial

def test_ignores_invalid_messages():
    invalid_message = {'action': 'NOT A VALID ACTION', 'data': []}
    radio = Radio()
    radio.serial = DummySerial(json.dumps(invalid_message))

    assert radio.receive() == None

def test_valid_actions_contain_no_duplicates():
    radio = Radio()
    assert len(radio.VALID_ACTIONS) is len(set(radio.VALID_ACTIONS))

def test_captures_wake_message():
    expected_message = {'action': Radio.ACTION_WAKE, 'data': []}
    radio = Radio()
    radio.serial = DummySerial(json.dumps(expected_message))

    message = radio.receive()

    assert message['action'] == expected_message['action']
    assert message['data'] == expected_message['data']

def test_captures_sleep_message():
    expected_message = {'action': Radio.ACTION_SLEEP, 'data': []}
    radio = Radio()
    radio.serial = DummySerial(json.dumps(expected_message))

    message = radio.receive()

    assert message['action'] == expected_message['action']
    assert message['data'] == expected_message['data']

def test_captures_launch_message():
    expected_message = {'action': Radio.ACTION_LAUNCH, 'data': []}
    radio = Radio()
    radio.serial = DummySerial(json.dumps(expected_message))

    message = radio.receive()

    assert message['action'] == expected_message['action']
    assert message['data'] == expected_message['data']


def test_captures_test_brake_message():
    expected_message = {'action': Radio.ACTION_TEST_BRAKES, 'data': []}
    radio = Radio()
    radio.serial = DummySerial(json.dumps(expected_message))

    message = radio.receive()

    assert message['action'] == expected_message['action']
    assert message['data'] == expected_message['data']

def test_captures_test_report_position_message():
    expected_message = {'action': Radio.ACTION_POSITION_REPORT, 'data': []}
    radio = Radio()
    radio.serial = DummySerial(json.dumps(expected_message))

    message = radio.receive()

    assert message['action'] == expected_message['action']
    assert message['data'] == expected_message['data']
