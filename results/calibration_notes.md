# Calibration notes

All numbers here come from calibration passages only.
No evaluation passage was used.

## Step 1: unmarked calibration passages

We scored the 150 unmarked calibration passages with the real key.
Results: `results/calibration_unmarked_scores.csv`

## Step 2: practice watermarking

Editor: Barack. Reviewer: Sylvain (scores hidden during review).
Target: 0.70. Stopping rule: stop at the target or after 15 minutes.
Details: `watermarked/calibration_log.csv`

| Passage | Before | After | Minutes | Target reached | Usable |
|---|---|---|---|---|---|
| C-W-01 | 0.409 | 0.504 | 15 | no | yes |
| C-W-02 | 0.479 | 0.629 | 15 | no | yes |
| C-W-03 | 0.427 | 0.530 | 10 | no | yes |
| C-W-04 | 0.547 | 0.705 | 14 | yes | yes |
| C-W-05 | 0.407 | 0.512 | 13 | no | yes |

## Step 3: choosing the threshold

We tested 4 thresholds. 0.55, 0.60 and 0.65 come from the project
description. 0.51 is the middle point between the average unmarked
score (about 0.45) and the average practice score (about 0.58).

Results: `results/threshold_candidates.csv` (made by `choose_threshold.py`)

| Threshold | Unmarked flagged (of 150) | Practice outputs missed (of 5) |
|---|---|---|
| 0.51 | 27 | 1 |
| 0.55 | 5 | 3 |
| 0.60 | 1 | 3 |
| 0.65 | 1 | 4 |

We chose **0.60**.

- 0.51 flags 27 normal passages (18%), which is too many.
- 0.55 and 0.60 miss the same number of outputs (3), but 0.60 flags
  fewer normal passages (1 instead of 5).
- 0.65 flags the same number of normal passages as 0.60 (1), but
  misses more outputs (4 instead of 3).
