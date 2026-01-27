import subprocess
import numpy as np
import tempfile
import soundfile as sf


def record_inmp441(duration_sec=2.0, device="hw:1,0"):
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        cmd = [
            "arecord",
            "-D", device,
            "-f", "S16_LE",
            "-r", "16000",
            "-c", "1",
            "-d", str(int(duration_sec)),
            tmp.name
        ]

        subprocess.run(cmd, check=True)

        audio, _ = sf.read(tmp.name, dtype="int16")
        return audio
