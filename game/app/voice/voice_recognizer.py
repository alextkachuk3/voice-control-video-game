import threading

from app.voice.audio_stream import AudioStream
from app.voice.command_processor import CommandProcessor
from app.voice.whisper_integration import WhisperIntegration


class RealTimeCommandRecognizer:
    def __init__(self, commands, buffer_duration=2, overlap_duration=0.5, on_detected=None):
        self.audio_stream = AudioStream(buffer_duration, overlap_duration)
        self.whisper = WhisperIntegration(
            prompt=f"Commands are: {', '.join(commands)}."
        )
        # self.whisper = WhisperIntegration()
        self.command_processor = CommandProcessor(commands)
        self.__on_detected = on_detected
        self.__is_running = True

    def close(self):
        self.__is_running = False
        self.audio_stream.close()

    def process_audio(self):
        """Process the rolling audio buffer and recognize commands."""
        while self.__is_running:
            # Get the raw bytes from the audio buffer
            audio_bytes = self.audio_stream.get_buffer_as_bytes()
            transcription = self.whisper.transcribe(audio_bytes.read())
            if transcription:
                recognized_command = self.command_processor.process_transcription(transcription)
                if recognized_command:
                    print(f"Recognized Command: {recognized_command}")
                    if self.__on_detected is not None:
                        self.__on_detected(recognized_command)

    def run(self):
        """Start audio streaming and processing."""
        self.audio_stream.start_stream()
        record_thread = threading.Thread(target=self.audio_stream.update_audio_buffer)
        process_thread = threading.Thread(target=self.process_audio)
        record_thread.start()
        process_thread.start()

        print("Audio streaming and processing started. Press Ctrl+C to stop.")
        try:
            record_thread.join()
            process_thread.join()
        except KeyboardInterrupt:
            print("\nStopping...")
