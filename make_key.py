
# Create the secret watermark key ONE time and save it.

import os
import secrets

KEY_FILE = "secrets/key.bin"

if os.path.exists(KEY_FILE):
    print("A key already exists. Not making a new one.")
else:
    os.makedirs("secrets", exist_ok=True)
    key = secrets.token_bytes(32)
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print("New key saved to", KEY_FILE)