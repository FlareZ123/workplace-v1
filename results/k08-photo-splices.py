"""Bounded K08 photo-caption + Emily-note splice diagnostic.

The surviving mail says Emily used the desk notes and photographs to develop
her final words. This tests the narrowly defined possibility that she joined
one contiguous, source-exact 2..10 word phrase from a photo/galley/mug caption
to one contiguous, source-exact 2..10 word phrase from her six surviving
draft/description notes, in either order, using eight fixed connectors.

The original K08 HMAC/slot commitment is applied without modification.
A negative result excludes only these explicitly defined candidate phrases.
"""
from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1] / "resources"
PHOTOS = ("N01", "N04", "N08", "N09", "N11", "N14", "N19")
EMILY = ("N02", "N06", "N10", "N13", "N20", "N23")
JOINERS = (" ", " and ", " with ", " as ", " when ", " while ",
           " until ", " before ")


def spans(note_text: str, note_ids: tuple[str, ...]) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for note_id in note_ids:
        match = re.search(
            r"^" + note_id + r" / [^\n]+\n([^\n]+)",
            note_text,
            re.MULTILINE,
        )
        if match is None:
            raise ValueError(f"Missing source note {note_id}")
        words = re.findall(r"[a-z0-9]+", match.group(1).lower())
        for start in range(len(words)):
            for end in range(start + 2, min(start + 11, len(words) + 1)):
                result.append((note_id, " ".join(words[start:end])))
    return result


def search() -> dict[str, object]:
    path = ROOT / "evidence/crew/noticeboard-and-desk-notes.txt"
    note_text = path.read_text(encoding="utf-8")
    routing = json.loads((ROOT / "evidence/recovery-routing.json").read_text(encoding="utf-8"))
    acceptance = json.loads((ROOT / "acceptance.json").read_text(encoding="utf-8"))
    nonce = bytes.fromhex(routing["K08"]["desk_nonce"])
    target = bytes.fromhex(acceptance["slot_sha256"]["K08"])
    photo_fragments = spans(note_text, PHOTOS)
    emily_fragments = spans(note_text, EMILY)
    count = 0
    for first_list, second_list in ((photo_fragments, emily_fragments),
                                    (emily_fragments, photo_fragments)):
        for _, left in first_list:
            for _, right in second_list:
                for joiner in JOINERS:
                    phrase = left + joiner + right
                    component = hmac.digest(nonce, phrase.encode("utf-8"), "sha256")[:16]
                    count += 1
                    if hashlib.sha256(component).digest() == target:
                        return {
                            "acceptance": "PASS", "phrase": phrase,
                            "K08": component.hex().upper(), "tested": count
                        }
    return {
        "acceptance": "NO_MATCH", "photo_note_ids": list(PHOTOS),
        "emily_note_ids": list(EMILY), "photo_spans": len(photo_fragments),
        "emily_spans": len(emily_fragments), "joiners": list(JOINERS),
        "tested": count,
        "notes_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(search(), indent=2))
