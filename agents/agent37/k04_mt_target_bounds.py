"""Bound selected K04 row-129 MT output-stream index without its payload bytes.

Read-only original ZIP or extracted resources. Independent of REC8 acceptance hash.
Assumes every row corresponds to four consecutive MT outputs, source ordering
is stream ordering, and inter-row extra output consumption is nonnegative.
"""
from __future__ import annotations
import hashlib, re, struct, sys, zipfile
from collections import defaultdict
from pathlib import Path

SPOOL = "evidence/print/spool-reconstruction.log"
DIGEST = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"

def ur(y, n):
    x = y
    for _ in range(6): x = y ^ (x >> n)
    return x & 0xffffffff

def ul(y, n, m):
    x = y
    for _ in range(6): x = y ^ ((x << n) & m)
    return x & 0xffffffff

def ut(y):
    return ur(ul(ul(ur(y,18),15,0xefc60000),7,0x9d2c5680),11)

def twist(a, b):
    y = (a & 0x80000000) | (b & 0x7fffffff)
    return (y >> 1) ^ (0x9908b0df if y & 1 else 0)

def source_words(root):
    if root.is_file():
        with zipfile.ZipFile(root) as z: raw = z.read(SPOOL)
    else: raw = (root / SPOOL).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == DIGEST
    lines = (line for line in raw.decode().splitlines() if line.startswith("2026-"))
    rows = [bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", line).group(1)) for line in lines]
    assert len(rows) == 133
    words = [list(map(ut, struct.unpack("<4I", row))) for row in rows]
    words[129] = []  # genuinely withhold the suspect selected payload
    return words

def get_witnesses(words):
    lookup = defaultdict(list)
    for r, ws in enumerate(words):
        for j, value in enumerate(ws):
            lookup[value].append((r, j))
    out = []
    for a, ws in enumerate(words):
        if len(ws) < 4: continue
        for i in range(3):
            step = twist(ws[i], ws[i+1])
            for b in range(a+1, len(words)):
                for j, value in enumerate(words[b]):
                    for c, k in lookup.get(value ^ step, ()):
                        if c > b: out.append(((a,i),(b,j),(c,k)))
    return out

def shortest(edges, source, target):
    d = [float("inf")] * 133
    d[source] = 0
    for _ in range(132):
        changed = False
        for a, b, w in edges:
            if d[a] + w < d[b]:
                d[b] = d[a] + w
                changed = True
        if not changed: break
    assert not any(d[a] + w < d[b] for a,b,w in edges), "contradictory source constraints"
    return int(d[target])

def run(root):
    hits = get_witnesses(source_words(root))
    assert len(hits) == 25
    edges = []
    for (a,i),(b,j),(c,k) in hits:
        for u,v,w in ((a,b,397+i-j),(a,c,624+i-k)):
            edges += [(u,v,w),(v,u,-w)]
    for r in range(1,133):
        edges.append((r,r-1,-4))  # s[r]-s[r-1] >= 4
    low = -shortest(edges, 129, 0)
    high = shortest(edges, 0, 129)
    assert (low,high) == (916,971)
    print("source_digest", DIGEST)
    print("source_only_witnesses",len(hits),"selected_row129_withheld",True)
    print("relative_first_output_index_inclusive",low,high,"possibilities",high-low+1)
    print("K04_component", "UNRESOLVED")

if __name__ == "__main__":
    if len(sys.argv)!=2: raise SystemExit("usage: python k04_mt_target_bounds.py <original-case.zip>")
    run(Path(sys.argv[1]))
