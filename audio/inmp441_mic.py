import subprocess
import numpy as np
from config.settings import SAMPLE_RATE, CHUNK, SILENCE_THRESHOLD, SILENCE_CHUNK


def record_inmp441(device="mic"):
    print("[Audio] Using INMP441 (Streaming Mode via arecord)")

    cmd = [
        "arecord",
        "-D", device,
        "-f", "S16_LE",
        "-r", str(SAMPLE_RATE),
        "-c", "1",
        "-t", "raw"  
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    silence_chunks = 0
    audio_buffer = []

    try:
        while True:
            data = process.stdout.read(CHUNK * 2)  # 2 bytes per int16

            if not data:
                break

            audio_np = np.frombuffer(data, dtype=np.int16)
            audio_buffer.append(audio_np)

            amplitude = np.abs(audio_np).mean()

            if amplitude < SILENCE_THRESHOLD:
                silence_chunks += 1
            else:
                silence_chunks = 0

            if silence_chunks > SILENCE_CHUNK:
                break

    finally:
        process.terminate()
        process.wait()

    if len(audio_buffer) == 0:
        return None

    audio = np.concatenate(audio_buffer)
    return audio
