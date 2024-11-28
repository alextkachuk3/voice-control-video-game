import sounddevice as sd
import numpy as np
import queue


class AudioStream:
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    CHANNELS = 1

    def __init__(self, buffer_duration=2, overlap_duration=0.5):
        self.stream = None
        self.buffer_duration = buffer_duration
        self.overlap_duration = overlap_duration
        self.buffer_size = int(self.SAMPLE_RATE * buffer_duration)
        self.overlap_size = int(self.SAMPLE_RATE * overlap_duration)
        self.audio_buffer = np.zeros(self.buffer_size, dtype="float32")
        self.audio_queue = queue.Queue()

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Audio error: {status}")
        self.audio_queue.put(indata.copy())

    def start_stream(self):
        self.stream = sd.InputStream(
            samplerate=self.SAMPLE_RATE,
            channels=self.CHANNELS,
            blocksize=self.CHUNK_SIZE,
            callback=self._audio_callback,
            dtype="float32",
        )
        self.stream.start()

    def update_audio_buffer(self):
        while True:
            chunk = self.audio_queue.get()
            chunk_size = len(chunk)
            self.audio_buffer = np.roll(self.audio_buffer, -chunk_size)
            self.audio_buffer[-chunk_size:] = chunk.flatten()
