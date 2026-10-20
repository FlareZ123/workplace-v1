"""Counterfactual direct-initial-state output recurrence test, not actual std::mt19937.

Real MT19937 first-cycle outputs are emitted from a TWISTED state. The 128-row
negative here tests a narrower imaginary producer emitting the raw initialized
state directly; its synthetic positive does not validate standard seeded MT.
See Agent 2 corrected twist-aware original-state test
agents/agent2/k04_true_posttwist_mt_init_gate.py. Never loads selected coupon,
route mask, acceptance commitments or K08 evidence.
"""
import hashlib
import re
from pathlib import Path

MASK = 0xFFFFFFFF
A = 1812433253
SOURCE_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
REGULAR = re.compile(rb"^2026-10-03T.* JOB=PS-261003-(03\d\d|04[012]\d) ATTEMPT=1 STATE=ACK .*?PAYLOAD=([A-F0-9]{32}) ")


def inv_r(y, shift):
    x = y
    for _ in range(5):
        x = y ^ (x >> shift)
    return x & MASK


def inv_l(y, shift, bitmask):
    x = y
    for _ in range(8):
        x = y ^ ((x << shift) & bitmask)
    return x & MASK


def untemper(y):
    x = inv_r(y, 18)
    x = inv_l(x, 15, 0xEFC60000)
    x = inv_l(x, 7, 0x9D2C5680)
    return inv_r(x, 11)


def temper(x):
    y = x ^ (x >> 11)
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 15) & 0xEFC60000
    return (y ^ (y >> 18)) & MASK


def implied_indexes(payload, byteorder):
    words = [int.from_bytes(payload[j:j+4], byteorder) for j in range(0, 16, 4)]
    states = [untemper(y) for y in words]
    return tuple((states[j+1] - A * (states[j] ^ (states[j] >> 30))) & MASK for j in range(3))


def run(source):
    b = source.read_bytes()
    assert hashlib.sha256(b).hexdigest() == SOURCE_SHA
    rows = [bytes.fromhex(m.group(2).decode()) for line in b.splitlines()
            if (m := REGULAR.match(line))]
    assert len(rows) == 128, f"Unexpected regular row count: {len(rows)}"
    for orientation in ("big", "little"):
        first_possible = full_matches = 0
        for payload in rows:
            a, c, d = implied_indexes(payload, orientation)
            first_possible += (1 <= a <= 621)
            full_matches += (1 <= a <= 621 and c == a + 1 and d == a + 2)
        print(f"ORIGINAL {orientation}: rows={len(rows)}, initial-phase pair possible={first_possible}, full run compatible={full_matches}")
        assert full_matches == 0
    for seed in (0, 8131, 0x12345678, MASK):
        state = [seed]
        for i in range(1, 624):
            state.append((A * (state[-1] ^ (state[-1] >> 30)) + i) & MASK)
        for phase in (0, 17, 419, 620):
            for orientation in ("big", "little"):
                payload = b"".join(temper(x).to_bytes(4, orientation)
                                   for x in state[phase:phase+4])
                assert implied_indexes(payload, orientation) == (
                    phase + 1, phase + 2, phase + 3)
    print("Synthetic positive controls: 32/32 PASS")
    print("COUNTERFACTUAL untwisted direct-state output only. Standard C++ MT19937 not excluded by this experiment.")
    print("See agents/agent2/k04_true_posttwist_mt_init_gate.py for the corrected conditional test. K04 bits gained=0.")


if __name__ == "__main__":
    import sys

    path = (Path(sys.argv[1]) if len(sys.argv) > 1 else
            Path(__file__).resolve().parents[2] / "resources/evidence/print/spool-reconstruction.log")
    run(path)
