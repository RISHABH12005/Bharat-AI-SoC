from nlp.intents import INTENTS


def normalize(text):
    return text.lower().strip()


def detect_intent(text):
    text = normalize(text)

    if not text:
        return None

    for intent, keywords in INTENTS.items():
        for k in keywords:
            if k in text:
                return intent

    return "UNKNOWN"
