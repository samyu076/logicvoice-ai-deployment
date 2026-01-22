import io
import wave

SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2  # int16


class AudioBuffer:
    def __init__(self):
        self.buffer = bytearray()

    def add_chunk(self, chunk: bytes):
        self.buffer.extend(chunk)

    def clear(self):
        self.buffer.clear()

    def size(self):
        return len(self.buffer)

    def to_wav_bytes(self) -> bytes:
        wav_io = io.BytesIO()
        with wave.open(wav_io, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(SAMPLE_WIDTH)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(self.buffer)
        return wav_io.getvalue()
