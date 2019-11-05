import state_generator
import gesture_detector
import metawear_csvreader
import audio_player
import threading
import time


class MaudifyYourMovementSimulator(threading.Thread):
    def __init__(self, observers, delay = 0.1, state_size=1):
        threading.Thread.__init__(self)
        self.sg = state_generator.StateGenerator(count=state_size)
        for key, item in observers.items():
            self.sg.add_observer(metawear_csvreader.MetaWearCsvReader(item, key))
        self.gd = gesture_detector.GestureDetector()
        self.ap = audio_player.AudioPlayer()
        self.running = False
        self.delay = delay

    def __enter__(self):
        self.running = True
        self.run()

    def __exit__(self, type, value, traceback):
        self.stop()

    def run(self):
        with self.sg as sg:
            while self.running is True:
                time.sleep(self.delay)
                result = self.gd.detect(self.sg.get_state())
                if result is True:
                    print(result)
                    self.ap.play_track("sounds/boing.wav")

    def stop(self):
        self.running = False