
# Helps a person watermark a passage by hand.
# It uses the secret key, so it is NOT for query-access attacks.

import sys
import csv
SYNONYMS_FILE = "watermarked/synonyms_candidates.csv"
from collections import Counter

from settings import KEY_FILE
from watermark.tokenizer import WORD_PATTERN, prepare_text, normalize, words
from watermark.color import word_color, GREEN
from watermark.detector import detect

# Read the secret key from its file.
def read_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

# Put [ ] around every red word in the text.
def mark_red(text, key):
    def mark(match):
        word = match.group()
        if word_color(normalize(word), key) == GREEN:
            return word
        return "[" + word + "]"
    return WORD_PATTERN.sub(mark, prepare_text(text))

# Print a passage with red words marked, and its score.
def show(path, key):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    print(mark_red(text, key))
    result = detect(text, key)
    print()
    print("Score:", round(result["score"], 3), "| Words:", result["total_words"])
    
# Print the color of each word.
def check(word_list, key):
    for word in word_list:
        color = word_color(normalize(word), key)
        print(word, "green" if color == GREEN else "red")
# For each red word in the passage, print its green synonyms from the list.
# For each red word in the passage, print its green synonyms from the list.
# For each red word in the passage, print its green synonyms from the list.
def suggest(path, key):
    with open(path, encoding="utf-8") as f:
        counts = Counter(words(f.read()))
    with open(SYNONYMS_FILE, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        word = row["word"]
        if word not in counts or word_color(word, key) == GREEN:
            continue
        greens = [c for c in row["candidates"].split("|") if word_color(c, key) == GREEN]
        print(word, "(" + str(counts[word]) + "x) ->", ", ".join(greens) or "no green synonym")
        
        
def main():
    key = read_key()
    job = sys.argv[1]
    if job == "show":
        show(sys.argv[2], key)
    elif job == "check":
        check(sys.argv[2:], key)
    elif job == "suggest":
        suggest(sys.argv[2], key)
    else:
        print("Unknown job. Use: show <file>  or  check <word> ...  or  suggest <file>")

if __name__ == "__main__":
    main()