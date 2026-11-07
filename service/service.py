# The door: checks the person, asks the detector, and gives the answer.

from settings import RESPONSE_MODES, RESPONSE_MODE, SCORE_DIGITS


# Turn the detector's full result into the answer the person sees.
def shape_answer(result, mode=RESPONSE_MODE):
    if mode not in RESPONSE_MODES:
        raise ValueError("Unknown response mode: " + str(mode))
    if mode == "score":
        return {"outcome": "ok",
                "score": round(result["score"], SCORE_DIGITS),
                "flagged": result["flagged"]}
    return {"outcome": "ok", "flagged": result["flagged"]}