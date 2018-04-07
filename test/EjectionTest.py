import time
from app.rocket.device_factory import DeviceFactory

device_factory = DeviceFactory

while(True):
    message = self.device_factory.radio.receive()
    if message['action'] == u'confirm_comms':
        self.device_factory.radio.transmit('reply', 'Radios receiving and transmitting.')

    elif message['action'] == u'test_ejection_stage_one':
        self.device_factory.radio.transmit('reply', 'Testing Stage One of ejection.')
        self.device_factory.radio.transmit('reply', 'Deploying Stage One in T-minus:')
        for x in range(5):
            t = str(5-x)
            self.device_factory.radio.transmit('reply', x)
            sleep(1)
        self.device_factory.radio.tansmit('reply', '0')
        self.device_factory.parachute.deploy_stage_one()
        self.device_factory.radio.transmit('reply', 'Stage One deployed')


    elif message['action'] == u'test_ejection_stage_two':
        self.device_factory.radio.transmit('reply', 'Testing stage two of ejection.')
        self.device_factory.radio.transmit('reply', 'Deploying Stage Two in T-minus:')
        for x in range(5):
            t = str(5-x)
            self.device_factory.radio.transmit('reply', time)
            sleep(1)
        self.device_factory.radio.transmit('reply', '0')
        self.device_factory.parachute.deploy_stage_two()
        self.device_factory.radio.transmit('reply', 'Stage Two deployed.')

    elif message['action'] == 'quit':
        break;
