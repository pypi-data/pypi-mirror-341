import unicodedata
import re

STOPWORDS = {"di", "del", "della", "dei", "delle", "lo", "la", "il", "i", "gli", "le", "in", "a", "da", "su"}

def normalize_name(name: str) -> str:
    name = name.strip().lower()
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
    name = re.sub(r'[^a-z\\s]', '', name)
    tokens = name.split()
    tokens = [t for t in tokens if t not in STOPWORDS]
    return ' '.join(tokens)
