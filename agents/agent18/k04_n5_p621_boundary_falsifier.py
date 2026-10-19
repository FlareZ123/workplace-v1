"""K04 n=5 / absolute first-row34 phase p=621: boundary-aware source gate.

Standalone original-source test with existing Agent18 SHA-pinned MT helpers.
Run: python agents/agent18/k04_n5_p621_boundary_falsifier.py original.zip
Uses intact printer rows10/41, plus original-source early/late initialized
state windows. Does not touch disputed row129, masks, commitments or verifier.
"""
import random
import re
import struct
import sys
from zipfile import ZipFile

from k04_ax_31bit_seed_sieve import (
    M, inverse_pair, seed_word, source_words, untemper,
)
from k04_ax_backward_checkpoint_sieve import backward, twist

TOP = 0x80000000
LOW = 0x7FFFFFFF
P = 621


def test_boundary(early, late, r10, r41):
    """Derive complete S[55..57] state chain and predict X[54].top."""
    mixed = [inverse_pair(a, b) for a, b in zip(r10, r41)]
    # p621: four 227-separated row10/41 pairs invert to first-cycle
    # X[54].high, X[55..57] full and X[58].low31.
    x55 = (mixed[0] & LOW) | (mixed[1] & TOP)
    x56 = (mixed[1] & LOW) | (mixed[2] & TOP)
    x57 = (mixed[2] & LOW) | (mixed[3] & TOP)
    x54high = mixed[0] & TOP

    # First-cycle X56=S453 xor twist(S56,S57),
    # X57=S454 xor twist(S57,S58).
    a = inverse_pair(x56, early[0])   # S56.high, S57.low31
    b = inverse_pair(x57, early[1])   # S57.high, S58.low31
    s57 = (a & LOW) | (b & TOP)

    # Source-derived late initialized state S[620..623] fixes
    # KEY[1] at update 622 and KEY[2] at update 623 for n=5.
    k1 = (seed_word(late[0], late[1], late[2], 622) - 1) & M
    k2 = (seed_word(late[1], late[2], late[3], 623) - 2) & M

    candidates = []
    for high in (0, TOP):
        s58 = (b & LOW) | high
        s56 = backward(s58, s57, 58, k2, 2)
        if (s56 & TOP) != (a & TOP):
            continue  # independently recovered first-cycle S56.high
        s55 = backward(s57, s56, 57, k1, 1)
        s452 = x55 ^ twist(s55 >> 31, s56)
        s451 = backward(early[0], s452, 453, k2, 2)
        # First-cycle X54=S451 xor twist(S54,S55);
        # twist(...).high = S55.lowbit, independent of S54.
        predicted = ((s451 >> 31) ^ (s55 & 1)) << 31
        candidates.append({
            "s58_high": high, "s56": s56, "s55": s55,
            "s452": s452, "s451": s451,
            "x54_high_predicted": predicted,
            "x54_high_source": x54high,
            "matches": predicted == x54high,
        })
    return candidates


def synthetic():
    positives = 0
    for trial in range(100):
        seed = sum(
            ((0x9A12376B + j * 0x1FE312F + trial * 0x50B7) & M) << (32*j)
            for j in range(5)
        )
        state = random.Random(seed).getstate()[1][:624]
        rng = random.Random(seed)
        x = [untemper(rng.getrandbits(32)) for _ in range(P+231)]

        # Derive both initialized-state windows through actual *output*
        # inversions, not solely through CPython getstate introspection.
        middle = [inverse_pair(x[P+j], x[P+227+j]) for j in range(4)]
        previous = [(middle[j] & LOW) | (middle[j+1] & TOP)
                    for j in range(3)]
        early_mixed = [inverse_pair(previous[j], x[P-169+j])
                       for j in range(3)]
        early = [(early_mixed[j] & LOW) | (early_mixed[j+1] & TOP)
                 for j in range(2)]
        late_mixed = [inverse_pair(x[P-229+j], x[P-2+j])
                      for j in range(5)]
        late = [(late_mixed[j] & LOW) | (late_mixed[j+1] & TOP)
                for j in range(4)]
        assert early == list(state[453:455])
        assert late == list(state[620:624])

        cases = test_boundary(early, late, x[P-170:P-166], x[P+57:P+61])
        assert any(
            case["matches"] and
            case["s56"] == state[56] and
            case["s55"] == state[55] and
            case["s452"] == state[452] and
            case["s451"] == state[451]
            for case in cases
        ), (trial, cases)
        positives += 1
    assert positives == 100
    print("ACTUAL_CPYTHON_SEEDED_100_POSITIVE_CONTROLS_PASS")


def original(filename):
    early, _, late = source_words(filename)
    with ZipFile(filename) as archive:
        raw = archive.read("evidence/print/spool-reconstruction.log").decode()
    lines = [s for s in raw.splitlines() if s.startswith("2026-")]

    def row(index):
        assert index in (10, 41)
        payload = bytes.fromhex(
            re.search(r"PAYLOAD=([0-9A-F]{32})", lines[index]).group(1)
        )
        return [untemper(v) for v in struct.unpack("<4I", payload)]

    result = test_boundary(early, late, row(10), row(41))
    print("source_firstcycle_p", 621, "key_array_words", 5)
    print("surviving_S56_high_preconditions", len(result))
    for v in result:
        print("S58_MSB", v["s58_high"] >> 31,
              "S56", f'{v["s56"]:08X}',
              "S55", f'{v["s55"]:08X}',
              "S452", f'{v["s452"]:08X}',
              "S451", f'{v["s451"]:08X}',
              "X54_source_high", v["x54_high_source"] >> 31,
              "X54_predicted_high", v["x54_high_predicted"] >> 31)
    assert len(result) == 1
    assert result[0]["x54_high_source"] == 0
    assert result[0]["x54_high_predicted"] == TOP
    assert not any(v["matches"] for v in result)
    print("ORIGINAL_SOURCE_FIVE_WORD_PHASE_621_EXCLUDED")
    print("K04_K08_UNRECOVERED; ACCEPTANCE_UNREAD")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_n5_p621_boundary_falsifier.py case.zip")
    synthetic()
    original(sys.argv[1])
