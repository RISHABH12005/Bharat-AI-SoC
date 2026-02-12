from nlp.intent_parser import detect_intent

samples = [
    "नमस्ते",
    "लाइट चालू करो",
    "पंखा बंद कर दो",
    "अभी कितना टाइम है",
    "रुको"
]

for s in samples:
    intent = detect_intent(s)
    print(f"{s}  →  {intent}")
