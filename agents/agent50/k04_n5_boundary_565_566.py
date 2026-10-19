"""Boundary-aware CPython MT19937 K04 producer-phase sieve.

Run: python agents/agent50/k04_n5_boundary_565_566.py <original-case.zip>
Uses Agent14's intact source-pinned printer/AX alignments, never selected
printer row129, K04 mask, K08 caption, or any REC8 commitment.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent14"))
from k04_ax_seed_divisor_gate import (
    MASK, LATE, INITIAL, inverse_twist, initialized_state,
    untemper, source_window,
)
from k04_n5_three_window_seed import source_rows

MAGIC = 0x80000000
LENGTHS = (1, 2, 5, 10, 17, 34, 85, 170)


def mix(x, k):
    return ((x ^ (x >> 30)) * k) & MASK


def unmix(x, k):
    y = (x * pow(k, -1, 1 << 32)) & MASK
    return y ^ (y >> 30)


def partial_key(index, a, b, c_low, n):
    slot = (index - 1) % n
    first = ((b + index - 1) ^ mix(a, 1566083941)) & MASK
    base = INITIAL[index] ^ mix(first, 1664525)
    return (((((c_low + index) & 0x7FFFFFFF)
               ^ (mix(b, 1566083941) & 0x7FFFFFFF))
             - base - slot) & 0x7FFFFFFF)


def prior_state(b, c, key, index, n):
    slot = (index - 1) % n
    second = (c + index) ^ mix(b, 1566083941)
    first = unmix(INITIAL[index] ^ ((second - key - slot) & MASK),
                  1664525)
    return unmix(first ^ ((b + index - 1) & MASK), 1566083941)


def p565(r10, r41, early):
    mixed = [inverse_twist(a, b) for a, b in zip(r10, r41)]
    # At p565: row41 outputs X622..625 and mixed[1/2] straddle
    # X623 -> X624, jointly giving complete first-cycle X0.
    x0 = (mixed[1] & 0x7FFFFFFF) | (mixed[2] & MAGIC)
    # X0 = S397 xor twist(S0.high, S1.low31). CPython always sets
    # initialized S0 = 80000000; hence recovered twist input top=1.
    return x0, inverse_twist(early[0], x0)


def p566(r10, r41, early, late, late_next, n):
    assert 170 % n == 0
    mixed = [inverse_twist(a, b) for a, b in zip(r10, r41)]
    x0 = (mixed[0] & 0x7FFFFFFF) | (mixed[1] & MAGIC)
    # KEY[(569-1)%n] and KEY[(399-1)%n] coincide iff n | 170.
    key_low = partial_key(569, late[2], late[3], late_next, n)
    branches = []
    for upper in (0, MAGIC):
        s397 = prior_state(early[0], early[1], key_low | upper, 399, n)
        mixed0 = inverse_twist(s397, x0)
        branches.append((upper, s397, mixed0))
    return x0, key_low, branches


def controls():
    passes = 0
    for n in LENGTHS:
        for z in range(4):
            seed = sum(((0x32145AA7 + 0x12B37*k + z*0x871) & MASK)
                       << (32*k) for k in range(n))
            rng = random.Random(seed)
            s = initialized_state(seed)
            assert s == list(rng.getstate()[1][:624])
            x = [untemper(rng.getrandbits(32)) for _ in range(628)]
            phase = 565
            x0, v = p565(x[phase-170:phase-166],
                         x[phase+57:phase+61], s[phase-168:phase-166])
            assert x0 == x[0] and (v >> 31) == 1
            assert (v & 0x7FFFFFFF) == (s[1] & 0x7FFFFFFF)
            phase = 566
            x0, keylow, branches = p566(
                x[phase-170:phase-166], x[phase+57:phase+61],
                s[phase-168:phase-166], s[phase-1:phase+3],
                s[phase+3] & 0x7FFFFFFF, n)
            slot = 568 % n
            assert x0 == x[0] and keylow == ((seed >> (32*slot)) & 0x7FFFFFFF)
            assert ((seed >> (32*slot)) & MAGIC,
                    s[397], MAGIC | (s[1] & 0x7FFFFFFF)) in branches
            passes += 1
    print("ACTUAL_PYTHON_SEEDED_CONTROLS_PASS", passes, "per_phase")


def original(zip_path):
    rows = source_rows(zip_path)
    early, early_next = source_window(zip_path)
    late_next = inverse_twist(rows[3][3], rows[34][2]) & 0x7FFFFFFF
    assert late_next == 0x31FD69FC
    x0, v = p565(rows[10], rows[41], early)
    print("p565 X0", f"{x0:08X}", "twist_input", f"{v:08X}",
          "observed_S0_TOP", v >> 31, "required_CPython_S0_TOP", 1)
    assert (v >> 31) == 0
    print("p565 EXCLUDED for ALL CPython init_by_array key lengths")
    for n in LENGTHS:
        x0, keylow, branches = p566(rows[10], rows[41],
                                     early, LATE, late_next, n)
        survivors = [(int(bool(up)), f"{s397:08X}", f"{m:08X}")
                     for up, s397, m in branches if m & MAGIC]
        assert survivors == [(0, "F9A69445", "A849FF73")]
        print("p566 n", n, "key_slot", 568 % n,
              "key_low31", f"{keylow:08X}", "survivors", survivors)
    print("p566: conditional KEY upper=0; initialized S397=F9A69445, S1low31=2849FF73")
    print("K04_K08_UNRESOLVED; NO_ACCEPTANCE_INPUTS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python k04_n5_boundary_565_566.py original.zip")
    controls()
    original(sys.argv[1])
