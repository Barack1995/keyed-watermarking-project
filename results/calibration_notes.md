# Calibration notes

All numbers here come from calibration passages only.
No evaluation passage was used.

## Step 1: unmarked calibration passages

We scored the 150 unmarked calibration passages with the real key.
Results: `results/calibration_unmarked_scores.csv`

## Step 2: practice watermarking

We tried three watermarking methods on the 5 calibration passages.
Target for all three: 0.70.

| Version | Method | Stopping rule |
|---|---|---|
| v1 | manual: a person swaps red words for green synonyms with `watermark_helper.py` | target reached or 15 minutes |
| v2 | automatic: `auto_watermark.py` swaps every red word that has a green WordNet synonym or broader word | target reached or no more red words to try |
| v3 | automatic: same as v2, but skips words with 3 letters or fewer | target reached or no more red words to try |

### v1: manual

Editor: Barack. Reviewer: Sylvain (scores hidden during review).
Details: `watermarked/calibration_log.csv`

| Passage | Before | After | Minutes | Target reached | Usable |
|---|---|---|---|---|---|
| C-W-01 | 0.409 | 0.504 | 15 | no | yes |
| C-W-02 | 0.479 | 0.629 | 15 | no | yes |
| C-W-03 | 0.427 | 0.530 | 10 | no | yes |
| C-W-04 | 0.547 | 0.705 | 14 | yes | yes |
| C-W-05 | 0.407 | 0.512 | 13 | no | yes |

### v2 and v3: automatic

The professor advised us to focus on watermarking and detection, not on keeping the exact meaning, and to automate the substitution.

| Passage | Before | v2 after | v2 words changed | v3 after | v3 words changed |
|---|---|---|---|---|---|
| C-W-01 | 0.409 | 0.705 | 39 | 0.644 | 31 |
| C-W-02 | 0.479 | 0.701 | 26 | 0.675 | 23 |
| C-W-03 | 0.427 | 0.701 | 32 | 0.590 | 19 |
| C-W-04 | 0.547 | 0.703 | 20 | 0.703 | 20 |
| C-W-05 | 0.407 | 0.701 | 49 | 0.593 | 31 |
| Reached 0.70 | | 5 of 5 | | 1 of 5 | |

v2 replaced many small words with odd meanings (for example "are"
became "ar", "at" became "astatine"). v3 keeps small words, so the
text is easier to read, but it reaches the target less often.
The v2 and v3 calibration outputs were not separately quality-checked.

| Method | Reached 0.70 | Time per passage | Text |
|---|---|---|---|
| v1 manual | 1 of 5 | 10 to 15 minutes | natural |
| v2 automatic | 5 of 5 | seconds | broken |
| v3 automatic | 1 of 5 | seconds | strange in places |

**We chose v3.**

## Step 3: choosing the threshold

We tested 4 thresholds. 0.55, 0.60 and 0.65 come from the project
description. 0.51 is a rough middle point between typical unmarked
scores (just under 0.5) and the average v1 practice score (0.58).

### First test, with the v1 outputs

Results: `results/threshold_candidates.csv`

| Threshold | Unmarked flagged (of 150) | v1 outputs missed (of 5) |
|---|---|---|
| 0.51 | 27 | 1 |
| 0.55 | 5 | 3 |
| 0.60 | 1 | 3 |
| 0.65 | 1 | 4 |

### Final test, with the v3 outputs (the chosen method)

Results: `results/threshold_candidates_v3.csv` (made by `choose_threshold.py`)

| Threshold | Unmarked flagged (of 150) | v3 outputs missed (of 5) |
|---|---|---|
| 0.51 | 27 | 0 |
| 0.55 | 5 | 0 |
| 0.60 | 1 | 2 |
| 0.65 | 1 | 3 |

We chose **0.60**.

- 0.51 flags 27 normal passages (18%), which is too many.
- 0.65 flags the same number of normal passages as 0.60 (1), but
  misses more outputs (3 instead of 2).
- Between 0.55 and 0.60: 0.60 makes fewer errors in total (3 instead
  of 5) and wrongly flags fewer normal passages (1 instead of 5).
  We think wrongly flagging a normal text is the more harmful error.

## Step 4: fixed settings

Stored in `settings.py` and committed to Git before evaluation.

| Setting | Value |
|---|---|
| Key | one 32-byte random key, `secrets/key.bin` |
| Word rules | `RULES.md`, `watermark/tokenizer.py` |
| Threshold | 0.60 (flag when score > 0.60) |
| Watermarking method | `auto_watermark.py`, v3 (skip words with 3 letters or fewer) |
| Target | 0.70 |
| Stopping rule | target reached, or no more red words with a green replacement |
