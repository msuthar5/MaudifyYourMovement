import serial
import pyaudio
import wave
import time
import threading

CHUNK_SIZE = 1024
class AudioPlayer:
    def __init__(self):
        self.pyaudio = pyaudio.PyAudio()

    def play_track(self, track):
        AsyncSound(self.pyaudio, track).start()

class AsyncSound(threading.Thread):
    def __init__(self, pyaudio_obj, track):
        threading.Thread.__init__(self)
        self.pyaudio = pyaudio_obj
        self.track = track

    def run(self):
        with wave.open(self.track, "rb") as f:
            stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(f.getsampwidth()),
                            channels=f.getnchannels(),
                            rate=f.getframerate(),
                            output=True)
            data = f.readframes(CHUNK_SIZE)
            while data:
                stream.write(data)
                data = f.readframes(CHUNK_SIZE)
            
            stream.stop_stream()
            stream.close()
