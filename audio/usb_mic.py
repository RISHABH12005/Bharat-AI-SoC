import pyaudio
import numpy as np

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK = 1024
FORMAT = pyaudio.paInt16


def record_usb(duration_sec=2.0, device_index=None):
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=device_index
    )

    frames = []
    for _ in range(int(SAMPLE_RATE / CHUNK * duration_sec)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    audio_np = np.frombuffer(b"".join(frames), dtype=np.int16)
    return audio_np
