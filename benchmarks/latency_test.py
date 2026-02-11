import time
import os
import psutil
from datetime import datetime

import soundfile as sf

from asr.hindi_asr import transcribe_wav
from nlp.intent_parser import detect_intent
from tts.responses import RESPONSES
from tts.hindi_tts import speak
from audio.audio_io import record_audio

from config.settings import (
    USE_MIC,
    MIC_DURATION,
    SAMPLE_RATE,
    TEST_WAV,
    TMP_DIR,
    RESULTS_DIR
)


def now():
    return time.perf_counter()


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def log_to_file(lines):
    ensure_dir(RESULTS_DIR)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"{RESULTS_DIR}/latency_{ts}.log"
    with open(path, "w") as f:
        f.write("\n".join(lines))
    return path


def main():
    output = []
    output.append("=== Latency Benchmark ===")
    output.append("Audio format: 16kHz mono WAV")
    output.append(f"Mode: {'MIC' if USE_MIC else 'FILE'}")

    process = psutil.Process(os.getpid())
    process.cpu_percent(interval=None)  # init CPU measurement

    ensure_dir(TMP_DIR)

    t0 = now()

    if USE_MIC:
        audio, sr = record_audio(MIC_DURATION)
        mic_wav = f"{TMP_DIR}/mic.wav"
        sf.write(mic_wav, audio, sr)
        text = transcribe_wav(mic_wav)
    else:
        text = transcribe_wav(TEST_WAV)

    t1 = now()

    intent = detect_intent(text)
    t2 = now()

    response = RESPONSES.get(intent, RESPONSES["UNKNOWN"])
    speak(response)
    t3 = now()

    cpu = process.cpu_percent(interval=None)
    mem = process.memory_info().rss / (1024 * 1024)

    output.extend([
        f"CPU usage         : {cpu:.1f} %",
        f"Memory usage      : {mem:.1f} MB",
        f"ASR latency       : {(t1 - t0) * 1000:.1f} ms",
        f"Intent latency    : {(t2 - t1) * 1000:.2f} ms",
        f"TTS latency       : {(t3 - t2) * 1000:.1f} ms",
        f"End-to-End latency: {(t3 - t0) * 1000:.1f} ms",
        "",
        f"ASR Output : {text}",
        f"Intent     : {intent}"
    ])

    for line in output:
        print(line)

    log_path = log_to_file(output)
    print(f"\n[Saved] {log_path}")


if __name__ == "__main__":
    main()
