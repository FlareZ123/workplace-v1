"""Read-only, bounded K08 recovery hypothesis: three anchored desk-note fragments.

The keeper's surviving email names hospitality after a watch, the end of
night, and water/voices at the table. This tests one hypothesis, not a
claim of actual final wording: an exact contiguous 2..8-word fragment from
N02 (watch/room/hands), N13 (night/mugs/window/lamp) and N20 (sea/voices/
table), each present once in any order, separated by one of three joiners.
The text is normalized according to the original route before checking the
unchanged HMAC/slot-SHA256 commitment. The final caption has no authenticated
verbatim transcription in the supplied export.
"""
from __future__ import annotations

import hashlib
import hmac
import itertools
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / "resources" if (BASE / "resources").exists() else BASE
NOTES = ROOT / "evidence/crew/noticeboard-and-desk-notes.txt"
JOINERS = (" ", " and ", " while ")
ANCHORS = {"N02": ("watch", "room", "hands"),
           "N13": ("night", "mugs", "window", "lamp"),
           "N20": ("sea", "voices", "table")}


def source_words(text: str, note_id: str) -> list[str]:
    match = re.search(r"^" + note_id + r" / [^\n]+\n([^\n]+)", text, re.M)
    if not match:
        raise ValueError(f"Missing source {note_id}")
    phrase = match.group(1)
    if note_id == "N02":
        phrase = phrase.split(":", 1)[1]
    if note_id == "N20":
        phrase = phrase.split(".", 1)[0]
    return re.findall(r"[a-z0-9]+", phrase.lower())


def fragments(words: list[str], anchors: tuple[str, ...]) -> list[str]:
    all_fragments = set()
    for start in range(len(words)):
        for end in range(start + 2, min(start + 9, len(words) + 1)):
            piece = words[start:end]
            if any(anchor in piece for anchor in anchors):
                all_fragments.add(" ".join(piece))
    return sorted(all_fragments)


def main() -> None:
    original = NOTES.read_bytes()
    text = original.decode("utf-8")
    route = json.loads((ROOT / "evidence/recovery-routing.json").read_text())
    acceptance = json.loads((ROOT / "acceptance.json").read_text())
    nonce = bytes.fromhex(route["K08"]["desk_nonce"])
    target = bytes.fromhex(acceptance["slot_sha256"]["K08"])
    frag = {key: fragments(source_words(text, key), anchors)
            for key, anchors in ANCHORS.items()}
    # Independently confirmed: exact N02 first draft does not match.
    control = "a good watch leaves the room ready for the next pair of hands"
    control_hex = hmac.digest(nonce, control.encode(), "sha256")[:16].hex().upper()
    assert control_hex == "BF889359B0303F2B2B2FD96AE841210B"
    padded_nonce = nonce.ljust(64, b"\x00")
    inner_base = hashlib.sha256(bytes(b ^ 0x36 for b in padded_nonce))
    outer_base = hashlib.sha256(bytes(b ^ 0x5c for b in padded_nonce))
    tested = 0
    for order in itertools.permutations(ANCHORS):
        first, second, third = (frag[name] for name in order)
        joiners_bytes = tuple(s.encode("utf-8") for s in JOINERS)
        for a, b, c in itertools.product(first, second, third):
            ab, bb, cb = a.encode(), b.encode(), c.encode()
            for j1, j2 in itertools.product(joiners_bytes, repeat=2):
                phrase_bytes = ab + j1 + bb + j2 + cb
                inner = inner_base.copy()
                inner.update(phrase_bytes)
                outer = outer_base.copy()
                outer.update(inner.digest())
                slot = outer.digest()[:16]
                tested += 1
                if hashlib.sha256(slot).digest() == target:
                    print(json.dumps({"result": "PASS", "phrase": phrase_bytes.decode(),
                                      "K08": slot.hex().upper(), "tested": tested}, indent=2))
                    return
    print(json.dumps({"result": "NO_MATCH", "notes_sha256": hashlib.sha256(original).hexdigest(),
                      "source_ids": list(ANCHORS), "fragment_counts": {k: len(v) for k, v in frag.items()},
                      "joiners": list(JOINERS), "orderings": 6,
                      "assignment_tests": tested}, indent=2))


if __name__ == "__main__":
    main()
