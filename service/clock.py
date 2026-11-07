# What time is it now?
# Normal use: real time. Experiments: fake time, moved only by the driver.

import json
import os
import time

CLOCK_FILE = "service_state/clock.json"


# Return the current time in seconds.
def now():
    if os.path.exists(CLOCK_FILE):
        with open(CLOCK_FILE) as f:
            return json.load(f)["now"]
    return time.time()


# DRIVER ONLY: switch to fake time, starting at a chosen number of seconds.
def start_fake_time(start=0):
    os.makedirs("service_state", exist_ok=True)
    with open(CLOCK_FILE, "w") as f:
        json.dump({"now": start}, f)


# DRIVER ONLY: move the fake clock forward by some seconds.
def advance(seconds):
    current = now()
    with open(CLOCK_FILE, "w") as f:
        json.dump({"now": current + seconds}, f)


# DRIVER ONLY: stop using fake time and go back to real time.
def use_real_time():
    if os.path.exists(CLOCK_FILE):
        os.remove(CLOCK_FILE)