# Detect the watermark in a text.

from watermark.tokenizer import words
from watermark.color import word_color, GREEN

# Score one text with the key.
def detect(text, key, threshold=None):
    word_list = words(text)
    if len(word_list) == 0:
        raise ValueError("Empty input: the text has no words to score.")
    green_count = sum(1 for w in word_list if word_color(w, key) == GREEN)
    score = green_count / len(word_list)
    total_words = len(word_list)
    distinct_words = len(set(word_list))
    flagged = None if threshold is None else score > threshold
    return {
        "score": score,
        "flagged": flagged,
        "total_words": total_words,
        "distinct_words": distinct_words,
    }
    
    