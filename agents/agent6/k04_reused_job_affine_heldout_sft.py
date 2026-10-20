"""Original-source held-out test of a shared 128-bit affine job-retry producer.

Conditional mechanism: both physical job identities use the same affine
transition P[next] = A*P[current]+B (mod 2^128), with each event advancing
one state regardless of its CLASS or dispatch status.

Known transitions:
  0420 STORES ACK1 -> RECOVER ACK2
  0417 LABEL ACK1  -> RECOVER REQUESTED1
Held-out prediction:
  0417 REQUESTED1 -> [selected ACK2 excluded] -> REQUESTED3

No K04 selected ACK value, routing mask, commitment or verifier is used.
"""
from __future__ import annotations

import hashlib
import random
import re
import sys
from pathlib import Path

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MODULUS = 1 << 128
MASK = MODULUS - 1


def valuations(value: int) -> int:
    return 128 if value == 0 else (value & -value).bit_length() - 1


def affine_candidates(x0: int, x1: int, y0: int, y1: int) -> list[tuple[int, int]]:
    """Solve A*(x0-y0) = x1-y1 modulo 2**128, B = x1-A*x0."""
    dx = (x0 - y0) & MASK
    dy = (x1 - y1) & MASK
    t = valuations(dx)
    if valuations(dy) < t:
        return []
    assert t < 128
    mod = MODULUS >> t
    base = ((dy >> t) * pow(dx >> t, -1, mod)) % mod
    return [(base + i*mod, (x1-(base + i*mod)*x0) & MASK)
            for i in range(1 << t)]


def read_source(path: Path) -> tuple[bytes, bytes, bytes, bytes, bytes]:
    source = path.read_bytes()
    assert hashlib.sha256(source).hexdigest() == SPOOL_SHA
    lines = [line for line in source.splitlines()
             if b"2026-10-03T18:02:00Z JOB=PS-261003-0417" not in line]
    rows = {}
    for line in lines:
        if b"JOB=PS-261003-0417" not in line and b"JOB=PS-261003-0420" not in line:
            continue
        f = dict(re.findall(rb"([A-Z]+)=([^ ]+)", line))
        key = (f[b"JOB"].decode(), f[b"ATTEMPT"].decode(), f[b"STATE"].decode())
        rows[key] = bytes.fromhex(f[b"PAYLOAD"].decode())
    return (
        rows["PS-261003-0420", "1", "ACK"],
        rows["PS-261003-0420", "2", "ACK"],
        rows["PS-261003-0417", "1", "ACK"],
        rows["PS-261003-0417", "1", "REQUESTED"],
        rows["PS-261003-0417", "3", "REQUESTED"],
    )


def run(path: Path) -> None:
    randomizer = random.Random(12917)
    for i in range(100):
        x0 = randomizer.getrandbits(128) | 1
        y0 = randomizer.getrandbits(128) & ~1
        a_true = randomizer.getrandbits(128)
        b_true = randomizer.getrandbits(128)
        x1 = (a_true*x0+b_true) & MASK
        y1 = (a_true*y0+b_true) & MASK
        candidates = affine_candidates(x0, x1, y0, y1)
        assert (a_true, b_true) in candidates, i
        y3 = (a_true*(a_true*y1+b_true)+b_true) & MASK
        assert any((a*(a*y1+b)+b)&MASK == y3 for a, b in candidates)
    assert affine_candidates(1, 2, 17, 0) == []
    print("SYNTHETIC_CONTROLS: 101/101 PASS")

    q0, q1, j0, j1, j3 = read_source(path)
    for endian in ("little", "big"):
        x0, x1, y0, y1, y3 = [
            int.from_bytes(v, endian) for v in (q0, q1, j0, j1, j3)
        ]
        print("BYTE_ORDER", endian,
              "dx_v2", valuations((x0-y0)&MASK),
              "dy_v2", valuations((x1-y1)&MASK))
        candidates = affine_candidates(x0, x1, y0, y1)
        print("AFFINE_MODELS", len(candidates))
        for a, b in candidates:
            # With selected ACK2 wholly withheld, predict next known request3.
            predicted = (a*(a*y1+b)+b)&MASK
            print("HELDOUT_0417_REQUESTED3_PREDICTION",
                  predicted.to_bytes(16, endian).hex().upper(),
                  "MATCH", predicted == y3)
            assert predicted != y3
    print("SOURCE_HELDOUT_ACCEPTED_MODELS=0")
    print("K04_ACTUAL_TARGET_BITS=0; K08_FINAL_WORDS=0")


if __name__ == "__main__":
    run(Path(sys.argv[1]) if len(sys.argv) == 2 else
        Path(__file__).resolve().parents[2] / "resources/evidence/print/spool-reconstruction.log")
