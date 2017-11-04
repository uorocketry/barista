import threading

class SensorThread(threading.Thread):
    def run(self):
        print('hi i am the sensor thread')
