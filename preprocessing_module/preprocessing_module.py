import re
from spellchecker import SpellChecker
spell = SpellChecker()

def clean_text(text):
    text = text.replace("\r", "\n")
    text = re.sub(r'[^\S\n]+', ' ', text)
    text = re.sub(r'[^A-Za-z0-9\s\.,;:\?!\'\"\-\n]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def correct_spelling(text):
    words = text.split()
    corrected = []
    for w in words:
        if len(w) <= 2 or any(c.isdigit() for c in w):
            corrected.append(w)
            continue
        if w[0].isupper():
            corrected.append(w)
            continue
        sugg = spell.correction(w)
        corrected.append(sugg if sugg else w)
    return " ".join(corrected)

def preprocess_text(text):
    t = clean_text(text)
    t = correct_spelling(t)
    return t