# Create the service accounts ONE time and save them.
# Each account gets a random secret token and a role.

import os
import json
import secrets

ACCOUNTS_FILE = "secrets/accounts.json"

# Our demonstration accounts: name and role.
ACCOUNTS = [
    ("alice", "submitter"),
    ("audra", "auditor"),
]

if os.path.exists(ACCOUNTS_FILE):
    print("Accounts already exist. Not making new ones.")
else:
    os.makedirs("secrets", exist_ok=True)
    accounts = {}
    for name, role in ACCOUNTS:
        token = secrets.token_hex(16)
        accounts[token] = {"account": name, "role": role}
        print("Created account:", name, "(" + role + ")")
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)
    print("Accounts saved to", ACCOUNTS_FILE)