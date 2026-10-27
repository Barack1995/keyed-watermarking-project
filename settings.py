# Fixed settings for the experiment.
# Chosen in calibration. Do not change these during evaluation.

# Where the secret key is saved (never put the key itself here).
KEY_FILE = "secrets/key.bin"

# Detection threshold: flag a text only when its score is greater than this.
THRESHOLD = 0.60

# Watermarking method: auto_watermark.py, version v1, with a target of 70% of red words replaced by green synonyms.
# (WordNet synonyms and broader words, skip words with 3 letters or fewer).
WATERMARK_TARGET = 0.70
MIN_WORD_LENGTH = 4
STOPPING_RULE = "target reached, or no more red words with a green synonym"