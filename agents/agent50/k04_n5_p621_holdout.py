"""K04: exact five-word CPython seed phase p621, 31-bit heldout exclusion.

Run: python agents/agent50/k04_n5_p621_holdout.py <original-case.zip>

Consumes only original intact printer rows3/10/34/41/64, original AX-7778
alignment and derived source states. Reads no selected printer row129, K04
mask, K08 final caption, REC8 commitment or original verifier.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent14"))
from k04_ax_seed_divisor_gate import (
    MASK, LATE, inverse_twist, initialized_pair, initialized_state,
    next_state, seed_word, source_window, untemper,
)
from k04_n5_three_window_seed import source_rows
from k04_n5_crossboundary_gate import bridge, previous


def twist(a, b):
    mixed = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return (mixed >> 1) ^ (0x9908B0DF if mixed & 1 else 0)


def derived(p, r10, r41, early, early_next_low31, late):
    assert p == 621
    s57, early_outputs, s56_high, s58_low = bridge(r10, r41, early)
    mixed = [inverse_twist(a, b) for a, b in zip(r10, r41)]
    x58_low_heldout = mixed[3] & 0x7FFFFFFF
    # The pair inversion uses only the first three mixed words here.
    # The fourth is reserved for an actual source-value prediction.
    j = p - 567
    keys = {}
    for index in (p + 1, p + 2):
        slot = (index - 1) % 5
        keys[slot] = (seed_word(*late[index-p-1:index-p+2], index)
                      - slot) & MASK
    assert set(keys) == {1, 2}

    candidates = []
    for upper in (0, 0x80000000):
        s58 = s58_low | upper
        s56 = previous(s57, s58, keys[2], j + 4, 5)
        if s56 & 0x80000000 != s56_high:
            continue
        s55 = previous(s56, s57, keys[1], j + 3, 5)
        s452 = early_outputs[0] ^ twist(s55, s56)
        index = j + 400
        slot = (index - 1) % 5
        assert (index, slot) == (454, 3)
        key3 = (seed_word(s452, early[0], early[1], index)
                - slot) & MASK
        s59 = next_state(s57, s58, key3, 59, 5)
        predicted = (early_next_low31 ^ twist(s58, s59)) & 0x7FFFFFFF
        candidates.append(dict(
            s58_upper=upper,
            key3=key3,
            s59=s59,
            predicted_heldout=predicted,
            source_heldout=x58_low_heldout,
            hit=predicted == x58_low_heldout,
        ))
    return candidates


def positives():
    count = 0
    for z in range(120):
        seed = sum(((0x4135AB07 + 0x9E3779B9*k + z*0x6427) & MASK)
                   << (32*k) for k in range(5))
        rng = random.Random(seed)
        s = initialized_state(seed)
        assert s == list(rng.getstate()[1][:624])
        outputs = [untemper(rng.getrandbits(32)) for _ in range(852)]
        p = 621
        candidates = derived(
            p, outputs[p-170:p-166], outputs[p+57:p+61],
            s[p-168:p-166], s[p-166] & 0x7FFFFFFF, s[p-1:p+3],
        )
        good = [c for c in candidates if c["s58_upper"] == s[58] & 0x80000000]
        assert len(good) == 1 and good[0]["hit"]
        assert good[0]["predicted_heldout"] == outputs[58] & 0x7FFFFFFF
        assert good[0]["key3"] == (seed >> 96) & MASK
        assert good[0]["s59"] == s[59]
        count += 1
    print("ACTUAL_CPYTHON_160BIT_SEEDED_POSITIVES_PASS", count)


def original(zip_path):
    rows = source_rows(zip_path)
    early, partial_early = source_window(zip_path)
    # Independent source-pin: row3->34 fifth inverse pair supplies
    # initialized S455.low31 (p=621), never used in branch/key derivation.
    later_partial = inverse_twist(rows[3][3], rows[34][2]) & 0x7FFFFFFF
    assert later_partial == 0x31FD69FC
    candidates = derived(621, rows[10], rows[41], early, partial_early, LATE)
    for c in candidates:
        print("S58_UPPER", c["s58_upper"] >> 31)
        print("DERIVED_KEY3", f'{c["key3"]:08X}')
        print("DERIVED_S59", f'{c["s59"]:08X}')
        print("PREDICTED_X58_LOW31", f'{c["predicted_heldout"]:08X}')
        print("ORIGINAL_X58_LOW31", f'{c["source_heldout"]:08X}')
        print("HELDOUT_MATCH", c["hit"])
    assert len(candidates) == 1
    assert candidates[0]["s58_upper"] == 0x80000000
    assert candidates[0]["key3"] == 0x9E407C4F
    assert candidates[0]["predicted_heldout"] == 0x7BC6D981
    assert candidates[0]["source_heldout"] == 0x16DF5138
    assert not candidates[0]["hit"]
    print("SOURCE_CONDITIONAL_n5_phase621_EXCLUDED")
    print("ORIGINAL_ACCEPTANCE_NOT_READ_K04_K08_MISSING")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python k04_n5_p621_holdout.py original-case.zip")
    positives()
    original(sys.argv[1])
