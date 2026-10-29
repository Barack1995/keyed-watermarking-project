# auto_watermark.py
# Watermark passages automatically: swap red words for green WordNet words.
# It uses the secret key, so it is NOT for query-access attacks.

import csv
import os
from collections import Counter

from nltk.corpus import wordnet as wn

from watermark_helper import read_key
from watermark.tokenizer import WORD_PATTERN, prepare_text, normalize, words
from watermark.color import word_color, GREEN
from watermark.detector import detect

TARGET = 0.70
ORIGINALS = "data/passages/evaluation/watermarking"
OUTPUT = "watermarked/evaluation"
PASSAGES = ["E-W-01", "E-W-02", "E-W-03", "E-W-04", "E-W-05",
            "E-W-06", "E-W-07", "E-W-08", "E-W-09", "E-W-10"]

VERSION = "v3"
MIN_WORD_LENGTH = 4
LOG_FILE = f"watermarked/auto_log_evaluation_{VERSION}.csv"


# Get synonyms and broader words for one word from WordNet.
def candidates(word):
    found = set()
    for meaning in wn.synsets(word):
        for group in [meaning] + meaning.hypernyms():
            for lemma in group.lemmas():
                found.add(lemma.name().lower())
    return found


# Keep only candidates that are one word, different, and green.
def green_synonyms(word, key):
    good = []
    for c in sorted(candidates(word)):
        if words(c) == [c] and c != word and word_color(c, key) == GREEN:
            good.append(c)
    return good


# Give the new word the same capital letters as the old word.
def match_case(new, old):
    if len(old) > 1 and old.isupper():
        return new.upper()
    if old[0].isupper():
        return new.capitalize()
    return new


# Replace every occurrence of one word in the text.
def replace_word(text, old, new):
    def swap(match):
        word = match.group()
        if normalize(word) == old:
            return match_case(new, word)
        return word
    return WORD_PATTERN.sub(swap, text)


# Swap red words for green words until the score reaches the target.
def watermark(text, key):
    text = prepare_text(text)
    counts = Counter(words(text))
    red_words = [w for w, n in counts.most_common()
    if len(w) >= MIN_WORD_LENGTH and word_color(w, key) != GREEN]
    changes = []
    for word in red_words:
        if detect(text, key)["score"] >= TARGET:
            break
        options = green_synonyms(word, key)
        if not options:
            continue
        text = replace_word(text, word, options[0])
        changes.append((word, options[0], counts[word]))
    return text, changes


def main():
    key = read_key()
    os.makedirs(OUTPUT, exist_ok=True)
    rows = []
    for pid in PASSAGES:
        with open(f"{ORIGINALS}/{pid}.txt", encoding="utf-8") as f:
            original = f.read()
        new_text, changes = watermark(original, key)
        with open(f"{OUTPUT}/{pid}_{VERSION}.txt", "w", encoding="utf-8") as f:
            f.write(new_text)
        before = detect(original, key)["score"]
        after = detect(new_text, key)["score"]
        changed = sum(n for _, _, n in changes)
        print(pid, round(before, 3), "->", round(after, 3), "| words changed:", changed)
        rows.append({
            "passage_id": pid, "version": VERSION, "target": TARGET,
            "min_word_length": MIN_WORD_LENGTH,
            "score_before": round(before, 3), "score_after": round(after, 3),
            "target_reached": "yes" if after >= TARGET else "no",
            "words_changed": changed,
            "swaps": "; ".join(f"{old}->{new} ({n}x)" for old, new, n in changes),
        })
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print("Log saved to", LOG_FILE)


if __name__ == "__main__":
    main()