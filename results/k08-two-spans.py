"""H-17 K08 source-clause recombination diagnostic.

Tests all ordered pairs of contiguous normalized word spans taken from
different Emily draft/description notes, with six fixed join patterns.
These constructed phrases are hypotheses, not independently authenticated.
No writes, network calls, or facility access.
"""
from __future__ import annotations

import hashlib
import hmac
import itertools
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "resources"
SOURCE = {
    "N02": "A good watch leaves the room ready for the next pair of hands",
    "N06": "The little lamp stays on until the corridor has gone quiet",
    "N10": "The desk copy was meant to sound like us not like a quarterly report I kept going back to the photograph after the last cup",
    "N13": "At the end of the night the mugs stood beside the window and somebody had remembered to leave the little lamp on",
    "N20": "I wanted the line to hold the sea the end of the night and the voices at the table",
}
JOINERS = (" ", " and ", " while ", " as ", " when ", " until ")


def main() -> None:
    routing = json.loads((ROOT / "evidence/recovery-routing.json").read_text(encoding="utf-8"))
    inventory = json.loads((ROOT / "acceptance.json").read_text(encoding="utf-8"))
    key = bytes.fromhex(routing["K08"]["desk_nonce"])
    target = inventory["slot_sha256"]["K08"]
    spans = []
    for note, text in SOURCE.items():
        words = re.findall(r"[a-z0-9]+", text.lower())
        spans.extend(
            (note, " ".join(words[i:j]))
            for i in range(len(words))
            for j in range(i + 1, len(words) + 1)
        )
    count = 0
    for left, right in itertools.product(spans, repeat=2):
        if left[0] == right[0]:
            continue
        for joiner in JOINERS:
            caption = left[1] + joiner + right[1]
            slot = hmac.new(key, caption.encode("utf-8"), hashlib.sha256).digest()[:16]
            count += 1
            if hashlib.sha256(slot).hexdigest() == target:
                print(f"FOUND: {left[0]} + {right[0]} {caption!r} K08={slot.hex().upper()}")
                return
    print(f"NO_MATCH: {len(spans)} spans, {count} candidate phrases")


if __name__ == "__main__":
    main()
