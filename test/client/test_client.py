import pytest
import time

from client import Client
from app.device.radio import Radio
from test.fixtures.dummy_device_factory import DummyDeviceFactory


@pytest.fixture
def rocket():
    device_factory = DummyDeviceFactory()
    return Rocket(device_factory)

@pytest.fixture
def client():
    return Client()


def test_connection_with_rocket(rocket, client):
    def mock_radio_receive():
        return { 'action':'connecting', 'data': [] }
    rocket.device_factory.radio.receive = mock_radio_receive
    client.run()
    assert client.connected == True

# def
