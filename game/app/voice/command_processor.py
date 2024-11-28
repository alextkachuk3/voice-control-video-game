class CommandProcessor:
    def __init__(self, commands):
        self.commands = commands

    def find_command(self, transcription):
        """Identify a known command in the transcription."""
        for command in self.commands:
            if command in transcription.lower():
                return command
        return None

    def process_transcription(self, transcription):
        """Process transcription and return the recognized command."""
        return self.find_command(transcription)