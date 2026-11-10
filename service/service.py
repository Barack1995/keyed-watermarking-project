# The door: checks the person, asks the detector, and gives the answer.

from settings import RESPONSE_MODES, RESPONSE_MODE, SCORE_DIGITS
from settings import KEY_FILE, THRESHOLD
from watermark.detector import detect
from service.accounts import check_token, is_allowed
from service.ratelimit import check_rate_limit
from service.logbook import write_log, read_log


# Turn the detector's full result into the answer the person sees.
def shape_answer(result, mode=RESPONSE_MODE):
    if mode not in RESPONSE_MODES:
        raise ValueError("Unknown response mode: " + str(mode))
    if mode == "score":
        return {"outcome": "ok",
                "score": round(result["score"], SCORE_DIGITS),
                "flagged": result["flagged"]}
    return {"outcome": "ok", "flagged": result["flagged"]}


# Read the secret key (made once by make_key.py in Milestone 1).
def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()


# The door: handle one request from start to end.
def handle_request(token, action, text=None):
    # 1. Who are you?
    account, role = check_token(token)
    if account is None:
        write_log("unknown", action, "rejected: invalid credential", False, None)
        return {"outcome": "rejected: invalid credential"}

    # 2. Are you allowed?
    if not is_allowed(role, action):
        write_log(account, action, "denied: not permitted", False, None)
        return {"outcome": "denied: not permitted"}

    # 3. Too many knocks?
    allowed, remaining = check_rate_limit(account)
    if not allowed:
        write_log(account, action, "rate_limited", True, remaining)
        return {"outcome": "rate_limited"}

    # 4a. Auditor asks to read the log.
    if action == "read_log":
        lines = read_log()
        write_log(account, action, "ok", False, remaining)
        return {"outcome": "ok", "log": lines}

    # 4b. Ask the detector (Milestone 1).
    try:
        result = detect(text or "", load_key(), THRESHOLD)
    except ValueError:
        write_log(account, action, "rejected: no words", False, remaining)
        return {"outcome": "rejected: no words"}

    # 5. Shape the answer (score or decision only).
    answer = shape_answer(result)

    # 6. Write the log (no text, no score).
    write_log(account, action, "ok", False, remaining)
    return answer