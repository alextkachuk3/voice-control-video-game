import threading
from audio_stream import AudioStream
from whisper_integration import WhisperIntegration
from command_processor import CommandProcessor


class RealTimeCommandRecognizer:
    def __init__(self, commands, buffer_duration=2, overlap_duration=0.5):
        self.audio_stream = AudioStream(buffer_duration, overlap_duration)
        self.whisper = WhisperIntegration(
            prompt=f"Commands are: {', '.join(commands)}."
        )
        # self.whisper = WhisperIntegration()
        self.command_processor = CommandProcessor(commands)

    def process_audio(self):
        """Process the rolling audio buffer and recognize commands."""
        while True:
            # Get the raw bytes from the audio buffer
            audio_bytes = self.audio_stream.get_buffer_as_bytes()
            transcription = self.whisper.transcribe(audio_bytes.read())
            if transcription:
                recognized_command = self.command_processor.process_transcription(transcription)
                if recognized_command:
                    print(f"Recognized Command: {recognized_command}")

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
