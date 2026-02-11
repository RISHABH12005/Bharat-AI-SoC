import pyaudio
import numpy as np
from config.settings import (
    SAMPLE_RATE,
    CHANNELS,
    CHUNK,
    FORMAT,
    SILENCE_THRESHOLD,
    SILENCE_CHUNK
)


def record_usb(device_index=None):
    print("[Audio] Using USB microphone (Streaming Mode)")

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=device_index
    )

    silence_chunks = 0
    frames = []

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

            audio_np = np.frombuffer(data, dtype=np.int16)
            amplitude = np.abs(audio_np).mean()

            if amplitude < SILENCE_THRESHOLD:
                silence_chunks += 1
            else:
                silence_chunks = 0

            if silence_chunks > SILENCE_CHUNK:
                break

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

    if len(frames) == 0:
        return None

    audio_np = np.frombuffer(b"".join(frames), dtype=np.int16)
    return audio_np
