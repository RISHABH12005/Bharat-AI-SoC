import json
import wave
from vosk import Model, KaldiRecognizer
from config.settings import CHUNK
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model",
    "vosk-model-small-hi-0.22"
)

_model = None


def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError("Vosk Hindi model not found")
        _model = Model(MODEL_PATH)
    return _model


model = load_model()


def transcribe_wav(wav_path):
    wf = wave.open(wav_path, "rb")

    if wf.getnchannels() != 1 or wf.getframerate() != 16000:
        raise ValueError("Audio must be mono 16kHz WAV")

    
    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)

    result = json.loads(rec.FinalResult())
    return result.get("text", "")


def transcribe_audio(audio_np):
    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)

    chunk_samples = CHUNK
    total_samples = len(audio_np)

    for i in range(0, total_samples, chunk_samples):
        chunk = audio_np[i:i + chunk_samples]
        rec.AcceptWaveform(chunk.tobytes())

    result = json.loads(rec.FinalResult())
    return result.get("text", "")


