# Command-line client: the only way a person (or attacker) talks to the service.
# It sends a token + a request to the door and prints the answer.

import argparse
import json

from service.service import handle_request

# The options a person can type.
parser = argparse.ArgumentParser(description="Talk to the watermark detection service.")
parser.add_argument("--token-file", required=True, help="file that holds your access token")
action = parser.add_mutually_exclusive_group(required=True)
action.add_argument("--detect", metavar="TEXT_FILE", help="check a text file for the watermark")
action.add_argument("--read-log", action="store_true", help="read the request log (auditors only)")
args = parser.parse_args()

# Read the token from its file (strip removes spaces and line breaks).
with open(args.token_file, encoding="utf-8") as f:
    token = f.read().strip()

# Send the request through the door.
if args.detect:
    with open(args.detect, encoding="utf-8") as f:
        answer = handle_request(token, "detect", f.read())
else:
    answer = handle_request(token, "read_log")

# Show the answer.
print(json.dumps(answer, indent=2))