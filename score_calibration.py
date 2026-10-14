# Calibration step 1: score the 150 unmarked calibration passages.

import csv
import os

from settings import KEY_FILE
from watermark.detector import detect

PASSAGES_FOLDER = "data/passages"
PASSAGES_LIST = "data/passages/passages.csv"
RESULTS_FILE = "results/calibration_unmarked_scores.csv"

# Read the secret key from its file.
def read_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()
    
# Return the rows for unmarked calibration passages only.
# Return the rows for unmarked calibration passages only.
def read_calibration_unmarked():
    with open(PASSAGES_LIST, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [r for r in rows if r["set"] == "calibration" and r["purpose"] == "unmarked"]

# Read the text of one passage.
def read_passage(row):
    path = os.path.join(PASSAGES_FOLDER, row["set"], row["purpose"], row["passage_id"] + ".txt")
    with open(path, encoding="utf-8") as f:
        return f.read()
    
# Score each passage and keep the results.
def score_passages(rows, key):
    results = []
    for row in rows:
        result = detect(read_passage(row), key)
        results.append({
            "passage_id": row["passage_id"],
            "length_group": row["length_group"],
            "source_id": row["source_id"],
            "score": result["score"],
            "total_words": result["total_words"],
            "distinct_words": result["distinct_words"],
        })
    return results


# Save the results to a CSV file.
def save_results(results):
    os.makedirs("results", exist_ok=True)
    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        
def main():
    key = read_key()
    rows = read_calibration_unmarked()
    results = score_passages(rows, key)
    save_results(results)
    print("Scored", len(results), "passages. Saved to", RESULTS_FILE)


if __name__ == "__main__":
    main()