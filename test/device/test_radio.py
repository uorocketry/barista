import pytest

import json
from app.device.radio import Radio
from test.fixtures.dummy_serial import DummySerial

def test_ignores_invalid_messages():
    invalid_message = {'action': 'NOT A VALID ACTION', 'data': []}
    radio = Radio()
    radio.serial = DummySerial(json.dumps(invalid_message))

    message = radio.receive()

    assert message['action'] == None
    assert message['data'] == None

def test_valid_actions_contain_no_duplicates():
    radio = Radio()
    assert len(radio.VALID_ACTIONS) == len(set(radio.VALID_ACTIONS))

def test_captures_connecting_message():
    expected_message = {'action': Radio.ACTION_CONNECTING, 'data': []}
    radio = Radio()
    radio.serial = DummySerial(json.dumps(expected_message))

    message = radio.receive()

    assert message['action'] == expected_message['action']
    assert message['data'] == expected_message['data']

def test_captures_transition_message():
    expected_message = {'action': Radio.ACTION_TRANSITION, 'data': 'my_state'}
    radio = Radio()
    radio.serial = DummySerial(json.dumps(expected_message))

    message = radio.receive()

    assert message['action'] == expected_message['action']
    assert message['data'] == expected_message['data']

def test_captures_arm_message():
    expected_message = {'action': Radio.ACTION_ARM, 'data': []}
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


def test_captures_test_report_connecting_message():
    expected_message = {'action': Radio.ACTION_CONNECTING, 'data': []}
    radio = Radio()
    radio.serial = DummySerial(json.dumps(expected_message))

    message = radio.receive()

    assert message['action'] == expected_message['action']
    assert message['data'] == expected_message['data']
