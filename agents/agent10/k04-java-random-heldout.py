"""K04 held-out test of Java java.util.Random 48-bit generator.

Recover an internal state from two observed 32-bit halves of an unaffected
printer row; predict its remaining two halves before considering any K04 hash.
Uses original spool only, with source SHA pin and synthetic positive control.
"""
from pathlib import Path
from hashlib import sha256
import json
import re

A = 0x5DEECE66D
C = 0xB
MASK = (1 << 48) - 1
SOURCE_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def spool_payloads(root=Path("resources")):
    source = (root / "evidence/print/spool-reconstruction.log").read_bytes()
    assert sha256(source).hexdigest() == SOURCE_SHA256
    values = [
        bytes.fromhex(match.group(1).decode("ascii"))
        for match in re.finditer(rb"PAYLOAD=([0-9A-F]{32})", source)
    ]
    assert len(values) == 133
    return values


def state_candidates(first, second):
    for low in range(1 << 16):
        state = (first << 16) | low
        following = (state * A + C) & MASK
        if following >> 16 == second:
            yield following


def check_row(raw, endian):
    words = [int.from_bytes(raw[i:i+4], endian) for i in (0,4,8,12)]
    possible = 0
    confirmed = 0
    for state in state_candidates(words[0], words[1]):
        possible += 1
        third = (state * A + C) & MASK
        fourth = (third * A + C) & MASK
        if (third >> 16, fourth >> 16) == (words[2],words[3]):
            confirmed += 1
    return possible, confirmed


def synthetic_control():
    state = 0x123456789ABC
    words = []
    for _ in range(4):
        state = (state*A+C) & MASK
        words.append(state >> 16)
    for endian in ("little","big"):
        row = b"".join(v.to_bytes(4,endian) for v in words)
        candidates, confirmed = check_row(row,endian)
        assert candidates >= 1 and confirmed == 1
    return "PASS"


def analyze(root=Path("resources")):
    assert synthetic_control() == "PASS"
    payloads = spool_payloads(root)
    results = {}
    for endian in ("little","big"):
        tests = [check_row(row,endian) for row in payloads]
        results[endian] = {
            "regular_two_word_fits": sum(n > 0 for n,_ in tests[:128]),
            "regular_four_word_confirmed": sum(n > 0 for _,n in tests[:128]),
            "tail_two_word_fits": sum(n > 0 for n,_ in tests[128:]),
            "tail_four_word_confirmed": sum(n > 0 for _,n in tests[128:]),
        }
    return {"synthetic_control":"PASS","hypotheses":results}


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2))
