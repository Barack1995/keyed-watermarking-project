# score_evaluation.py
# Evaluation step 5: score the 150 unmarked evaluation passages
# with the fixed settings, and count false positives.

import csv

from settings import THRESHOLD
from score_calibration import read_key, read_passage, PASSAGES_LIST
from watermark.detector import detect

RESULTS_FILE = "results/evaluation_unmarked_scores.csv"

# Return the rows for unmarked evaluation passages only.
def read_evaluation_unmarked():
    with open(PASSAGES_LIST, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [r for r in rows if r["set"] == "evaluation" and r["purpose"] == "unmarked"]

# Score each passage with the fixed threshold.
def score_passages(rows, key):
    results = []
    for row in rows:
        result = detect(read_passage(row), key, THRESHOLD)
        results.append({
            "passage_id": row["passage_id"],
            "length_group": row["length_group"],
            "source_id": row["source_id"],
            "score": result["score"],
            "flagged": "yes" if result["flagged"] else "no",
            "total_words": result["total_words"],
            "distinct_words": result["distinct_words"],
        })
    return results

def main():
    key = read_key()
    rows = read_evaluation_unmarked()
    results = score_passages(rows, key)

    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    flagged = sum(1 for r in results if r["flagged"] == "yes")
    print("Threshold:", THRESHOLD)
    print("False positives:", flagged, "of", len(results))
    for group in ["short", "medium", "long"]:
        in_group = [r for r in results if r["length_group"] == group]
        group_flagged = sum(1 for r in in_group if r["flagged"] == "yes")
        print(" ", group, ":", group_flagged, "flagged of", len(in_group))
    print("Saved to", RESULTS_FILE)


if __name__ == "__main__":
    main()