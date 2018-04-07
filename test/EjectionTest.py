import time
from app.device.radio import Radio
from app.rocket.device_factory import DeviceFactory

device_factory = DeviceFactory()
radio = Radio()

while(True):
    message = radio.receive()
    if message['action'] == u'confirm_comms':
        radio.transmit('reply', 'Radios receiving and transmitting.')

    elif message['action'] == u'test_ejection_stage_one':
        radio.transmit('reply', 'Testing Stage One of ejection.')
        radio.transmit('reply', 'Deploying Stage One in T-minus:')
        for x in range(5):
            t = str(5-x)
            radio.transmit('reply', x)
            sleep(1)
        radio.tansmit('reply', '0')
        device_factory.parachute.deploy_stage_one()
        radio.transmit('reply', 'Stage One deployed')


    elif message['action'] == u'test_ejection_stage_two':
        radio.transmit('reply', 'Testing stage two of ejection.')
        radio.transmit('reply', 'Deploying Stage Two in T-minus:')
        for x in range(5):
            t = str(5-x)
            radio.transmit('reply', time)
            sleep(1)
        radio.transmit('reply', '0')
        device_factory.parachute.deploy_stage_two()
        radio.transmit('reply', 'Stage Two deployed.')

    elif message == None:
        sleep(1)

    elif message['action'] == 'quit':
        break;
