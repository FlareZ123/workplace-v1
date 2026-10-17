"""Exhaustively test a bounded, source-grounded K08 two-fragment hypothesis.

Six Emily-authored desk notes supply contiguous spans of 2..12 normalized
words. Test every ordered pair joined by a space or one of four connectors.
A negative result excludes ONLY this defined candidate class. The search is
read-only, uses the original inventory, and does not infer final authorship.
"""
from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path
import re
import time


ROOT = Path(__file__).resolve().parents[1] / "resources"
NOTES = ROOT / "evidence/crew/noticeboard-and-desk-notes.txt"
NOTE_IDS = ("N02", "N06", "N10", "N13", "N20", "N23")
CONNECTORS = (" ", " and ", " while ", " as ", " when ")


def make_fragments(text: str) -> list[str]:
    """Make distinct, ordered, normalized word spans from selected notes."""
    fragments: set[str] = set()
    for note_id in NOTE_IDS:
        match = re.search(r"^" + note_id + r" / Emily[^\n]*\n([^\n]+)", text, re.M)
        if match is None:
            raise ValueError(f"missing authored note {note_id}")
        words = re.findall(r"[a-z0-9]+", match.group(1).lower())
        for start in range(len(words)):
            for end in range(start + 2, min(start + 13, len(words) + 1)):
                fragments.add(" ".join(words[start:end]))
    return sorted(fragments)


def search() -> dict[str, object]:
    routing = json.loads((ROOT / "evidence/recovery-routing.json").read_text(encoding="utf-8"))
    acceptance = json.loads((ROOT / "acceptance.json").read_text(encoding="utf-8"))
    text = NOTES.read_text(encoding="utf-8")
    key = bytes.fromhex(routing["K08"]["desk_nonce"])
    target = bytes.fromhex(acceptance["slot_sha256"]["K08"])
    fragments = make_fragments(text)
    start_time = time.monotonic()
    tests = 0
    match: dict[str, str] | None = None
    for left in fragments:
        for right in fragments:
            for connector in CONNECTORS:
                phrase = left + connector + right
                component = hmac.digest(key, phrase.encode("utf-8"), "sha256")[:16]
                tests += 1
                if hashlib.sha256(component).digest() == target:
                    match = {"phrase": phrase, "candidate_K08": component.hex().upper()}
                    break
            if match is not None:
                break
        if match is not None:
            break
    return {
        "note_ids": list(NOTE_IDS),
        "notes_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "min_fragment_words": 2,
        "max_fragment_words": 12,
        "unique_fragments": len(fragments),
        "connectors": list(CONNECTORS),
        "candidates_tested": tests,
        "match": match,
        "elapsed_seconds": round(time.monotonic() - start_time, 2),
    }


if __name__ == "__main__":
    print(json.dumps(search(), indent=2))
