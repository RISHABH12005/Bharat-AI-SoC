import time
import os
import psutil
from datetime import datetime

from asr.hindi_asr import transcribe_audio, transcribe_wav
from nlp.intent_parser import detect_intent
from tts.responses import RESPONSES
from tts.hindi_tts import speak
from audio.audio_io import record_audio

from config.settings import (
    USE_MIC,
    MIC_DURATION,
    TEST_WAV,
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
    output.append("=== Latency Benchmark (In-Memory Optimized) ===")
    output.append("Audio format: 16kHz mono int16")
    output.append(f"Mode: {'MIC' if USE_MIC else 'FILE'}")

    process = psutil.Process(os.getpid())
    process.cpu_percent(interval=None)

    # ===============================
    # RECORDING
    # ===============================
    record_start = now()

    if USE_MIC:
        audio = record_audio(MIC_DURATION)
        if audio is None:
            print("No audio device available.")
            return
        record_end = now()
    else:
        record_end = now()

    # ===============================
    # ASR (Compute Only)
    # ===============================
    asr_start = now()

    if USE_MIC:
        text = transcribe_audio(audio)
    else:
        text = transcribe_wav(TEST_WAV)

    asr_end = now()

    # ===============================
    # INTENT
    # ===============================
    intent_start = now()
    intent = detect_intent(text)
    intent_end = now()

    # ===============================
    # TTS
    # ===============================
    tts_start = now()
    response = RESPONSES.get(intent, RESPONSES["UNKNOWN"])
    speak(response)
    tts_end = now()

    # ===============================
    # SYSTEM STATS
    # ===============================
    cpu = process.cpu_percent(interval=None)
    mem = process.memory_info().rss / (1024 * 1024)

    # ===============================
    # METRICS
    # ===============================
    recording_latency = (record_end - record_start) * 1000
    asr_latency = (asr_end - asr_start) * 1000
    intent_latency = (intent_end - intent_start) * 1000
    tts_latency = (tts_end - tts_start) * 1000
    e2e_no_record = (tts_end - asr_start) * 1000
    total_latency = (tts_end - record_start) * 1000

    output.extend([
        "",
        f"CPU usage              : {cpu:.1f} %",
        f"Memory usage           : {mem:.1f} MB",
        "",
        f"Recording latency      : {recording_latency:.1f} ms",
        f"ASR compute latency    : {asr_latency:.1f} ms",
        f"Intent latency         : {intent_latency:.2f} ms",
        f"TTS latency            : {tts_latency:.1f} ms",
        "",
        f"End-to-End (no record) : {e2e_no_record:.1f} ms",
        f"Total latency          : {total_latency:.1f} ms",
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
