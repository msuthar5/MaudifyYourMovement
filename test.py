import mw_datastream
from state_generator import *
from mbientlab.metawear import MetaWear, libmetawear, parse_value, cbindings
import time

MAC_ADDRESS = "F4:64:F5:70:67:0D"

sg = StateGenerator()
collector = mw_datastream.MetaWearDataCollector(sg, MAC_ADDRESS)
collector.start()
collector.wait_until_collecting()
time.sleep(5)
collector.stop()

print(sg.total)