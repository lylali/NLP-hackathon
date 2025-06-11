import re
from langdetect import detect

def clean_text(text):
    """Remove HTML tags and extra whitespace."""
    text = re.sub(r'<.*?>', '', str(text))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def detect_language(text):
    """Detect the language of the input text."""
    try:
        return detect(text)
    except:
        return "unknown"
