from pathlib import Path

class TranscriptionService:
    async def transcribe(self, audio_path: str) -> str:
        # Stub for transcription
        name = Path(audio_path).stem
        return f"Transcribed text from {name}"
