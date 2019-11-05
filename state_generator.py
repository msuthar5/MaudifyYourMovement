import time
from datetime import datetime
import threading

class StateGenerator(threading.Thread):
    def __init__(self, count=10, frequency=12):
        threading.Thread.__init__(self)
        self.time_wait = 1.0 / frequency
        self.count = count
        self.data = []
        self.total = 0
        self.readable_state = []
        self.observers = []
        self.running = False
    
    def add_observer(self, observer):
        self.observers.append(observer)

    def observe(self):
        out = {}
        for observer in self.observers:
            out[observer.name + "_x"] = observer.x
            out[observer.name + "_y"] = observer.y
            out[observer.name + "_z"] = observer.z
        
        self.data.append(out)
        while len(self.data) > self.count:
            self.data.pop(0)
        
        self.readable_state = self.data

    def get_state(self):
        return self.readable_state

    def run(self):
        for observer in self.observers:
            observer.start()

        for observer in self.observers:
            observer.wait_until_collecting()
        
        self.running = True

        while self.running is True:
            self.observe()

    def stop(self):
        for observer in self.observers:
            observer.stop()
        self.running = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()



