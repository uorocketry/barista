import threading

class CommsThread(threading.Thread):
    def run(self):
        print('hi i am the comm thread')
