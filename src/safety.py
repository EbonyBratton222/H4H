"""Safety checks that run in plain Python, whatever Gemma says."""

EMERGENCY_PHRASES = [
    "can't get up", "cant get up", "cannot get up", "can not get up",
    "chest pain", "unconscious", "not breathing", "unresponsive", "000",
]
NDIS_PHRASES = ["ndis", "disabilit"]

EMERGENCY_MESSAGE = "If this is an emergency, call 000."
NDIS_MESSAGE = "This tool covers aged care. For the NDIS, see ndis.gov.au or ask your GP."


def _normalise(text):
    return text.lower().replace("’", "'")   # treat curly apostrophes as straight


def is_emergency(text):
    text = _normalise(text)
    return any(phrase in text for phrase in EMERGENCY_PHRASES)


def mentions_ndis(text):
    text = _normalise(text)
    return any(phrase in text for phrase in NDIS_PHRASES)
