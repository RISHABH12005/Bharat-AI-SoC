from asr.hindi_asr import transcribe_wav
from nlp.intent_parser import detect_intent
from tts.responses import RESPONSES
from tts.hindi_tts import speak

wav = "samples/turn_on.wav"

text = transcribe_wav(wav)
intent = detect_intent(text)

print("ASR:", text)
print("Intent:", intent)

response = RESPONSES.get(intent, RESPONSES["UNKNOWN"])
speak(response)
