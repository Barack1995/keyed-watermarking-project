# Demonstrations for the service (project section 5.1).
# Runs client.py as a separate program each time, like a real person,
# and saves everything to results/service_demo/demo_output.txt.

import os
import subprocess
import sys

from service import clock, ratelimit, config

OUT_DIR = "results/service_demo"
OUT_FILE = os.path.join(OUT_DIR, "demo_output.txt")
PASSAGE = "data/passages/evaluation/watermarking/E-W-01.txt"
ALICE = "secrets/alice_token.txt"
AUDRA = "secrets/audra_token.txt"
BAD = "secrets/bad_token.txt"

lines = []


# Print a line on screen and also keep it for the output file.
def say(text=""):
    print(text)
    lines.append(text)


# Run client.py as a new program and record what it prints.
def run_client(*args, show=True):
    cmd = [sys.executable, "client.py", *args]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    if show:
        say("$ python client.py " + " ".join(args))
        say(out)
    return out


# ---- Setup (referee only): clean state, fake clock, fake token ----
ratelimit.reset_counters()
if os.path.exists("service_state/log.jsonl"):
    os.remove("service_state/log.jsonl")
clock.start_fake_time(0)
with open(BAD, "w") as f:
    f.write("this-is-not-a-real-token")

say("SERVICE DEMONSTRATIONS")
say("Fake clock starts at 0 seconds. Rate limit: 20 requests per 60 seconds.")
say()

# ---- Demo 1: invalid credential is rejected ----
say("DEMO 1: invalid token is rejected")
run_client("--token-file", BAD, "--detect", PASSAGE)
say()

# ---- Demo 2: role decides what you may do ----
say("DEMO 2: submitter may detect, but may not read the log")
run_client("--token-file", ALICE, "--detect", PASSAGE)
run_client("--token-file", ALICE, "--read-log")
say()

# ---- Demo 3: rate limit still works after client restarts ----
say("DEMO 3: rate limit survives client restarts")
say("Alice already used 1 request in Demo 2. Each request below is a NEW client program.")
for i in range(19):
    run_client("--token-file", ALICE, "--detect", PASSAGE, show=False)
say("Sent 19 more requests (20 in total) with 19 separate client programs.")
say("Request 21, from yet another new client program:")
run_client("--token-file", ALICE, "--detect", PASSAGE)
say("Referee moves the fake clock forward 60 seconds. New window:")
clock.advance(60)
run_client("--token-file", ALICE, "--detect", PASSAGE)
say()

# ---- Demo 4: auditor reads the log; log holds no text, score, or token ----
say("DEMO 4: auditor may read the log")
run_client("--token-file", AUDRA, "--read-log")
say()

with open("service_state/log.jsonl", encoding="utf-8") as f:
    log_text = f.read()
with open(PASSAGE, encoding="utf-8") as f:
    passage_start = f.read()[:40]
tokens = [open(p, encoding="utf-8").read().strip() for p in (ALICE, AUDRA)]

say("Checks on the saved log file:")
say("  contains passage text? " + str(passage_start in log_text))
say("  contains a score?      " + str('"score"' in log_text))
say("  contains a token?      " + str(any(t in log_text for t in tokens)))
say()

# ---- Demo 5: binary mode hides the score everywhere ----
say("DEMO 5: binary mode shows the decision only")
say("Referee switches the service to binary mode (configuration C).")
config.set_switches(RESPONSE_MODE="binary")
answer = run_client("--token-file", ALICE, "--detect", PASSAGE)
log_view = run_client("--token-file", AUDRA, "--read-log", show=False)
with open("service_state/log.jsonl", encoding="utf-8") as f:
    log_text = f.read()
say("Checks in binary mode:")
say("  answer contains a score?         " + str('"score"' in answer))
say("  auditor's log view has a score?  " + str('"score"' in log_view))
say("  saved log file has a score?      " + str('"score"' in log_text))
config.clear_switches()
say()

# ---- Save the output and the log, then clean up ----
os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
with open(os.path.join(OUT_DIR, "log_after_demo.jsonl"), "w", encoding="utf-8") as f:
    f.write(log_text)

clock.use_real_time()
ratelimit.reset_counters()
config.clear_switches()
os.remove("service_state/log.jsonl")
os.remove(BAD)
print("Saved to", OUT_FILE)