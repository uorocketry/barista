from app.device.radio import Radio
import logging
while True:

    radio = Radio()
    message = radio.receive()
    command = raw_input('>>>')

    if message['action'] == u'reply':
        print(message['data'])

    if command == 'help':
        print('''
        help                 = prints this stuff
        connect <port>       = connect to XBee on port
        send <action> <data> = send a message
        ''')
    elif command.startswith('connect'):
        radio.set_port(command.split(' ')[1])
    elif command.startswith('send'):
        action = command.split(' ')[1]
        data = command.split(' ')[2:-1] if len(command.split(' ')) > 2 else None
        radio.transmit(action, data)
    elif command == 'quit':
        break
