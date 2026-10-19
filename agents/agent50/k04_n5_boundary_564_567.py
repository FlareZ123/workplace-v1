"""Conditional CPython five-word-seed boundary cracking, original source only.

Run: python agents/agent50/k04_n5_boundary_564_567.py <original-case.zip>
Source-selected printer row129, original commitments, mask, nonce and
REC8 verifier are never loaded. Depends on existing Agent14 source-pinned
algebra, not its phase-range decision.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent14"))
from k04_ax_seed_divisor_gate import (
    MASK, LATE, inverse_twist, untemper, seed_word, source_window,
    recover_key_low31, initialized_state,
)
from k04_n5_three_window_seed import source_rows
from k04_n5_crossboundary_gate import bridge, previous


def edge567(r10, r41, earlier, late):
    # p=567: second-cycle row41 at X624..627.
    s3, x, s2high, s4low = bridge(r10, r41, earlier)
    i = 569
    key3 = (seed_word(*late[1:4], i) - 3) & MASK
    states = [(top, previous(s3, s4low | top, key3, 4, 5))
              for top in (0, 0x80000000)]
    return s3, s4low, s2high, key3, states


def edge564(r10, r41, earlier, early_next):
    # p=564: row41 X621, X622, X623, X624 straddles the twist.
    m = [inverse_twist(x, y) for x, y in zip(r10, r41)]
    s622 = (m[0] & 0x7FFFFFFF) | (m[1] & 0x80000000)
    s623 = (m[1] & 0x7FFFFFFF) | (m[2] & 0x80000000)
    s621top = m[0] & 0x80000000
    key2low = recover_key_low31(564, earlier, early_next, 5)
    states = [(top, previous(s622, s623, key2low | top, 623, 5))
              for top in (0, 0x80000000)]
    return s622, s623, s621top, key2low, states


def controls():
    hits = 0
    for z in range(32):
        seed = sum(((0x4135AB07 + 0x9E3779B9*k + z*0x6427) & MASK)
                   << (32*k) for k in range(5))
        rng = random.Random(seed)
        state = initialized_state(seed)
        assert state == list(rng.getstate()[1][:624])
        x = [untemper(rng.getrandbits(32)) for _ in range(628)]
        p = 567
        s3, s4low, s2top, k3, branches = edge567(
            x[p-170:p-166], x[p+57:p+61],
            state[p-168:p-166], state[p-1:p+3])
        assert s3 == state[3] and s4low == (state[4] & 0x7FFFFFFF)
        assert s2top == (state[2] & 0x80000000)
        assert k3 == ((seed >> 96) & MASK)
        assert (state[4] & 0x80000000, state[2]) in branches
        p = 564
        s622, s623, s621top, k2low, branches = edge564(
            x[p-170:p-166], x[p+57:p+61],
            state[p-168:p-166], state[p-166] & 0x7FFFFFFF)
        assert (s622, s623, s621top) == (
            state[622], state[623], state[621] & 0x80000000)
        assert k2low == ((seed >> 64) & 0x7FFFFFFF)
        assert state[621] in [s for _, s in branches]
        hits += 1
    print("ACTUAL_PYTHON_SEEDED_CONTROLS_PASS", hits, "for_each_phase")


def original(zip_path):
    rows = source_rows(zip_path)
    earlier, low31 = source_window(zip_path)
    # Preserve the original AX-7778 stream-alignment assumption.
    s3, s4low, s2top, key3, branches = edge567(
        rows[10], rows[41], earlier, LATE)
    print("p567 S3", f"{s3:08X}", "S4low", f"{s4low:08X}",
          "S2top", s2top >> 31, "KEY3", f"{key3:08X}")
    print("p567 branch S2", [(int(bool(t)), f"{v:08X}") for t, v in branches])
    assert not any((v & 0x80000000) == s2top for _, v in branches)
    print("p567 EXCLUDED for CPython init_by_array with n=5")
    s622, s623, s621top, k2low, branches = edge564(
        rows[10], rows[41], earlier, low31)
    surviving = [(int(bool(t)), f"{v:08X}") for t, v in branches
                 if (v & 0x80000000) == s621top]
    print("p564 S622", f"{s622:08X}", "S623", f"{s623:08X}",
          "S621top", s621top >> 31, "KEY2low", f"{k2low:08X}")
    print("p564 KEY2top / S621 surviving", surviving)
    assert surviving == [(1, "1CFE981A")]
    print("K04_K08_UNRESOLVED; NO_ACCEPTANCE_INPUTS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python k04_n5_boundary_564_567.py original.zip")
    controls()
    original(sys.argv[1])
