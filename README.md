# Keyed Text Watermarking: Detection, Attacks, and Policy

This project has a detector, a small detection service, some attacks, and a policy. It is a team project for the Data Security and Privacy class, Fall 2026.

## Team
- Person A: Barack NIYONKURU - word rules, detector, service
- Person B: Sylvain NDAYISHIMIYE - passages, measurements, Attacks 1-2
- Person C: Raiyan ASHRAF - threat model, Attack 3, policy memo

## How to run
(We will add this later.)

To make the passages again, run:

    python make_passages.py

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
