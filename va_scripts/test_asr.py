from audio.audio_io import record_audio
from asr.hindi_asr import transcribe_wav
from nlp.intent_parser import detect_intent
import soundfile as sf
import tempfile
import os

audio = record_audio(3.0)

if audio is None:
    print("[ASR] No mic available (WSL test mode)")
    exit(0)

tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
sf.write(tmp.name, audio, 16000)

text = transcribe_wav(tmp.name)
intent = detect_intent(text)
os.unlink(tmp.name)

print("🗣️ Hindi ASR Output:")
print(text)
print("Intent:", intent)
