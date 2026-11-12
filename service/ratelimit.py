# Rate limit: each account may make a limited number of requests per time window.
# Counters are saved in a file, so they survive a client restart.

import json
import os

from service.clock import now
from service import config  # CHANGED: settings now come through config

COUNTERS_FILE = "service_state/counters.json"


# Read all counters from the file (empty if no file yet).
def load_counters():
    if not os.path.exists(COUNTERS_FILE):
        return {}
    with open(COUNTERS_FILE) as f:
        return json.load(f)


# Save all counters to the file.
def save_counters(counters):
    os.makedirs("service_state", exist_ok=True)
    with open(COUNTERS_FILE, "w") as f:
        json.dump(counters, f)


# Is this account allowed one more request? Returns (allowed, remaining).
def check_rate_limit(account):
    # Read the current settings (switch first, then settings.py).  # NEW
    limit = config.get("RATE_LIMIT_PER_WINDOW")  # NEW
    window = config.get("RATE_LIMIT_WINDOW_SECONDS")  # NEW

    # Piece 1: limit turned off -> always allowed.
    if not config.get("RATE_LIMIT_ENABLED"):  # CHANGED
        return True, None

    # Piece 2: get this account's count and the time.
    counters = load_counters()
    t = now()
    c = counters.get(account)

    # Piece 3: never knocked, or the window passed -> fresh window.
    if c is None or t - c["window_start"] >= window:  # CHANGED
        c = {"window_start": t, "count": 0}

    # Piece 4: already at the limit -> refuse.
    if c["count"] >= limit:  # CHANGED
        counters[account] = c
        save_counters(counters)
        return False, 0

    # Piece 5: allowed -> count it, save it, say how many are left.
    c["count"] += 1
    counters[account] = c
    save_counters(counters)
    return True, limit - c["count"]  # CHANGED


# DRIVER ONLY: clear all counters before a new experiment run.
def reset_counters():
    if os.path.exists(COUNTERS_FILE):
        os.remove(COUNTERS_FILE)