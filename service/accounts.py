# Who are you, and what are you allowed to do?
# Checks a token against the saved accounts.

import json
import hmac

ACCOUNTS_FILE = "secrets/accounts.json"

# What each role is allowed to do.
PERMISSIONS = {
    "submitter": {"detect"},
    "auditor": {"detect", "read_log"},
}

# Read all accounts from the secrets file.
def load_accounts():
    with open(ACCOUNTS_FILE) as f:
        return json.load(f)

# Find who owns this token. Returns (account, role), or (None, None) if unknown.
def check_token(token):
    for saved_token, info in load_accounts().items():
        if hmac.compare_digest(saved_token, token):
            return info["account"], info["role"]
    return None, None

# Is this role allowed to do this action? Returns True or False.
def is_allowed(role, action):
    return action in PERMISSIONS.get(role, set())