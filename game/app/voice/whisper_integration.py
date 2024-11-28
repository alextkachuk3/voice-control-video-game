import openai
from dotenv import load_dotenv
import os
import io


class WhisperIntegration:
    def __init__(self, sample_rate=16000, prompt=None):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("OpenAI API key not set. Please check your .env file or environment variables.")

        self.sample_rate = sample_rate
        self.prompt = prompt
        self.client = openai.OpenAI(api_key=self.api_key)

    def transcribe(self, audio_bytes):
        """
        Transcribe raw audio data bytes using Whisper.
        Args:
            audio_bytes (bytes): Raw audio data in bytes format.
        Returns:
            str: Transcription of the audio.
        """
        if not isinstance(audio_bytes, (bytes, bytearray)):
            raise ValueError("Audio data must be bytes or bytearray.")

        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.mp3"

        # Send the audio bytes to Whisper API
        response = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            temperature=0,
            prompt=self.prompt,
        )

        text = response.text
        return text
