"""Direct original-source MT19937 sampler nogoods without a 624-word GF(2) solve.

Usage: python agents/agent50/k04_metadata_twist_nogoods.py original-export.zip
Published source-consistent index955 is a conditional chronology hypothesis.
Selected spool row129, REC8 commitments and routing mask are never read.
"""
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
SPOOL = "evidence/print/spool-reconstruction.log"
SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
A = 0x9908b0df
HI = 0x80000000
LO = 0x7fffffff
DEST = {"store": 0, "desk": 1, "bench": 2}
CLASS = {"LABEL": 0, "STORES": 1, "RECOVER": 2}

def ur(y, n):
    x = y
    for _ in range(6):
        x = y ^ (x >> n)
    return x & 0xffffffff

def ul(y, n, mask):
    x = y
    for _ in range(6):
        x = y ^ ((x << n) & mask)
    return x & 0xffffffff

def untemper(y):
    return ur(ul(ul(ur(y, 18), 15, 0xefc60000), 7, 0x9d2c5680), 11)

def temper(y):
    y ^= y >> 11
    y ^= (y << 7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= y >> 18
    return y & 0xffffffff

def twist(a, b):
    x = (a & HI) | (b & LO)
    return ((x >> 1) ^ (A if x & 1 else 0)) & 0xffffffff

def inverse_twist(y):
    odd = y >> 31
    return (((y ^ (A if odd else 0)) << 1) | odd) & 0xffffffff

def candidates(t, at):
    """Return small, source-anchored candidate states and their donor identities."""
    paths = []
    # Hidden state is the recurrence's end word.
    p, n, m = at.get(t - 624), at.get(t - 623), at.get(t - 227)
    if n and m and t >= 624:
        aa = [p[2]] if p else [0, HI]
        paths.append(({m[2] ^ twist(a, n[2]) for a in aa}, "end",
                      [item[:2] for item in (p, n, m) if item]))
    # Hidden state is the recurrence's middle word.
    p, n, m = at.get(t - 397), at.get(t - 396), at.get(t + 227)
    if n and m:
        aa = [p[2]] if p else [0, HI]
        paths.append(({m[2] ^ twist(a, n[2]) for a in aa}, "middle",
                      [item[:2] for item in (p, n, m) if item]))
    # Hidden state is the successor's low31, optionally including its MSB.
    p, n = at.get(t + 396), at.get(t + 623)
    if p and n:
        low = inverse_twist(p[2] ^ n[2]) & LO
        q, r = at.get(t + 397), at.get(t + 624)
        high = [inverse_twist(q[2] ^ r[2]) & HI] if q and r else [0, HI]
        paths.append(({low | value for value in high}, "successor",
                      [item[:2] for item in (p, n, q, r) if item]))
    return paths

def main(source):
    starts = json.loads((ROOT / "results/h17-k04-source-consistent-index955.json")
                        .read_text(encoding="utf8"))["row_starts"]
    assert len(starts) == 133 and starts[129] == 955
    with ZipFile(source) as archive:
        raw = archive.read(SPOOL)
    assert hashlib.sha256(raw).hexdigest() == SHA
    lines = [line.decode() for line in raw.splitlines() if line.startswith(b"2026-")]
    assert len(lines) == 133
    at = {}
    for r, line in enumerate(lines):
        if r == 129:
            continue
        found = re.search(r"PAYLOAD=([0-9A-F]{32})", line)
        words = struct.unpack("<4I", bytes.fromhex(found.group(1)))
        for j, word in enumerate(words):
            at[starts[r] + j] = (r, j, untemper(word))
    assert len(at) == 528
    violations = []
    for row in range(127):
        if starts[row + 1] - starts[row] != 6:
            continue
        specs = [(4, 2, DEST[re.search(r"DEST=([a-z]+)", lines[row]).group(1)], "DEST"),
                 (5, 3, CLASS[re.search(r"CLASS=([A-Z]+)", lines[row + 1]).group(1)], "CLASS")]
        for offset, width, wanted, kind in specs:
            t = starts[row] + offset
            paths = candidates(t, at)
            if not paths:
                continue
            possible = set.intersection(*(part[0] for part in paths))
            codes = sorted({temper(value) >> (32 - width) for value in possible})
            if wanted not in codes:
                violations.append((row, kind, wanted, codes, t,
                                   [(name, donor) for _, name, donor in paths]))
    assert len(violations) == 15, violations
    assert len({row for row, *_ in violations}) == 11
    print("source-indexed output-role contradictions:", len(violations))
    print("distinct ordinary boundaries:", len({v[0] for v in violations}))
    for violation in violations:
        print(violation)
    # CLASS n4 maps accepted index3 also to LABEL, excluding two of the n3 boundaries.
    n4_bad = set()
    for row, kind, wanted, codes, t, donors in violations:
        if kind == "CLASS" and wanted == 0 and 3 in codes:
            continue
        n4_bad.add(row)
    assert len(n4_bad) == 9, sorted(n4_bad)
    print("distinct boundaries for CLASS n4:", sorted(n4_bad))

if __name__ == "__main__":
    main(Path(sys.argv[1]))
