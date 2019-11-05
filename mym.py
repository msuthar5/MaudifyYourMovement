import state_generator
import gesture_detector
import mw_datastream
import audio_player
import threading
import time


class MaudifyYourMovement(threading.Thread):
    def __init__(self, mac_address, delay = 0.1):
        threading.Thread.__init__(self)
        self.sg = state_generator.StateGenerator(count = 1)
        self.observer = mw_datastream.MetaWearDataObserver(mac_address, "accel")
        self.sg.add_observer(self.observer)
        self.gd = gesture_detector.GestureDetector()
        self.ap = audio_player.AudioPlayer()
        self.running = False
        self.delay = delay

    def __enter__(self):
        self.running = True
        self.run()

    def __exit__(self, type, value, traceback):
        self.stop()
        self.collector.stop()

    def run(self):
        self.collector.start()
        self.collector.wait_until_collecting()
        with self.sg as sg:
            while self.running is True:
                time.sleep(self.delay)
                result = self.gd.detect(self.sg.get_state())
                if result is True:
                    print(result)
                    self.ap.play_track("sounds/boing.wav")

    def stop(self):
        self.running = False

