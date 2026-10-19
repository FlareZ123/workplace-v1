"""Source-only MT19937 recurrence witnesses using an unobserved row-start predecessor.

Run: python agents/agent23/k04_mt_rowstart.py original-case.zip
Does not inspect the selected row129 or any acceptance commitment.
"""
import hashlib
import re
import struct
import sys
import zipfile
from collections import defaultdict

SPOOL = "evidence/print/spool-reconstruction.log"
SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def ur(y, shift):
    x = y
    for _ in range(6):
        x = y ^ (x >> shift)
    return x & 0xFFFFFFFF


def ul(y, shift, mask):
    x = y
    for _ in range(6):
        x = y ^ ((x << shift) & mask)
    return x & 0xFFFFFFFF


def untemper(y):
    return ur(ul(ul(ur(y, 18), 15, 0xEFC60000), 7, 0x9D2C5680), 11)


def twist(high_bit, next_word):
    y = ((high_bit & 1) << 31) | (next_word & 0x7FFFFFFF)
    return ((y >> 1) ^ (0x9908B0DF if y & 1 else 0)) & 0xFFFFFFFF


def discover(source):
    with zipfile.ZipFile(source) as z:
        raw = z.read(SPOOL)
    assert hashlib.sha256(raw).hexdigest() == SHA
    lines = [s for s in raw.decode().splitlines() if s.startswith("2026-")]
    payloads = [bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", s).group(1)) for s in lines]
    assert len(payloads) == 133
    words = [[untemper(v) for v in struct.unpack("<4I", p)] for p in payloads]
    words[129] = []
    lookup = defaultdict(list)
    for row, ws in enumerate(words):
        for j, value in enumerate(ws):
            lookup[value].append((row, j))
    within, boundary = [], []
    for row, ws in enumerate(words):
        for j in range(len(ws)-1):
            delta = twist(ws[j] >> 31, ws[j+1])
            for mid in range(row+1, len(words)):
                for k, value in enumerate(words[mid]):
                    for end, l in lookup.get(delta ^ value, ()):
                        if end > mid:
                            within.append(((row,j),(mid,k),(end,l)))
        if not ws:
            continue
        for bit in (0, 1):
            delta = twist(bit, ws[0])
            for mid in range(row+1, len(words)):
                for k, value in enumerate(words[mid]):
                    for end, l in lookup.get(delta ^ value, ()):
                        if end > mid:
                            boundary.append((row, bit, (mid,k), (end,l)))
    return within, boundary


def bound_function(within, boundary):
    edges = []
    def equal(a, b, offset):
        edges.append((a,b,offset))
        edges.append((b,a,-offset))
    for (a,j),(b,k),(c,l) in within:
        equal(a,b,397+j-k)
        equal(a,c,624+j-l)
    for a, bit, (b,k), (c,l) in boundary:
        equal(a,b,396-k)
        equal(a,c,623-l)
    for r in range(132):
        edges.append((r+1,r,-4))

    def shortest(start, end):
        d = [float("inf")]*133
        d[start] = 0
        for _ in range(132):
            changed = False
            for a,b,v in edges:
                if d[a]+v < d[b]:
                    d[b] = d[a]+v
                    changed = True
            if not changed:
                break
        assert not any(d[a]+v < d[b] for a,b,v in edges)
        return d[end]

    return lambda a,b: (-shortest(b,a),shortest(a,b))


def main(source):
    within, boundary = discover(source)
    assert len(within) == 25
    assert len(boundary) == 17
    assert (43,1,(96,3),(128,0)) in boundary
    assert (44,0,(97,2),(130,3)) in boundary
    assert ((44,0),(97,3),(131,0)) in within
    difference = bound_function(within, boundary)
    assert difference(43,44) == (11,65)
    assert difference(130,131) == (4,4)
    assert difference(0,129) == (917,971)
    print("spool_sha256",SHA)
    print("selected_row129_withheld",True)
    print("within_witnesses",len(within),"row_start_witnesses",len(boundary))
    for x in boundary:
        print("row_start",x)
    print("s44-s43",difference(43,44))
    print("s131-s130",difference(130,131))
    print("s129-s0",difference(0,129))
    print("exact s128=s43+623, s130=s44+620, s131=s44+624")
    print("exact g128+g129=s44-s43-11")
    print("K04 UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_mt_rowstart.py original-case.zip")
    main(sys.argv[1])
