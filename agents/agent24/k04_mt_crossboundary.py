"""Check cross-row MT19937 twists in original printer spool, without commitment reads."""
import hashlib
import re
import struct
from collections import defaultdict
from pathlib import Path

p = Path("resources/evidence/print/spool-reconstruction.log")
raw = p.read_bytes()
assert hashlib.sha256(raw).hexdigest() == "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"

def ur(y, n):
    x = y
    for _ in range(6):
        x = y ^ (x >> n)
    return x & 0xffffffff

def ul(y, n, m):
    x = y
    for _ in range(6):
        x = y ^ ((x << n) & m)
    return x & 0xffffffff

def untemper(y):
    return ur(ul(ul(ur(y, 18), 15, 0xefc60000), 7, 0x9d2c5680), 11)

def twist(a, b):
    v = (a & 0x80000000) | (b & 0x7fffffff)
    return (v >> 1) ^ (0x9908b0df if v & 1 else 0)

hexes = [re.search(r"PAYLOAD=([0-9A-F]{32})", x).group(1)
         for x in raw.decode().splitlines() if x.startswith("2026-")]
w = [[untemper(x) for x in struct.unpack("<4I", bytes.fromhex(h))] for h in hexes]
assert len(w) == 133
lookup = defaultdict(list)
for i, row in enumerate(w):
    for j, x in enumerate(row):
        lookup[x].append((i, j))
hits = []
for i in range(132):
    t = twist(w[i][3], w[i + 1][0])
    for j in range(i + 1, 133):
        for k, value in enumerate(w[j]):
            for a, b in lookup.get(value ^ t, ()):
                if a > j:
                    hits.append(((i, 3), (j, k), (a, b)))
assert hits == [
    ((3, 3), (57, 3), (87, 3)),
    ((12, 3), (67, 1), (97, 2)),
    ((13, 3), (68, 1), (98, 3)),
    ((33, 3), (86, 2), (116, 3)),
    ((40, 3), (94, 2), (125, 0)),
    ((43, 3), (97, 2), (130, 3)),
]
print("Cross-row twist equalities:", *hits, sep="\n")
print("Conditional stream-gap conclusions: d33=d40=d43=d130=4; d42>=14")
