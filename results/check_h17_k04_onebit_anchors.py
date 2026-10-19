"""Recover extra MT19937 recurrence witnesses with unknown predecessor MSB.

Run: python results/check_h17_k04_onebit_anchors.py original-case.zip
Selected K04 row 129 is excluded before searching; no acceptance read.
"""
import hashlib
import re
import struct
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

SOURCE = "evidence/print/spool-reconstruction.log"
SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def ur(y, n):
    x = y
    for _ in range(6):
        x = y ^ (x >> n)
    return x & 0xFFFFFFFF


def ul(y, n, m):
    x = y
    for _ in range(6):
        x = y ^ ((x << n) & m)
    return x & 0xFFFFFFFF


def untemper(y):
    return ur(ul(ul(ur(y, 18), 15, 0xEFC60000), 7, 0x9D2C5680), 11)


def tw(one_bit, next_word):
    y = (one_bit << 31) | (next_word & 0x7FFFFFFF)
    return ((y >> 1) ^ (0x9908B0DF if y & 1 else 0)) & 0xFFFFFFFF


def scan(rows):
    entries = [(r, j, x) for r, row in enumerate(rows)
               if r != 129 for j, x in enumerate(row)]
    by_value = defaultdict(list)
    for r, j, x in entries:
        by_value[x].append((r, j))
    found = []
    for a, i, second in entries:
        for predecessor_msb in (0, 1):
            t = tw(predecessor_msb, second)
            for b, j, middle in entries:
                if b <= a:
                    continue
                for c, k in by_value.get(middle ^ t, ()):
                    if c > b:
                        found.append(((a, i), (b, j), (c, k), predecessor_msb))
    return found


def run(source):
    if source.is_file():
        with zipfile.ZipFile(source) as z:
            raw = z.read(SOURCE)
    else:
        raw = (source / SOURCE).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SHA
    payloads = [bytes.fromhex(s.decode())
                for s in re.findall(rb"PAYLOAD=([0-9A-F]{32})", raw)]
    assert len(payloads) == 133
    words = [tuple(untemper(x) for x in struct.unpack("<4I", p))
             for p in payloads]
    matches = scan(words)
    assert len(matches) == 42, len(matches)
    assert sum(m[0][1] == 0 for m in matches) == 17
    anchors = [
        ((43, 0), (96, 3), (128, 0), 1),
        ((44, 0), (97, 2), (130, 3), 0),
        ((45, 0), (98, 2), (132, 2), 1),
    ]
    assert all(x in matches for x in anchors)
    print("source_sha256", SHA)
    print("one_bit_witnesses", len(matches), "start_word_witnesses", 17)
    print("independent_tail_anchors", anchors)
    print("conditional_s128_minus_s43", 623)
    print("conditional_s130_minus_s44", 620)
    print("conditional_min_s44_minus_s43", 11)
    print("conditional_min_hidden_outputs", 7)
    print("target_129_predecessor_words", "inside_hidden_43_to_44_gap")
    print("K04", "UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python check_h17_k04_onebit_anchors.py ORIGINAL_CASE.zip")
    run(Path(sys.argv[1]))
