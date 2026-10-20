"""Test route-sheet mask as an independent contiguous MT19937 source witness.

Requires only original resources/evidence; withholds selected RECOVER ACK, hashes,
nonce and verifier. Searches source-order-consistent printer recurrence controls.
"""
import itertools
import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[2] / "resources" / "evidence"

def undo_rshift(value, shift):
    x = value
    for _ in range(5):
        x = value ^ (x >> shift)
    return x & 0xffffffff

def undo_lshift(value, shift, mask):
    x = value
    for _ in range(5):
        x = value ^ ((x << shift) & mask)
    return x & 0xffffffff

def untemper(value):
    return undo_rshift(
        undo_lshift(undo_lshift(undo_rshift(value, 18), 15, 0xefc60000), 7, 0x9d2c5680), 11)

def twist(x, y):
    z = (x & 0x80000000) | (y & 0x7fffffff)
    return (z >> 1) ^ (0x9908b0df if z & 1 else 0)

printer = []
lines = (root / "print/spool-reconstruction.log").read_text().splitlines()
for index, line in enumerate(lines):
    if "JOB=PS-261003-0417 ATTEMPT=2 STATE=ACK " in line:
        continue  # original selected K04 target, never read into inference
    match = re.search(r"PAYLOAD=([0-9A-F]{32})", line)
    if match is None:
        continue
    raw = bytes.fromhex(match.group(1))
    printer.append((index, [untemper(int.from_bytes(raw[4*k:4*k+4], "little")) for k in range(4)]))

routing = json.loads((root / "recovery-routing.json").read_text())
raw_mask = bytes.fromhex(routing["K04"]["masked_component"])
mask_views = []
for order in ("forward", "reverse"):
    parts = [raw_mask[k:k+4] for k in range(0, 16, 4)]
    if order == "reverse":
        parts.reverse()
    for endian in ("little", "big"):
        mask_views.append((order, endian, [untemper(int.from_bytes(part, endian)) for part in parts]))

assert len(printer) == 132
# Positive control: identify actual original 2-step recurrence witnesses across
# three intact printer runs, allowing offsets in each 4-word run.
controls = []
for (i, early), (j, middle), (h, future) in itertools.combinations(printer, 3):
    for e in range(2):
        for m in range(3):
            for f in range(3):
                if all(future[f+t] == middle[m+t] ^ twist(early[e+t], early[e+t+1])
                       for t in range(2)):
                    controls.append((i, j, h, e, m, f))
assert len(controls) == 7, controls
print("intact printer-only positive two-recurrence controls:", len(controls))
for order, endian, mask in mask_views:
    hits = []
    for (i, a), (j, b) in itertools.combinations(printer, 2):
        for ka in range(2):
            for kb in range(3):
                for km in range(3):
                    if km < 2 and all(b[kb+t] == a[ka+t] ^ twist(mask[km+t], mask[km+t+1])
                                      for t in range(2)):
                        hits.append(("mask early", i, j, ka, kb, km))
                    if all(b[kb+t] == mask[km+t] ^ twist(a[ka+t], a[ka+t+1])
                           for t in range(2)):
                        hits.append(("mask middle", i, j, ka, kb, km))
                    if all(mask[km+t] == b[kb+t] ^ twist(a[ka+t], a[ka+t+1])
                           for t in range(2)):
                        hits.append(("mask future", i, j, ka, kb, km))
    print("mask", order, endian, "two-equation recurrence witnesses:", len(hits))
    assert not hits, hits
