import subprocess
import tempfile
import os
from config.env import is_wsl


def speak(text):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name

    subprocess.run([
        "espeak-ng",
        "-v", "hi",
        "-s", "150",
        "-a", "200",
        "-w", wav_path,
        text
    ], check=True)

    if not is_wsl():
        subprocess.run(["aplay", wav_path])
    else:
        print(f"[WSL] Audio generated: {wav_path}")

    return wav_path
