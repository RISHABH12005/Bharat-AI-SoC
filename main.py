import logging
from config.settings import RECORD_SECONDS, LOG_PATH
from audio.audio_io import record_audio
from asr.hindi_asr import transcribe_wav, transcribe_audio
from nlp.intent_parser import detect_intent
from tts.responses import RESPONSES
from tts.hindi_tts import speak


logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)


def run_once():
    try:
        audio = record_audio(RECORD_SECONDS)

        text = transcribe_audio(audio)
        logging.info(f"ASR: {text}")

        intent = detect_intent(text)
        logging.info(f"Intent: {intent}")

        response = RESPONSES.get(intent, RESPONSES["UNKNOWN"])
        speak(response)

    except Exception as e:
        logging.error(str(e))
        speak("कोई त्रुटि आ गई है")


def main():
    speak("नमस्ते, सहायक शुरू हो गया है")

    while True:
        run_once()


if __name__ == "__main__":
    main()
