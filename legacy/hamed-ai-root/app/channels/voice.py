"""Provider-neutral voice channel contracts."""
class VoiceAdapter:
    def transcribe(self, audio: bytes) -> str:
        raise NotImplementedError

    def synthesize(self, text: str) -> bytes:
        raise NotImplementedError
