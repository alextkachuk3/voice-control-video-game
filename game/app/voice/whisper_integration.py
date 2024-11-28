import openai
from dotenv import load_dotenv
import os


class WhisperIntegration:
    def __init__(self, sample_rate=16000, prompt=None):
        self.sample_rate = sample_rate
        self.prompt = prompt

        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def transcribe(self, audio_buffer):
        """Send audio buffer to Whisper for transcription."""
        if not openai.api_key:
            raise ValueError("OpenAI API key not set. Please check your .env file or environment variables.")

        import io
        import soundfile as sf

        with io.BytesIO() as wav_file:
            sf.write(wav_file, audio_buffer, self.sample_rate, format="WAV")
            wav_file.seek(0)
            response = openai.Audio.transcribe(
                model="whisper-1",
                file=wav_file,
                temperature=0,
                prompt=self.prompt,
            )
        return response.get("text", "").strip()
