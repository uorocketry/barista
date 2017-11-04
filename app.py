from threads import *

def cmd_help():
    print('\nhelp')
    print('lists availible commands')


def cmd_run():
    active_thread = ContolThread()
    active_thread.run()


print('\n888888b.                 d8b        888            ')
print('888  "88b                Y8P        888              ')
print('888  .88P                           888              ')
print('8888888K.  8888b. 888d888888.d8888b 888888 8888b.    ')
print('888  "Y88b    "88b888P"  88888K     888       "88b   ')
print('888    888.d888888888    888"Y8888b.888   .d888888   ')
print('888   d88P888  888888    888     X88Y88b. 888  888   ')
print('8888888P" "Y888888888    888 88888P\' "Y888"Y888888\n')

while(True):
    line = raw_input('>>> ')

    cmd = line.split(' ')[0]
    args = line.split(' ')[1:]

    if cmd == 'help':
        cmd_help()
    elif cmd == 'run':
        cmd_run()
    else:
        exec(line)
