# Word Rules (Tokenization and Normalization)

These rules decide what counts as a word and how each word is written
before it gets a color. The SAME rules are used for counting passage
lengths, watermarking, and detection. The code is in
`watermark/tokenizer.py`.

## Rules

1. **What is a word:** a run of letters. Numbers, underscores, and
   punctuation are not part of words.
2. **Unicode:** the whole text is normalized with Unicode NFC before
   splitting, so a letter like "e" with an accent is always stored the
   same way.
3. **Case:** every word is lowercased.
4. **Hyphens and apostrophes split words.**

## Examples

| Text | Words |
|---|---|
| `Book, BOOK and book!` | book, book, and, book |
| `well-known` | well, known |
| `don't` | don, t |
| `In 1813` | in |
| `_very_` (Gutenberg italics) | very |
| `cafe` with an accent | one word, always the same form |

## Counting

- **Total words:** every word, counted each time it appears.
- **Distinct words:** each different word counted once.
- Example: `the cat and the dog` = 5 total, 4 distinct.

## Scoring

The detector is in `watermark/detector.py`.

1. Split the text into words with the rules above.
2. Give each word a color with the secret key (`watermark/color.py`).
   1 means green, 0 means red.
3. Score = green words / total words.
   Repeated words count every time.
4. The text is flagged only when the score is **greater than** the threshold.
   A score equal to the threshold is not flagged.

Example: 65 green words out of 100 words gives a score of 0.65.
With a threshold of 0.60, the text is flagged.

The detector also returns the total and distinct word counts.

## Empty input

If the text has no words (for example `123 !!`), the detector does not
give a score. It stops with this error:

    ValueError: Empty input: the text has no words to score.

## Threshold

The threshold is not chosen yet. We will choose it in calibration and
save it in `settings.py`. It will not change during evaluation.

## Important

These rules must not change after the passages are split into
calibration and evaluation sets. A change would alter word counts and
length groups, and the passages would have to be cut again.
