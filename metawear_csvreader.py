import threading
import time

class MetaWearCsvReader(threading.Thread):
    def __init__(self, filename, name):
        threading.Thread.__init__(self)
        self.f = filename
        self.name = name
        self.x = None
        self.y = None
        self.z = None
        self.now = time.time()
        self.running = False

    def run(self):
        self.now = time.time()
        with open(self.f, "r") as data:
            self.running = True
            data_in = data.readline()
            data_in = data.readline()
            while len(data_in) > 0 and self.running is True:
                values = data_in.split(',')
                wait_until = float(values[2])
                while time.time() - self.now < wait_until:
                    time.sleep(0.01)
                self.x = float(values[3])
                self.y = float(values[4])
                self.z = float(values[5])
                data_in = data.readline()

    def wait_until_collecting(self):
        while self.running is False:
            pass
        return True

    def stop(self):
        self.running = False
        
                
            


