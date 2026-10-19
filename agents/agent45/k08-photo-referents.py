"""Read-only K08 test for N08/N14 as the photograph following N10's 'last cup' reference.

Exactly one anchored 2..8-word source-exact fragment apiece from the photo
note, N13 and N20, all six source orders and three connectors in both gaps.
The photograph referent and literal-splice grammar are unproven hypotheses.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import re
import sys
import time

NOTE_SHA256 = "13f2318ccc54f35b590a2d76b3a80244fe24d70f0699c67c05858e8b8983c5cb"
ANCHORS = {
    "N08": ("window", "daylight", "water", "overnight"),
    "N14": ("horizon", "boat", "rain"),
    "N13": ("night", "mugs", "window", "lamp"),
    "N20": ("sea", "voices", "table"),
}
JOINERS = (b" ", b" and ", b" while ")


def fragments(notes: str, note_id: str) -> list[bytes]:
    match = re.search(r"^" + note_id + r" / [^\n]+\n([^\n]+)", notes, re.M)
    assert match is not None, note_id
    text = match.group(1).split(".", 1)[0] if note_id == "N20" else match.group(1)
    words = re.findall(r"[a-z0-9]+", text.lower())
    return sorted({
        " ".join(words[start:end]).encode("ascii")
        for start in range(len(words))
        for end in range(start + 2, min(start + 9, len(words) + 1))
        if any(anchor in words[start:end] for anchor in ANCHORS[note_id])
    })


def main(root: Path) -> None:
    note_bytes = (root / "evidence/crew/noticeboard-and-desk-notes.txt").read_bytes()
    assert hashlib.sha256(note_bytes).hexdigest() == NOTE_SHA256
    notes = note_bytes.decode("utf-8")
    routing = json.loads((root / "evidence/recovery-routing.json").read_text(encoding="utf-8"))
    inventory = json.loads((root / "acceptance.json").read_text(encoding="utf-8"))
    nonce = bytes.fromhex(routing["K08"]["desk_nonce"])
    target = bytes.fromhex(inventory["slot_sha256"]["K08"])
    padded_nonce = nonce.ljust(64, b"\0")
    inner_base = hashlib.sha256(bytes(value ^ 0x36 for value in padded_nonce))
    outer_base = hashlib.sha256(bytes(value ^ 0x5c for value in padded_nonce))

    def derive(message: bytes) -> bytes:
        inner = inner_base.copy()
        inner.update(message)
        outer = outer_base.copy()
        outer.update(inner.digest())
        return outer.digest()[:16]

    control = b"a good watch leaves the room ready for the next pair of hands"
    assert derive(control).hex().upper() == "BF889359B0303F2B2B2FD96AE841210B"
    sources = {note_id: fragments(notes, note_id) for note_id in ANCHORS}
    assert {key: len(sources[key]) for key in ANCHORS} == {
        "N08": 48, "N14": 68, "N13": 85, "N20": 62
    }

    for photo_id in ("N08", "N14"):
        started = time.perf_counter()
        tested = 0
        for order in itertools.permutations((photo_id, "N13", "N20")):
            for first, second, third in itertools.product(*(sources[key] for key in order)):
                for join_one in JOINERS:
                    for join_two in JOINERS:
                        phrase = first + join_one + second + join_two + third
                        slot = derive(phrase)
                        tested += 1
                        if hashlib.sha256(slot).digest() == target:
                            print(json.dumps({
                                "photo_id": photo_id,
                                "result": "PASS",
                                "phrase": phrase.decode("ascii"),
                                "K08": slot.hex().upper(),
                                "tested": tested,
                            }, indent=2))
                            return
        print(json.dumps({
            "photo_id": photo_id,
            "result": "NO_MATCH",
            "source_note_sha256": NOTE_SHA256,
            "fragment_counts": {key: len(sources[key]) for key in (photo_id, "N13", "N20")},
            "source_orders": 6,
            "connector_pairs": 9,
            "assignments": tested,
            "seconds": round(time.perf_counter() - started, 2),
        }, indent=2))


if __name__ == "__main__":
    resource_root = (
        Path(sys.argv[1]) if len(sys.argv) > 1
        else Path(__file__).resolve().parents[2] / "resources"
    )
    main(resource_root)
