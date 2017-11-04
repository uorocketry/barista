import threading
import time

class ContolThread(threading.Thread):
    def run(self):
        print('hi i am the control thread')
        time.sleep(2)
        print('hi i am the control thread')
