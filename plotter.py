import mw_datastream
from state_generator import *
from mbientlab.metawear import MetaWear, libmetawear, parse_value, cbindings
import time
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.animation as animation

class DataPlot:
    def __init__(self, sg):
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(3,1,1)
        self.ax2 = self.fig.add_subplot(3,1,2)
        self.ax3 = self.fig.add_subplot(3,1,3)
        self.sg = sg
    
    def animate(self, i):

        data = self.sg.get_state()
        x = [d['x'] for d in data]
        y = [d['y'] for d in data]
        z = [d['z'] for d in data]
        t = [d['dt'] for d in data]
        print(x)
        print(y)
        print(z)
        print(t)

        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax1.plot(t, x)
        self.ax2.plot(t, y)
        self.ax3.plot(t, z)

    def start(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=500)
        plt.show()
        






RUN_TIME = 10

MAC_ADDRESS = "F4:64:F5:70:67:0D"

sg = StateGenerator(count=20)
collector = mw_datastream.MetaWearDataCollector(sg, MAC_ADDRESS)
collector.start()
collector.wait_until_collecting()
s = time.time()
while time.time() - s < RUN_TIME:
    data = sg.get_state()
    xs = [d['x'] for d in data]
    ts = [d['dt'] for d in data]
    plt.clear()
    plt.plot(ts, xs)
    plt.pause(0.2)

plt.show()

collector.stop()
