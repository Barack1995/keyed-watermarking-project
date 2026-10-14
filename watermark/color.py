# Give each word a color using the secret key.

import hmac

GREEN = 1

# Return 1 (green) or 0 (red) for one word.
def word_color(word, key):
    return hmac.digest(key, word.encode("utf-8"), "sha256")[-1] & 1