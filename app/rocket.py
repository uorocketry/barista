from transitions import Machine

class Rocket(object):
    states = ['asleep', 'ground', 'powered', 'coast', ' descent', 'descent_drogue', 'descent_main']
    transitions = [
        { 'trigger': 'launch', 'source': 'ground', 'dest': 'powered' },
        { 'trigger': 'burnout', 'source': 'powered', 'dest': 'coast' },
        { 'trigger': 'appogee', 'source': 'coast', 'dest': 'descent' },
        { 'trigger': 'deploy_drogue', 'source': 'descent', 'dest': 'descent_drogue' },
        { 'trigger': 'deploy_main', 'source': 'descent_drogue', 'dest': 'descent_main' },
        { 'trigger': 'touchdown', 'source': 'descent_main', 'dest': 'ground' }
        { 'trigger': 'sleep', 'source': 'ground', 'dest': 'asleep' }
        { 'trigger': 'wake', 'source': 'asleep', 'dest': 'ground' }
    ]

    def __init__(self):
        self.state_machine = Machine(model=self, states=Rocket.states, transitions=Rocket.transitions, initial='ground')
