import io
import queue

import numpy as np
import sounddevice as sd
import soundfile as sf


class AudioStream:
    SAMPLE_RATE = 12000
    CHUNK_SIZE = 512
    CHANNELS = 1

    def __init__(self, buffer_duration=2, overlap_duration=0.5):
        self.stream = None
        self.buffer_duration = buffer_duration
        self.overlap_duration = overlap_duration
        self.buffer_size = int(self.SAMPLE_RATE * buffer_duration)
        self.overlap_size = int(self.SAMPLE_RATE * overlap_duration)
        self.audio_buffer = np.zeros(self.buffer_size, dtype="float32")
        self.audio_queue = queue.Queue()

        self.__is_running = True

    def close(self):
        self.__is_running = False

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
        """Continuously update the rolling audio buffer with new chunks."""
        while self.__is_running:
            chunk = self.audio_queue.get()
            chunk_size = len(chunk)
            self.audio_buffer = np.roll(self.audio_buffer, -chunk_size)
            self.audio_buffer[-chunk_size:] = chunk.flatten()

    def get_buffer_as_bytes(self):
        """
        Retrieve the rolling buffer as raw bytes in WAV format for Whisper API.
        """
        int16_buffer = (self.audio_buffer * 32767).astype("int16")

        audio_bytes = io.BytesIO()
        sf.write(audio_bytes, int16_buffer, samplerate=self.SAMPLE_RATE, format="WAV")
        audio_bytes.seek(0)
        return audio_bytes
