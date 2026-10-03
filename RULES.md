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

## Important

These rules must not change after the passages are split into
calibration and evaluation sets. A change would alter word counts and
length groups, and the passages would have to be cut again.
