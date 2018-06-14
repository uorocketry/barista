class DummySerial(object):
    def __init__(self, read_value):
        self.read_value = read_value

    def readline(self):
        return self.read_value
