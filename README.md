# Keyed Text Watermarking: Detection, Attacks, and Policy

This project has a detector, a small detection service, some attacks, and a policy. It is a team project for the Data Security and Privacy class, Fall 2026.

## Team
- Person A: Barack NIYONKURU - word rules, detector, service
- Person B: Sylvain NDAYISHIMIYE - passages, measurements, Attacks 1-2
- Person C: Raiyan ASHRAF - threat model, Attack 3, policy memo

## How to run

Run every command from the project folder.

### 1. Setup (one time)

You need Python 3 (we used 3.13). Install NLTK and download WordNet:

    pip install nltk
    python -c "import nltk; nltk.download('wordnet')"

### 2. Make the passages

    python make_passages.py

This cuts the books in `data/sources/` into passages and saves them in
`data/passages/`, with `passages.csv` and `summary.txt`.

### 3. Make the secret key (one time)

    python make_key.py

This saves a random 32-byte key in `secrets/key.bin`. It never overwrites
an existing key. The `secrets/` folder is not in Git, so a new copy of the
project gets a new key, and its scores will be different from ours.

### 4. Calibration

    python score_calibration.py
    python auto_watermark.py
    python choose_threshold.py

- `score_calibration.py` scores the 150 unmarked calibration passages
  (`results/calibration_unmarked_scores.csv`).
- `auto_watermark.py` watermarks the 5 calibration passages
  (`watermarked/calibration/`). The settings at the top of the file say
  which passages it uses and which version it makes.
- `choose_threshold.py` counts errors for each candidate threshold
  (`results/threshold_candidates_v3.csv`).

The fixed settings (threshold, target, method) are in `settings.py`.

### 5. Evaluation

    python score_evaluation.py
    python auto_watermark.py

- `score_evaluation.py` scores the 150 unmarked evaluation passages with
  the fixed threshold (`results/evaluation_unmarked_scores.csv`).
- `auto_watermark.py`, with its settings set to the evaluation passages,
  watermarks the 10 evaluation passages (`watermarked/evaluation/`).

### Helper tool

`watermark_helper.py` was used for manual watermarking (version v1):

    python watermark_helper.py show <file>
    python watermark_helper.py check <word> <word> ...
    python watermark_helper.py suggest <file>

`watermark_helper.py` and `auto_watermark.py` use the secret key. They
must never be used for query-access attacks.

### Results

Notes on calibration and evaluation, with all results in tables:
`results/calibration_notes.md` and `results/evaluation_notes.md`.

## Data sources

We took all passages from 8 free (public domain) books on Project Gutenberg.
We downloaded each book as "Plain Text UTF-8".

Number of books: 8

| ID | Book | Author | Link | Set |
|---|---|---|---|---|
| S01 | Pride and Prejudice | Jane Austen | https://www.gutenberg.org/ebooks/1342 | calibration |
| S03 | Dracula | Bram Stoker | https://www.gutenberg.org/ebooks/345 | calibration |
| S05 | Little Women | Louisa May Alcott | https://www.gutenberg.org/ebooks/514 | calibration |
| S07 | The Time Machine | H. G. Wells | https://www.gutenberg.org/ebooks/35 | calibration |
| S02 | Alice's Adventures in Wonderland | Lewis Carroll | https://www.gutenberg.org/ebooks/11 | evaluation |
| S04 | Frankenstein | Mary Shelley | https://www.gutenberg.org/ebooks/84 | evaluation |
| S06 | The Adventures of Sherlock Holmes | Arthur Conan Doyle | https://www.gutenberg.org/ebooks/1661 | evaluation |
| S08 | The Adventures of Tom Sawyer | Mark Twain | https://www.gutenberg.org/ebooks/74 | evaluation |

All passages from one book are in the same set.

Where to find more details:
- The list of books: `data/sources/sources_list.csv`
- Each passage and its book: `data/passages/passages.csv`
- How many passages came from each book, and how we chose the 5 passages for Attack 3: `data/passages/summary.txt`

## Contribution statement
(Each member will write what they did, with links to their commits.)

