"""Source-only hidden CLASS/DEST draw predictions from intact printer words.

Disputed selected original row129, masking data and REC8 digests stay unread.
Supports original hypothetical 133-row starts and synthetic seeded positive controls.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from k04_source_dest_parity_projection import original_rows, synthetic, temper

A = 0x9908B0DF
MASK = 0xFFFFFFFF

def twist(a: int, b: int) -> int:
    x = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return ((x >> 1) ^ (A if x & 1 else 0)) & MASK

def inverse(y: int) -> int:
    bit = y >> 31
    return (((y ^ (A if bit else 0)) << 1) | bit) & MASK

def selector_nogoods(rows, starts, classes, dests):
    """Report contradictory source triples; never infer selected coupon output."""
    if len(starts) != 133 or starts[0] != 0:
        raise ValueError("Require 133 original-relative printer starts")
    if any(starts[r + 1] < starts[r] + 4 for r in range(132)):
        raise ValueError("Overlapping original printer blocks")
    if rows[129] or any(len(words) != 4 for r, words in enumerate(rows) if r != 129):
        raise ValueError("Original selected row129 must be withheld")
    observed = {starts[r] + j: (r, j, w)
                for r, words in enumerate(rows) for j, w in enumerate(words)}
    hidden = {}
    for r in range(128):
        if r:
            hidden[starts[r] - 1] = ("CLASS", r, classes[r])
        hidden[starts[r] + 4] = ("DEST", r, dests[r])

    contradictions = []
    tested = {"CLASS": 0, "DEST": 0}
    for pos, (a, i, x) in observed.items():
        # Inverse one-step MT: original words at pos, pos+397, pos+624
        # fix the low31 of the normally hidden output at pos+1.
        b = observed.get(pos + 397)
        c = observed.get(pos + 624)
        target = hidden.get(pos + 1)
        if b is not None and c is not None and target is not None:
            kind, r, accepted = target
            low = inverse(b[2] ^ c[2]) & 0x7FFFFFFF
            codes = {temper(y) >> (29 if kind == "CLASS" else 30)
                     for y in (low, low | 0x80000000)}
            tested[kind] += 1
            allowed = {accepted} if kind == "CLASS" else {accepted, 3}
            if codes.isdisjoint(allowed):
                contradictions.append({
                    "producer": "inverse",
                    "source_rows_words": [[a, i], [b[0], b[1]], [c[0], c[1]]],
                    "target_row": r,
                    "target_field": kind,
                    "target_relative_word": -1 if kind == "CLASS" else 4,
                    "predicted_codes": sorted(codes),
                    "accepted_code": accepted,
                    "required_source_offset_pair": [397, 624],
                    "required_target_offset": 1,
                })
        # Forward one-step MT: original words at pos, pos+1, pos+397
        # predict the complete hidden output at pos+624.
        b = observed.get(pos + 1)
        c = observed.get(pos + 397)
        target = hidden.get(pos + 624)
        if b is not None and c is not None and target is not None:
            kind, r, accepted = target
            code = temper(c[2] ^ twist(x, b[2])) >> (29 if kind == "CLASS" else 30)
            tested[kind] += 1
            allowed = {accepted} if kind == "CLASS" else {accepted, 3}
            if code not in allowed:
                contradictions.append({
                    "producer": "forward",
                    "source_rows_words": [[a, i], [b[0], b[1]], [c[0], c[1]]],
                    "target_row": r,
                    "target_field": kind,
                    "target_relative_word": -1 if kind == "CLASS" else 4,
                    "predicted_codes": [code],
                    "accepted_code": accepted,
                    "required_source_offset_pair": [1, 397],
                    "required_target_offset": 624,
                })
    return {"checked_hidden_selectors": tested,
            "contradiction_count": len(contradictions),
            "source_nogoods": contradictions}

def main():
    for seed in (433, 958, 2267, 2311, 3142, 6785, 8113, 8122):
        rows, starts, classes, dests, _, _ = synthetic(seed)
        result = selector_nogoods(rows, starts, classes, dests)
        assert result["contradiction_count"] == 0, result
        print("Synthetic producer PASS", seed, "selected index", starts[129],
              "hidden selector checks", result["checked_hidden_selectors"])
    if len(sys.argv) == 3:
        rows, classes, dests = original_rows(sys.argv[1])
        starts = json.loads(Path(sys.argv[2]).read_text(encoding="utf8"))["row_starts"]
        result = selector_nogoods(rows, starts, classes, dests)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
