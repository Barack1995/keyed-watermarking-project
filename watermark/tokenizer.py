# Team word rules for counting, watermarking, and detection.

import re
import unicodedata

WORD_PATTERN = re.compile(r"[^\W\d_]+")

# Store letters like "é" in one standard form.
def prepare_text(text):
    return unicodedata.normalize("NFC", text)

# Split text into a list of words.
def tokenize(text):
    return WORD_PATTERN.findall(prepare_text(text))

# Make every word lowercase.
def normalize(word):
    return word.lower()


# Split text into words and lowercase them: use this for all counting.
def words(text):
    return [normalize(w) for w in tokenize(text)]