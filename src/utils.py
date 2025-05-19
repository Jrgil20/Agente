import re
from typing import List, Tuple

HASHTAG_PATTERN = re.compile(r"#\w+")
URL_PATTERN = re.compile(r"https?://\S+")


def clean_text(text: str) -> str:
    """Normaliza el texto: minúsculas, elimina enlaces e imágenes, caracteres especiales."""
    text = text.lower()
    text = URL_PATTERN.sub("", text)
    text = re.sub(r"[^\w\s#]", "", text)
    return text.strip()


def extract_hashtags(text: str) -> List[str]:
    """Extrae hashtags del texto."""
    return HASHTAG_PATTERN.findall(text)


def extract_keywords(text: str, keywords: List[str]) -> List[str]:
    """Extrae palabras clave relevantes del texto."""
    found = [kw for kw in keywords if kw in text]
    return found 