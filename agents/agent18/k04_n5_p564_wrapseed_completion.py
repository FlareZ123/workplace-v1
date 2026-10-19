"""K04: p564 CPython 160-bit integer seed via first/second init-pass wrap.

Run: python agents/agent18/k04_n5_p564_wrapseed_completion.py original.zip

Read-only: original intact printer, selected row129 / all REC8 acceptance
sources excluded. Row33 first word is reserved as a new intact-source holdout.
Does not require AX checkpoint position10 adjacency in the producer stream.
"""
import hashlib
import random
import re
import struct
import sys
from zipfile import ZipFile

from k04_ax_31bit_seed_sieve import (
    BASE, M, inverse_pair, mixing, seed_word, source_words, untemper,
)
from k04_ax_backward_checkpoint_sieve import backward
from k04_extra_late31_residue_sieve import original_late_extra

TOP = 0x80000000
LOW = 0x7FFFFFFF
P = 564
SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def exact_seeds(early, early_extra, late, late_extra, r10, r41):
    """Recover four full n5 seed words, last partial word has two branches."""
    mixed = [inverse_pair(a, b) for a, b in zip(r10, r41)]
    s622 = (mixed[0] & LOW) | (mixed[1] & TOP)
    s623 = (mixed[1] & LOW) | (mixed[2] & TOP)
    x0 = (mixed[2] & LOW) | (mixed[3] & TOP)

    # CPython initial state[0] top must 1; this fixes S1.low31.
    s0s1 = inverse_pair(x0, early[1])
    if not (s0s1 & TOP):
        return []

    # The otherwise unspent fourth inversion gives X1.low31, and
    # S398.low31 fixes twist(S1,S2).low31.
    twist_low = (mixed[3] & LOW) ^ early_extra
    partials = [inverse_pair(twist_low | h, 0) for h in (0, TOP)]
    if (partials[0] & TOP) != (partials[1] & TOP):
        raise AssertionError("unexpected first-cycle top-bit ambiguity")
    s1 = (s0s1 & LOW) | (partials[0] & TOP)

    key2_low = (seed_word(early[0], early[1], early_extra, 398)-2) & LOW
    key2_options = [
        key2_low | h for h in (0, TOP)
        if (backward(s623, s622, 623, key2_low | h, 2) & TOP)
           == (mixed[0] & TOP)
    ]
    key4 = (seed_word(late[0],late[1],late[2],565)-4) & M
    key0 = seed_word(late[1],late[2],late[3],566) & M
    key1_low = (seed_word(late[2],late[3],late_extra,567)-1) & LOW

    # The first init_by_array pass executes 624 mixing iterations for
    # a five-word key. Its final iteration re-updates array index1
    # with KEY[623%5]=KEY[3], after copying array[623] into array[0].
    # The second pass ends by re-updating index1 once with S623.
    # Reverse that final update and the i623 update to reconstruct
    # P1 and P623, which then ALGORITHMICALLY DETERMINE KEY3.
    first1 = ((BASE[1] ^ mixing(BASE[0], 1664525)) + key0) & M
    firstpass_623 = (((s623 + 623) & M)
                     ^ mixing(s622, 1566083941)) & M
    firstpass_1 = (((s1 + 1) & M)
                   ^ mixing(s623, 1566083941)) & M
    key3 = (firstpass_1 - (first1 ^ mixing(firstpass_623, 1664525))
            - 3) & M

    return [
        (key0, key1_low | h, key2, key3, key4)
        for key2 in key2_options for h in (0, TOP)
    ]


def derive_windows(stream, phase):
    original = [inverse_pair(stream[phase+j], stream[phase+227+j])
                for j in range(4)]
    before = [(original[j] & LOW) | (original[j+1] & TOP)
              for j in range(3)]
    early_pair = [inverse_pair(before[j], stream[phase-169+j])
                  for j in range(3)]
    early = [(early_pair[j]&LOW)|(early_pair[j+1]&TOP)
             for j in range(2)]
    late_pair = [inverse_pair(stream[phase-229+j],stream[phase-2+j])
                 for j in range(5)]
    late = [(late_pair[j]&LOW)|(late_pair[j+1]&TOP)
            for j in range(4)]
    return early,early_pair[2]&LOW,late,late_pair[4]&LOW


def synthetic():
    positives = 0
    for trial in range(100):
        seed = sum(
            ((0x4135AB07+0x9E3779B9*j+trial*0x6427)&M) << (32*j)
            for j in range(5)
        )
        state = random.Random(seed).getstate()[1][:624]
        rng = random.Random(seed)
        output = [untemper(rng.getrandbits(32)) for _ in range(P+231)]
        early,early_extra,late,late_extra = derive_windows(output,P)
        assert early == list(state[396:398])
        assert late == list(state[563:567])
        keys = exact_seeds(
            early,early_extra,late,late_extra,
            output[P-170:P-166],output[P+57:P+61],
        )
        original_words = tuple((seed>>(32*j))&M for j in range(5))
        assert original_words in keys,(trial,original_words,keys)
        positives += 1
    assert positives == 100
    print("ACTUAL_PYTHON_160BIT_SEEDED_100_EXACT_RECOVERY_CONTROLS_PASS")


def original(filename):
    early,early_extra,late = source_words(filename)
    late_extra = original_late_extra(filename)
    with ZipFile(filename) as archive:
        raw = archive.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw).hexdigest() == SHA
    rows = [s for s in raw.decode().splitlines() if s.startswith("2026-")]
    assert len(rows) == 133

    def row(i):
        assert i in (10,33,41)
        v = bytes.fromhex(
            re.search(r"PAYLOAD=([0-9A-F]{32})",rows[i]).group(1)
        )
        return list(struct.unpack("<4I",v))

    candidates = exact_seeds(
        early,early_extra,late,late_extra,
        list(map(untemper,row(10))),list(map(untemper,row(41))),
    )
    assert len(candidates) == 2
    assert candidates == [
        (0x87C39456,0x14F6FDDB,0x9E2EBD55,0xC8216162,0x4F2A90C0),
        (0x87C39456,0x94F6FDDB,0x9E2EBD55,0xC8216162,0x4F2A90C0),
    ]
    # Independent intact row33 first output at offset p-6 is withheld
    # from every candidate-building equation above.
    heldout = row(33)[0]
    assert heldout == 0x8F4C954C
    predictions = []
    for words in candidates:
        seed = sum(w<<(32*j) for j,w in enumerate(words))
        rng = random.Random(seed)
        output = [rng.getrandbits(32) for _ in range(P-6+1)]
        predicted = output[P-6]
        predictions.append(predicted)
        print("KEY1_MSB",words[1]>>31,
              "ROW33_HELDOUT_PRED",f"{predicted:08X}",
              "ORIGINAL",f"{heldout:08X}",
              "MATCH",predicted==heldout)
    assert predictions == [0x14068D57,0x73DB8979]
    assert all(word != heldout for word in predictions)
    print("ORIGINAL_p564_n5_EXCLUDED_WITH_SOURCE_ONLY_HELDOUT")
    print("ALL_p396_TO_621_FIVE_WORD_PYTHON_FIRSTCYCLE_PHASES_EXCLUDED")
    print("K04_K08_UNRECOVERED; ACCEPTANCE_UNREAD")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_n5_p564_wrapseed_completion.py case.zip")
    synthetic()
    original(sys.argv[1])
