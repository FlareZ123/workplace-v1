"""Source-only row9/40/63/124 MT19937 closure after Agent21 double-twist bridge.
Run with the unmodified original local case ZIP. Selected row129, routing, mask,
acceptance commitments, and K08 data are not read.
"""
from __future__ import annotations
import hashlib
import random
import re
import struct
import sys
import zipfile
from pathlib import Path

SPOOL = "evidence/print/spool-reconstruction.log"
SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MAG = 0x9908B0DF
ALL = 0xFFFFFFFF
LO31 = 0x7FFFFFFF
MSB = 0x80000000
STARTS = {9: 0, 40: 229, 63: 398, 124: 852}
NEW_FULL = {-394: 0x7168DD87, -393: 0x289D44B5,
            4: 0x8DAE2276, 625: 0x78204AD3,
            626: 0xC472C638, 627: 0xC34BEB5E, 628: 0x2EEBC38E}


def untemper(value: int) -> int:
    for shift, mask in ((18, None), (15, 0xEFC60000), (7, 0x9D2C5680), (11, None)):
        before = value
        for _ in range(6):
            value = before ^ (value >> shift if mask is None else ((value << shift) & mask))
    return value & ALL


def temper(value: int) -> int:
    value ^= value >> 11
    value ^= (value << 7) & 0x9D2C5680
    value ^= (value << 15) & 0xEFC60000
    return (value ^ (value >> 18)) & ALL


def twist(a: int, b: int) -> int:
    mixed = (a & MSB) | (b & LO31)
    return ((mixed >> 1) ^ (MAG if mixed & 1 else 0)) & ALL


def inverse_twist(value: int) -> int:
    odd = value >> 31
    return (((value ^ (MAG if odd else 0)) << 1) | odd) & ALL


def close_known(observed: dict[int, int]) -> dict[int, tuple[int, int]]:
    state = {pos: (ALL, value) for pos, value in observed.items()}

    def add_bits(pos: int, mask: int, value: int) -> bool:
        old_mask, old_value = state.get(pos, (0, 0))
        if ((old_value ^ value) & old_mask & mask) != 0:
            raise AssertionError(f"Inconsistent original MT state at {pos}")
        merged = (old_mask | mask, old_value | (mask & value))
        changed = merged != (old_mask, old_value)
        state[pos] = merged
        return changed

    for _ in range(40):
        changes = 0
        for pos in range(min(observed) - 624, max(observed) + 1):
            am, av = state.get(pos, (0, 0))
            bm, bv = state.get(pos + 1, (0, 0))
            cm, cv = state.get(pos + 397, (0, 0))
            dm, dv = state.get(pos + 624, (0, 0))
            if cm == dm == ALL:
                mixed = inverse_twist(cv ^ dv)
                changes += add_bits(pos, MSB, mixed & MSB)
                changes += add_bits(pos + 1, LO31, mixed & LO31)
            if am & MSB and bm & LO31 == LO31:
                term = twist(av, bv)
                if cm == ALL:
                    changes += add_bits(pos + 624, ALL, cv ^ term)
                if dm == ALL:
                    changes += add_bits(pos + 397, ALL, dv ^ term)
        if changes == 0:
            break
    else:
        raise AssertionError("Source closure did not converge")
    return state


def observed_group(rows: list[list[int]]) -> dict[int, int]:
    return {start + j: value for r, start in STARTS.items() for j, value in enumerate(rows[r])}


def bridge_assertions(rows: list[list[int]]) -> None:
    for j in (2, 3):
        a, b, c, d = (rows[9][j], rows[40][j - 2], rows[63][j - 2], rows[124][j - 2])
        mask = 0xBFFFFFFF
        ha = ((a & LO31) >> 1) ^ (MAG if a & 1 else 0)
        hb = ((b & LO31) >> 1) ^ (MAG if b & 1 else 0)
        assert ((c ^ d) & mask) == ((ha ^ hb) & mask)


def test_synthetic() -> None:
    for seed in range(20):
        rng = random.Random(18700 + seed)
        stream = [untemper(rng.getrandbits(32)) for _ in range(2000)]
        rows = [[] for _ in range(133)]
        for r, offset in STARTS.items():
            rows[r] = stream[600 + offset:604 + offset]
        bridge_assertions(rows)
        state = close_known(observed_group(rows))
        for pos in NEW_FULL:
            mask, value = state[pos]
            assert mask == ALL and value == stream[600 + pos], (seed, pos)
    print("Independent seeded producer controls: 20/20 PASS")


def test_original(source: Path) -> None:
    with zipfile.ZipFile(source) as archive:
        raw = archive.read(SPOOL)
    assert hashlib.sha256(raw).hexdigest() == SHA256
    rows = [[untemper(w) for w in struct.unpack("<4I", bytes.fromhex(m.group(1).decode("ascii")))]
            for m in re.finditer(rb"PAYLOAD=([0-9A-F]{32})", raw)]
    assert len(rows) == 133
    rows[129] = []
    bridge_assertions(rows)
    observed = observed_group(rows)
    state = close_known(observed)
    recovered = {p: value for p, (mask, value) in state.items()
                 if mask == ALL and p not in observed}
    assert recovered == NEW_FULL, recovered
    assert state[5] == (LO31, 0x5E28452A)
    assert temper(recovered[4]) >> 30 == 3
    print("Original spool SHA256", SHA256)
    print("Four row starts relative row9", STARTS)
    print("Source-only full hidden states", {str(p): f"{v:08X}" for p, v in recovered.items()})
    print("Four-word middle run", " ".join(f"{recovered[p]:08X}" for p in range(625, 629)))
    print("Original row9 hidden DEST code 3 (rejected), derived without DEST text")
    print("Original K04 coupon new bits: 0; final K08 caption words: 0")


if __name__ == "__main__":
    test_synthetic()
    test_original(Path(sys.argv[1]))
