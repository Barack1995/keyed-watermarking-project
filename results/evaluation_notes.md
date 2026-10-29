# Evaluation notes

All settings were fixed in calibration and not changed during evaluation
(see `settings.py`).

## Fixed settings

| Setting | Value |
|---|---|
| Threshold | 0.60 (flag only when score > 0.60) |
| Watermarking method | `auto_watermark.py`, method v3 (WordNet synonyms and broader words, skip words with 3 letters or fewer) |
| Watermarking target | 0.70 |
| Stopping rule | target reached, or no more red words with a green synonym |

## Main results

| Measurement | Calculation | Result |
|---|---|---|
| Unmarked false-positive rate | flagged unmarked evaluation passages / 150 | 1 / 150 = 0.7% |
| Detection rate on watermarking outputs | flagged outputs / 10 | 10 / 10 = 100% |
| Usable watermarking success rate | flagged and pass quality check / 10 | 0 / 10 = 0% |

Files: `results/evaluation_unmarked_scores.csv`,
`watermarked/auto_log_evaluation_v3.csv`,
`watermarked/evaluation_quality_review.csv`

## Unmarked passages by length group

| Length group | Words | Flagged | Tested |
|---|---|---|---|
| short | 30-99 | 1 | 50 |
| medium | 100-199 | 0 | 50 |
| long | 200-400 | 0 | 50 |
| total | | 1 | 150 |

The only false positive is a short passage. Short passages have fewer
words, so their scores vary more by chance.

## Watermarked passages

| Passage | Score before | Score after | Words changed | Flagged | Target reached |
|---|---|---|---|---|---|
| E-W-01 | 0.562 | 0.657 | 10 | yes | no |
| E-W-02 | 0.556 | 0.692 | 18 | yes | no |
| E-W-03 | 0.438 | 0.654 | 40 | yes | no |
| E-W-04 | 0.489 | 0.610 | 17 | yes | no |
| E-W-05 | 0.441 | 0.661 | 26 | yes | no |
| E-W-06 | 0.490 | 0.702 | 22 | yes | yes |
| E-W-07 | 0.469 | 0.667 | 32 | yes | no |
| E-W-08 | 0.500 | 0.660 | 17 | yes | no |
| E-W-09 | 0.504 | 0.658 | 18 | yes | no |
| E-W-10 | 0.450 | 0.661 | 23 | yes | no |

Words changed = number of word occurrences replaced by the script.

## Quality check

| Item | Result |
|---|---|
| Reviewer | Sylvain (did not make the outputs; scores hidden during review) |
| Meaning preserved | no, for all 10 |
| Readable | yes, for all 10 |
| Usable (both yes) | 0 of 10 |

Following the professor's guidance, our focus was watermarking and
detection, not keeping the exact meaning. The automatic method always
produced flagged text, but it changed the meaning.

## Repetition

### Most repetitive real passage: E-U-124

331 total words, 165 distinct words (ratio 0.50), score 0.547.

| Word | Times | Color |
|---|---|---|
| the | 15 | green |
| was | 13 | red |
| he | 13 | green |
| and | 12 | red |
| to | 11 | red |
| that | 7 | green |
| i | 7 | green |
| it | 6 | red |
| of | 6 | red |
| me | 6 | red |
| total | 96 | 42 green, 54 red |

These 10 words fill 96 of 331 word positions (29%). If "the" were red
instead of green, the score would drop by about 15 / 331 = 0.045.

### Extreme example: one word repeated

| Text | Total words | Distinct words | Score | Flagged |
|---|---|---|---|---|
| "the" x 1000 | 1000 | 1 | 1.0 | yes |
| "was" x 1000 | 1000 | 1 | 0.0 | no |

A long text is not automatically reliable. The score depends on how
many different words the text has, not only on its length.

## Small samples

| Measurement | Observed | Passages tested | 95% upper limit | How |
|---|---|---|---|---|
| False positives | 1 (0.7%) | 150 | about 3.2% | with 1 error: about 4.74 / 150 |
| Missed watermarks | 0 (0%) | 10 | about 30% | with 0 errors: 3 / 10 |

| Limit | Effect |
|---|---|
| The 150 unmarked evaluation passages come from only 4 books | Passages from the same book share words and style, so results are not fully independent. The real uncertainty is probably larger. |
