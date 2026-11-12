# Service settings for the current run.
# Default: settings.py. The referee (driver) may switch them for one run
# by writing service_state/config.json. Attack code must never touch this file.

import json
import os

import settings

CONFIG_FILE = "service_state/config.json"


# Get one setting: from the switch file if it is set there, otherwise from settings.py.
def get(name):
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            switches = json.load(f)
        if name in switches:
            return switches[name]
    return getattr(settings, name)


# DRIVER ONLY: switch settings for this run, e.g. set_switches(RESPONSE_MODE="binary").
def set_switches(**values):
    os.makedirs("service_state", exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(values, f)


# DRIVER ONLY: remove all switches and go back to settings.py.
def clear_switches():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)