
# Cut the source books into passages and split them into calibration and evaluation sets.

import csv
import random
import os
from watermark.tokenizer import words

# Where the files are.
SOURCES_FOLDER = "data/sources"
SOURCES_LIST = "data/sources/sources_list.csv"
PASSAGES_FOLDER = "data/passages"

# Numbers from the project description.
LENGTH_GROUPS = {
    "short": (30, 99),
    "medium": (100, 199),
    "long": (200, 400),
}
UNMARKED_PER_SET = 150
MIN_PER_GROUP = 30
WATERMARK_COUNT = {"calibration": 5, "evaluation": 10}
WATERMARK_RANGE = (100, 200)
ATTACK3_COUNT = 5
MIN_PARAGRAPH_WORDS = 8
SEED = 2026               #fixed number so the random choice can be repeated
# read the list of books.
def read_book_list():
    
    with open(SOURCES_LIST, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

# Read a book and open one book and keep only the story.
def read_story(book):
    path = SOURCES_FOLDER + "/" + book["file_name"]
    with open(path, encoding="utf-8-sig") as f:
        text = f.read()

    start = text.find("*** START OF")
    end = text.find("*** END OF")
    if start == -1 or end == -1:
        raise ValueError("Start or end line not found in " + path)

    start = text.find("\n", start) + 1
    return text[start:end]
# split the story into paragraphs.
# A paragraph is a group of lines with an empty line before and after it.
def split_paragraphs(story):
    paragraphs = []
    current = []
    for line in story.splitlines():
        if line.strip():
            current.append(line.strip())
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return paragraphs

# decide if a paragraph is real prose.
def is_prose(paragraph):
    if paragraph.startswith("["):
        return False
    if len(words(paragraph)) < MIN_PARAGRAPH_WORDS:
        return False

    letters = [c for c in paragraph if c.isalpha()]
    capitals = [c for c in letters if c.isupper()]
    if len(capitals) > len(letters) / 2:
        return False

    if not paragraph.endswith((".", "!", "?", '"', "'", "”", "’")):
        return False

    return True

# join whole paragraphs into passages of the right length.
def make_passages(paragraphs):
    passages = []
    targets = ["short", "medium", "long"]
    t = 0
    current = []
    current_words = 0

    for paragraph in paragraphs:
        n = len(words(paragraph))
        low, high = LENGTH_GROUPS[targets[t]]

        if current_words + n > high:
            current = []
            current_words = 0
            if n > high:
                continue

        current.append(paragraph)
        current_words += n

        if current_words >= low:
            passages.append("\n\n".join(current))
            current = []
            current_words = 0
            t = (t + 1) % 3

    return passages
# find the length group for a word count.
def length_group(total):
    for name, (low, high) in LENGTH_GROUPS.items():
        if low <= total <= high:
            return name
    return None


# Piece 5B: measure a passage.
def measure(passage):
    passage_words = words(passage)
    total = len(passage_words)
    return {
        "text": passage,
        "total_words": total,
        "distinct_words": len(set(passage_words)),
        "group": length_group(total),
    }
    
# cut every book and collect all passages, grouped by set.
def collect_all_passages(books):
    collected = {"calibration": [], "evaluation": []}
    for book in books:
        set_name = book["set"].strip().lower()
        story = read_story(book)
        prose = [p for p in split_paragraphs(story) if is_prose(p)]
        for passage in make_passages(prose):
            info = measure(passage)
            info["book"] = book
            collected[set_name].append(info)
    return collected

# choose the passages to keep for one set.
def choose_passages(passages, set_name):
    pool = list(passages)
    random.Random(SEED).shuffle(pool)

    low, high = WATERMARK_RANGE
    watermark = [p for p in pool if low <= p["total_words"] <= high]
    watermark = watermark[:WATERMARK_COUNT[set_name]]

    unmarked = []
    per_group = UNMARKED_PER_SET // len(LENGTH_GROUPS)
    for group in LENGTH_GROUPS:
        in_group = [p for p in pool if p["group"] == group and p not in watermark]
        unmarked += in_group[:per_group]

    return watermark, unmarked


# give each chosen passage an ID, and mark 5 for Attack 3.
# The method: the evaluation watermarking passages with the lowest IDs.
def label_passages(set_name, watermark, unmarked):
    prefix = set_name[0].upper()
    labeled = []

    for i, p in enumerate(unmarked, start=1):
        p["id"] = f"{prefix}-U-{i:03d}"
        p["set"] = set_name
        p["purpose"] = "unmarked"
        p["attack3"] = "no"
        labeled.append(p)

    for i, p in enumerate(watermark, start=1):
        p["id"] = f"{prefix}-W-{i:02d}"
        p["set"] = set_name
        p["purpose"] = "watermarking"
        if set_name == "evaluation" and i <= ATTACK3_COUNT:
            p["attack3"] = "yes"
        else:
            p["attack3"] = "no"
        labeled.append(p)

    return labeled

# Piece 8A: save each passage as a text file, and write passages.csv.
def save_passages(passages):
    rows = []
    for p in passages:
        folder = PASSAGES_FOLDER + "/" + p["set"] + "/" + p["purpose"]
        os.makedirs(folder, exist_ok=True)
        with open(folder + "/" + p["id"] + ".txt", "w", encoding="utf-8") as f:
            f.write(p["text"] + "\n")

        rows.append({
            "passage_id": p["id"],
            "set": p["set"],
            "purpose": p["purpose"],
            "attack3": p["attack3"],
            "length_group": p["group"],
            "total_words": p["total_words"],
            "distinct_words": p["distinct_words"],
            "source_id": p["book"]["source_id"],
            "title": p["book"]["title"],
            "author": p["book"]["author"],
            "link": p["book"]["link"],
        })

    with open(PASSAGES_FOLDER + "/passages.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
#write summary.txt with counts, checks, and methods.
def write_summary(books, chosen):
    used = {p["book"]["source_id"] for p in chosen}
    lines = [
        "Source documents listed: " + str(len(books)),
        "Source documents used: " + str(len(used)),
        "Random seed: " + str(SEED),
        "Attack 3 method: the " + str(ATTACK3_COUNT) + " evaluation watermarking "
        "passages with the lowest IDs, chosen before any scoring.",
        "",
    ]
    problems = []

    for set_name in ["calibration", "evaluation"]:
        in_set = [p for p in chosen if p["set"] == set_name]
        unmarked = [p for p in in_set if p["purpose"] == "unmarked"]
        watermark = [p for p in in_set if p["purpose"] == "watermarking"]
        lines.append(set_name.upper())

        for group in LENGTH_GROUPS:
            count = sum(1 for p in unmarked if p["group"] == group)
            lines.append("  unmarked " + group + ": " + str(count))
            if count < MIN_PER_GROUP:
                problems.append("PROBLEM: " + set_name + " has only " + str(count) + " " + group)

        lines.append("  unmarked total: " + str(len(unmarked)))
        lines.append("  watermarking: " + str(len(watermark)))
        if len(unmarked) != UNMARKED_PER_SET:
            problems.append("PROBLEM: " + set_name + " has " + str(len(unmarked)) + " unmarked")
        if len(watermark) != WATERMARK_COUNT[set_name]:
            problems.append("PROBLEM: " + set_name + " has " + str(len(watermark)) + " watermarking")

        lines.append("  passages per source:")
        for book in books:
            k = sum(1 for p in in_set if p["book"]["source_id"] == book["source_id"])
            if k > 0:
                lines.append("    " + book["source_id"] + " " + book["title"] + ": " + str(k))
        lines.append("")

    lines += problems or ["All checks passed."]
    text = "\n".join(lines)
    with open(PASSAGES_FOLDER + "/summary.txt", "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(text)
    
# run all the pieces in order.
def main():
    books = read_book_list()
    collected = collect_all_passages(books)
    chosen = []
    for set_name in ["calibration", "evaluation"]:
        watermark, unmarked = choose_passages(collected[set_name], set_name)
        chosen += label_passages(set_name, watermark, unmarked)
    save_passages(chosen)
    write_summary(books, chosen)


if __name__ == "__main__":
    main()

