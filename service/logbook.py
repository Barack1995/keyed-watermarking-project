# The log: one line for every request.
# Never stores the text, the score, or the token.

import json
import os

from service.clock import now

LOG_FILE = "service_state/log.jsonl"


# Add one line to the log. Only metadata: no text, no score, no token.
def write_log(account, action, outcome, rate_limited, remaining):
    os.makedirs("service_state", exist_ok=True)
    line = {
        "account": account,
        "time": now(),
        "action": action,
        "outcome": outcome,
        "rate_limited": rate_limited,
        "remaining": remaining,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(line) + "\n")


# Return all log lines as a list (used by auditors only).
def read_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE) as f:
        return [json.loads(line) for line in f if line.strip()]