import time
from app.device.radio import Radio
from app.device.parachute import Parachute


radio = Radio()
parachute = Parachute()

def wait_loop():
    while True:
        print('Waiting')
        message = radio.receive()
        if message == None:
            time.sleep(1)
        else:
            return message

def transmit(action, data):
    print('Transmiting: ' + str(action) +' - '+ str(data))
    radio.transmit(action, data)


if __name__ == "__main__":
    wait_loop()
    transmit('Hello', 'from Pi')

    # message = wait_loop()
    # if message['action'] == u'deploy':
    #     print('deploy')

    while True:
        message = wait_loop()


        if message['action'] == u'ping':
            transmit('reply', 'PI!')



        elif message['action'] == u'test_ejection_stage_one':
            transmit('reply', 'Testing Stage One of ejection.')
            radio.transmit('reply', 'Deploying Stage One in T-minus:')
            for x in range(5):
                t = str(5-x)
                radio.transmit('reply', t)
                time.sleep(1)
            radio.transmit('reply', '0')
            parachute.deploy_stage_one()
            # device_factory.parachute.deploy_stage_one()
            transmit('reply', 'Stage One deployed')
            time.sleep(15)
            parachute.cut_power()


        elif message['action'] == u'test_ejection_stage_two':
            transmit('reply', 'Testing stage two of ejection.')
            radio.transmit('reply', 'Deploying Stage Two in T-minus:')
            for x in range(5):
                t = str(5-x)
                radio.transmit('reply', t)
                time.sleep(1)
            radio.transmit('reply', '0')
            parachute.deploy_stage_two()
            # device_factory.parachute.deploy_stage_two()
            transmit('reply', 'Stage Two deployed.')
            time.sleep(15)
            parachute.cut_power()

        elif message == None:
            time.sleep(1)

        elif message['action'] == u'quit':
            break;

        time.sleep(1)
