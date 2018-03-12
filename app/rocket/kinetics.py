class Kinetics(object):
    def __init__(self):
        self.acceleration = { 'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.position = { 'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.velocity = { 'x': 0.0, 'y': 0.0, 'z': 0.0}

        self.brake_percentage = 0.5

    def activate(self):
        pass

    def deactivate(self):
        pass
