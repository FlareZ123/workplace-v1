"""Acceptance-blind, source-pinned MT19937 tail-gap constraint for original H17 ZIP."""
from __future__ import annotations
import hashlib
import math
import re
import struct
import sys
import zipfile
from pathlib import Path

SOURCE = "evidence/print/spool-reconstruction.log"
SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"

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
    return ur(ul(ul(ur(y,18),15,0xefc60000),7,0x9d2c5680),11)

def twist(a, b):
    y = (a & 0x80000000) | (b & 0x7fffffff)
    return (y >> 1) ^ (0x9908b0df if y & 1 else 0)

def run(source):
    if source.is_file():
        with zipfile.ZipFile(source) as z:
            raw = z.read(SOURCE)
    else:
        raw = (source / SOURCE).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SHA256
    lines = [s for s in raw.decode().splitlines() if s.startswith("2026-")]
    rows = [bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", line).group(1)) for line in lines]
    assert len(rows) == 133
    words = [tuple(map(untemper,struct.unpack("<4I",v))) for v in rows]
    witnesses = [((44,0),(97,3),(131,0)),((45,0),(98,3),(132,3))]
    starts = []
    for (a,i),(b,j),(c,k) in witnesses:
        assert words[c][k] == words[b][j] ^ twist(words[a][i],words[a][i+1])
        starts.append((397+i-j,624+i-k))
    assert starts == [(394,624),(394,621)]
    extra1 = starts[0][1]-starts[0][0]-4*(131-97)
    extra2 = starts[1][1]-starts[1][0]-4*(132-98)
    assert (extra1,extra2) == (94,91)
    n = 60
    prob = sum(math.comb(n+k-1,k)*(.75**n)*(.25**k) for k in range(5))
    print("source_spool_sha256", SHA256)
    print("tail_MT_witnesses", "PASS", witnesses)
    print("extra_draws_sum_g97_to_g130", extra1)
    print("extra_draws_sum_g98_to_g131", extra2)
    print("adjacent_gap_identities", "g44=g97", "g131=g97-3")
    print("fixed_4_extra_per_regular_interval", "IMPOSSIBLE", "minimum_120_gt_94")
    print("two_randbelow3_plus_one_fixed_word", "max_4_rejections_in_60_calls")
    print("iid_rejection_probability_upper_bound", f"{prob:.12g}")
    print("selected_row129", "NOT_PREDICTED")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_tail_gap_discriminator.py ORIGINAL_CASE.zip")
    run(Path(sys.argv[1]))
