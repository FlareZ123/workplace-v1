"""Selected-ACK-withheld original-source certificate: tail DEST sampler lacks a draw.

Usage: python k04_tail_dest_no_draw.py <original-unpacked-case-root>

The source-specific MT placements are conditional on a shared producer stream.
Selected printer row129 and all K04/K08 commitments are excluded entirely.
"""
import hashlib
import re
import struct
import sys
from pathlib import Path

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MAG = 0x9908B0DF
MASK = 0xFFFFFFFF


def undo_right(v, shift):
    x = v
    for _ in range(6):
        x = v ^ (x >> shift)
    return x & MASK


def undo_left(v, shift, bitmask):
    x = v
    for _ in range(6):
        x = v ^ ((x << shift) & bitmask)
    return x & MASK


def untemper(v):
    return undo_right(
        undo_left(undo_left(undo_right(v, 18), 15, 0xEFC60000), 7, 0x9D2C5680), 11
    )


def twist(first, next_word):
    z = (first & 0x80000000) | (next_word & 0x7FFFFFFF)
    return ((z >> 1) ^ (MAG if z & 1 else 0)) & MASK


def read_selected_source(root):
    path = root / "evidence/print/spool-reconstruction.log"
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == SPOOL_SHA
    lines = [line for line in data.decode("ascii").splitlines() if line.startswith("2026-")]
    assert len(lines) == 133
    # Never parse, inspect or use selected ACK row129.
    chosen = {}
    for index in (44, 97, 130, 131):
        line = lines[index]
        payload = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", line).group(1))
        destination = re.search(r"DEST=(\w+)", line).group(1)
        words = tuple(untemper(v) for v in struct.unpack("<4I", payload))
        chosen[index] = (words, destination)
    return chosen


def test(root):
    samples = read_selected_source(root)
    w44, _ = samples[44]
    w97, _ = samples[97]
    w130, dst130 = samples[130]
    w131, dst131 = samples[131]
    assert dst130 == "bench" and dst131 == "desk"
    assert w97[3] ^ twist(w44[0], w44[1]) == w131[0]
    inferred_predecessor_bits = [
        bit for bit in (0, 1)
        if w97[2] ^ twist(bit << 31, w44[0]) == w130[3]
    ]
    assert inferred_predecessor_bits == [0]
    # First equality forces s131 = s44 + 624.
    # Second equality forces s130 = s44 + 620.
    # Hence s131 = s130 + 4: four row130 payload draws then row131 payload.
    print("source SHA256 PASS")
    print("row44/97/131 untempered MT recurrence PASS")
    print("row44 predecessor MSB -> row97/130 recurrence PASS", inferred_predecessor_bits)
    print("conditional row130->row131 MT gap g130=0")
    print("row130 observed DEST=bench; post-payload sampler needs >=1 hidden draw")
    print("Therefore ordinary postpayload DEST sampler cannot apply to row130")
    print("selected ACK row129, acceptance and K08 sources withheld")


if __name__ == "__main__":
    test(Path(sys.argv[1]))
