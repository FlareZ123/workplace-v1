"""K04: five-word CPython seed, p566, source-only first-cycle X1/X2/X3 gate.

Run: python agents/agent18/k04_n5_p566_source_only_falsifier.py original.zip

Only intact printer rows3/10/34/41/64 and prior source-pinned MT recurrence.
Does not read selected row129, AX position10, K04 acceptance, mask, K08, verifier.
"""
import hashlib
import random
import re
import struct
import sys
from zipfile import ZipFile

from k04_ax_31bit_seed_sieve import (
    M, inverse_pair, seed_word, source_words, untemper,
)
from k04_ax_backward_checkpoint_sieve import backward
from k04_extra_late31_residue_sieve import original_late_extra

TOP = 0x80000000
LOW = 0x7FFFFFFF
P = 566
SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def branches(early, early_extra, late, late_extra, r10, r41):
    """Enumerate all source-aligned early CPython init-by-array completions."""
    parts = [inverse_pair(a, b) for a, b in zip(r10, r41)]
    x0, x1, x2 = [
        (parts[j] & LOW) | (parts[j+1] & TOP)
        for j in range(3)
    ]
    x3_low = parts[3] & LOW

    # Late source gives 31 bits of the n5 KEY[3] used again at i=399,i=4.
    key_low = (seed_word(late[2], late[3], late_extra, 569) - 3) & LOW

    # X1=S398 xor twist(S1,S2); X2=S399 xor twist(S2,S3).
    a = inverse_pair(x1, early[0])
    b = inverse_pair(x2, early[1])
    s2 = (a & LOW) | (b & TOP)
    s3_low = b & LOW

    found = []
    for upper in (0, TOP):
        key3 = key_low | upper
        s397 = backward(early[1], early[0], 399, key3, 3)
        # First-cycle X0=S397 xor twist(S0.high,S1.low31).
        z0 = inverse_pair(s397, x0)
        if (z0 & TOP) != TOP:  # CPython initializes S0=0x80000000
            continue
        s1 = (a & TOP) | (z0 & LOW)

        # X3.low31 and independently source-derived S400.low31
        # leave only the bit31 of the twist result unobserved.
        for x3_upper in (0, TOP):
            v = inverse_pair(x3_low | x3_upper, early_extra)
            s3 = (v & TOP) | s3_low
            for s4_upper in (0, TOP):
                s4 = (v & LOW) | s4_upper
                # Ordinary second-pass update at i=4, safely past
                # CPython init loop's exceptional i=2/3 boundary.
                prediction = backward(s4, s3, 4, key3, 3)
                found.append({
                    "key3": key3, "s397": s397, "s1": s1,
                    "s2": s2, "s3": s3, "s4": s4,
                    "pred_s2": prediction, "pass": prediction == s2,
                })
    return found


def derive_windows(stream, phase):
    """Build input witnesses independently from seeded actual MT outputs."""
    first = [inverse_pair(stream[phase+j], stream[phase+227+j])
             for j in range(4)]
    ancestors = [(first[j]&LOW)|(first[j+1]&TOP) for j in range(3)]
    second = [inverse_pair(ancestors[j],stream[phase-169+j])
              for j in range(3)]
    early = [(second[j]&LOW)|(second[j+1]&TOP) for j in range(2)]
    third = [inverse_pair(stream[phase-229+j],stream[phase-2+j])
             for j in range(5)]
    late = [(third[j]&LOW)|(third[j+1]&TOP) for j in range(4)]
    return early, second[2]&LOW, late, third[4]&LOW


def synthetic():
    successes = 0
    for trial in range(100):
        seed = sum(
            ((0x9A12376B + 0x1FE312F*j + 0x50B7*trial) & M) << (32*j)
            for j in range(5)
        )
        state = random.Random(seed).getstate()[1][:624]
        generator = random.Random(seed)
        stream = [untemper(generator.getrandbits(32))
                  for _ in range(P+231)]
        early, early_extra, late, late_extra = derive_windows(stream, P)
        assert early == list(state[398:400])
        assert late == list(state[565:569])
        results = branches(
            early, early_extra, late, late_extra,
            stream[P-170:P-166], stream[P+57:P+61],
        )
        expected_key = (seed >> (32*3)) & M
        assert any(
            c["pass"] and c["key3"] == expected_key and
            all(c["s"+str(i)] == state[i] for i in (1,2,3,4))
            for c in results
        ), (trial, results)
        successes += 1
    assert successes == 100
    print("ACTUAL_PYTHON_160BIT_SEEDED_100_POSITIVE_CONTROLS_PASS")


def original(filename):
    early, early_extra, late = source_words(filename)
    late_extra = original_late_extra(filename)
    with ZipFile(filename) as archive:
        raw = archive.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw).hexdigest() == SHA
    rows = [s for s in raw.decode().splitlines() if s.startswith("2026-")]
    assert len(rows) == 133

    def row(i):
        assert i in (10, 41)
        payload = bytes.fromhex(
            re.search(r"PAYLOAD=([0-9A-F]{32})", rows[i]).group(1)
        )
        return [untemper(v) for v in struct.unpack("<4I", payload)]

    results = branches(early, early_extra, late, late_extra,
                       row(10), row(41))
    assert len(results) == 4
    assert {v["key3"] for v in results} == {0x1E1396A7}
    assert {v["s1"] for v in results} == {0x2849FF73}
    assert {v["s2"] for v in results} == {0xF1A6234C}
    assert {v["s3"] for v in results} == {0x2F1F9ABB}
    assert {v["pred_s2"] for v in results} == {
        0xE19A4FB2, 0x3687AC8B, 0xCDC8E15E, 0x22B63E37
    }
    assert not any(v["pass"] for v in results)
    print("SOURCE_p566_n5_ALL_FOUR_S4_BRANCHES_CONTRADICT_S2")
    for v in results:
        print("KEY3", f'{v["key3"]:08X}',
              "S4", f'{v["s4"]:08X}', "source_S2",
              f'{v["s2"]:08X}', "seed_predicted_S2",
              f'{v["pred_s2"]:08X}')
    print("K04_K08_MISSING; ACCEPTANCE_UNREAD")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_n5_p566_source_only_falsifier.py case.zip")
    synthetic()
    original(sys.argv[1])
