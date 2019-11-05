from mbientlab.metawear import MetaWear, libmetawear, parse_value, cbindings
from ctypes import c_void_p, cast, POINTER
from time import sleep
from threading import Event
from sys import argv
import threading


class MetaWearDataStream:
    def __init__(self, mac_address, callback, frequency=12.0):
        self.device = MetaWear(mac_address)
        self.callback = cbindings.FnVoid_VoidP_DataP(callback)
        self.processor = None
        self.freq = frequency
        

    def setup(self):
        self.device.connect()
        libmetawear.mbl_mw_settings_set_connection_parameters(self.device.board, 7.5, 7.5, 0, 6000)
        sleep(1.5)

        e = Event()

        def processor_created(context, pointer):
            self.processor = pointer
            e.set()
        fn_wrapper = cbindings.FnVoid_VoidP_VoidP(processor_created)
        libmetawear.mbl_mw_acc_set_odr(self.device.board, self.freq)
        libmetawear.mbl_mw_acc_write_acceleration_config(self.device.board)
        acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(self.device.board)
        libmetawear.mbl_mw_dataprocessor_average_create(acc, 4, None, fn_wrapper)
        e.wait()
        libmetawear.mbl_mw_datasignal_subscribe(self.processor, None, self.callback)

    def start(self):
    
        libmetawear.mbl_mw_acc_enable_acceleration_sampling(self.device.board)
        libmetawear.mbl_mw_acc_start(self.device.board)

    def __enter__(self):
        self.setup()
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        libmetawear.mbl_mw_debug_reset(self.device.board)

class MetaWearDataObserver(threading.Thread):
    def __init__(self, mac_address, name):
        threading.Thread.__init__(self)
        self.mac_address = mac_address
        self.name = name
        self.x = None
        self.y = None
        self.z = None
    
    def run(self):
        with MetaWearDataStream(self.mac_address, self.ingest_stream) as mwds:
            self.running = True
            while self.running is True:
                pass

    def ingest_stream(self, ctx, data):
        data = parse_value(data)
        self.x = data["x"]
        self.y = data["y"]
        self.z = data["z"]

    def stop(self):
        self.running = False

    def wait_until_collecting(self):
        while self.running is False:
            pass
        return True