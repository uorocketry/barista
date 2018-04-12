from app.device.radio import Radio
import time

r = Radio()


def wait_loop():
    print('waiting...')
    while True:
        message = r.receive()
        if message == None:
            time.sleep(1)
        else:
            return message

def message_loop():
    print('message loop')
    ctr = 0
    while ctr <= 10:
        print(r.receive())
        ctr += 1

    return True

def transmit(action, data):
    r.transmit(action, data)
    message_loop()

if __name__ == "__main__":

    r.transmit('Hello', 'from Tx')
    message = wait_loop()
    print(message)

    time.sleep(1)
    print('test_ejection_stage_one')
    transmit('test_ejection_stage_one','from Tx')

    time.sleep(5)
    print('test_ejection_stage_two')
    transmit('test_ejection_stage_two','from Tx')

    time.sleep(1)
    print('quit')
    r.transmit('quit','from Tx')
