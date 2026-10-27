# choose_threshold.py
# Calibration step 3: count errors for each candidate threshold.

import csv

from watermark_helper import read_key
from watermark.detector import detect

CANDIDATES = [0.51, 0.55, 0.60, 0.65]

UNMARKED_SCORES = "results/calibration_unmarked_scores.csv" 
PRACTICE_FILES = [
    "watermarked/calibration/C-W-01_v3.txt",
    "watermarked/calibration/C-W-02_v3.txt",
    "watermarked/calibration/C-W-03_v3.txt",
    "watermarked/calibration/C-W-04_v3.txt",
    "watermarked/calibration/C-W-05_v3.txt",
]
# RESULTS_FILE = "results/threshold_candidates.csv"
RESULTS_FILE = "results/threshold_candidates_v3.csv"

# Read the scores of the 150 unmarked calibration passages.
def read_unmarked_scores():
    with open(UNMARKED_SCORES, encoding="utf-8") as f:
        return [float(row["score"]) for row in csv.DictReader(f)]
    
# Score the 5 edited practice passages with the real key.
def score_practice(key):
    scores = []
    for path in PRACTICE_FILES:
        with open(path, encoding="utf-8") as f:
            scores.append(detect(f.read(), key)["score"])
    return scores

# Count errors for one threshold.
def count_errors(threshold, unmarked, practice):
    false_positives = sum(1 for s in unmarked if s > threshold)
    misses = sum(1 for s in practice if s <= threshold)
    return false_positives, misses

def main():
    key = read_key()
    unmarked = read_unmarked_scores()
    practice = score_practice(key)
    print("Practice scores:", [round(s, 3) for s in practice])
    print()
    print("threshold | wrongly flagged (of 150) | missed (of 5)")
    rows = []
    for t in CANDIDATES:
        fp, missed = count_errors(t, unmarked, practice)
        print(f"   {t:.2f}   |          {fp:3d}             |      {missed}")
        rows.append({"threshold": t, "unmarked_flagged": fp, "unmarked_total": len(unmarked),
                        "practice_unflagged": missed, "practice_total": len(practice)})
    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print()
    print("Saved to", RESULTS_FILE)


if __name__ == "__main__":
    main() 