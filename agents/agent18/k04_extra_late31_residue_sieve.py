"""K04 source-only extra late low31 initialized-state and residue sieve.

Usage: python agents/agent18/k04_extra_late31_residue_sieve.py original.zip

Requires the two existing Agent18 source-pinned SFT modules in this directory.
Reads only intact printer rows 3,10,34,64 plus the transfer audit. Selected
row129, acceptance.json, K04/K08 digests, route mask, nonce are never read.
"""
import hashlib
import random
import re
import struct
import sys
from zipfile import ZipFile

from k04_ax_31bit_seed_sieve import (
    BASE, M, forward, inverse_pair, seed_word, source_words, untemper,
)
from k04_ax_backward_checkpoint_sieve import (
    backward, source_extension, temper, twist,
)

LOW = 0x7FFFFFFF
SOURCE = "evidence/print/spool-reconstruction.log"
SOURCE_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def original_late_extra(filename):
    """Direct independent original printer pair: row3 word3, row34 word2."""
    with ZipFile(filename) as archive:
        raw = archive.read(SOURCE)
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA
    rows = [s for s in raw.decode().splitlines() if s.startswith("2026-")]
    assert len(rows) == 133

    def word(row, j):
        assert row in (3, 34)  # the selected row129 is never opened
        payload = bytes.fromhex(
            re.search(r"PAYLOAD=([0-9A-F]{32})", rows[row]).group(1)
        )
        return untemper(struct.unpack("<4I", payload)[j])

    prior = word(3, 3)
    next_cycle = word(34, 2)
    assert (prior, next_cycle) == (0xD47006FA, 0xCC8EB204)
    extra = inverse_pair(prior, next_cycle) & LOW
    assert extra == 0x31FD69FC
    return extra


def inferred_key_low31(phase, length, late, extra):
    """New S[p+3] low31, plus known S[p+1:p+3], implies key[p+2] low31."""
    index = phase + 3
    key_index = (index - 1) % length
    return (seed_word(late[2], late[3], extra, index) - key_index) & LOW


def forward_pass(phase, length, early, early_extra, late, late_extra):
    assert 396 <= phase <= 620
    a = (phase + 2) % length
    b = (phase - 167) % length
    assert a == b  # length divides 169
    key = inferred_key_low31(phase, length, late, late_extra)
    prediction = forward(early[0], early[1], phase - 166, key, b)
    return (prediction & LOW) == early_extra


def backward_pass(phase, length, early, earlier_high, late,
                  late_extra, x170, checkpoint):
    assert 397 <= phase <= 620
    a = (phase + 2) % length
    b = (phase - 168) % length
    assert a == b  # length divides 170
    partial_key = inferred_key_low31(phase, length, late, late_extra)
    for key_high in (0, 0x80000000):
        state_before = backward(
            early[1], early[0], phase - 167, partial_key | key_high, b
        )
        if (state_before & 0x80000000) != earlier_high:
            continue
        for bit_before in (0, 1):
            if (temper(x170 ^ twist(bit_before, state_before)) >> 16) == checkpoint:
                return True
    return False


def controls():
    checks = 0
    for length in (13, 169):
        seed = sum(
            ((j * 2654435761 + 0x12345678) & M) << (32 * j)
            for j in range(length)
        )
        state = random.Random(seed).getstate()[1][:624]
        for phase in (396, 400, 535, 584, 620):
            assert forward_pass(
                phase, length, state[phase-168:phase-166],
                state[phase-166] & LOW, state[phase-1:phase+3],
                state[phase+3] & LOW
            )
            checks += 1

    for length in (5, 10, 17, 34, 85, 170):
        seed = sum(
            ((j * 2654435761 + 0x12345678) & M) << (32 * j)
            for j in range(length)
        )
        state = random.Random(seed).getstate()[1][:624]
        generator = random.Random(seed)
        stream = [generator.getrandbits(32) for _ in range(621)]
        for phase in (397, 400, 535, 584, 620):
            assert backward_pass(
                phase, length, state[phase-168:phase-166],
                state[phase-169] & 0x80000000, state[phase-1:phase+3],
                state[phase+3] & LOW, untemper(stream[phase-170]),
                stream[phase-397] >> 16,
            )
            checks += 1
    assert checks == 40
    print("ACTUAL_PYTHON_SEEDED_CONTROLS_PASS", checks)


def main(filename):
    controls()
    early, early_extra, late = source_words(filename)
    late_extra = original_late_extra(filename)
    print("NEW_PRINTER_INITIALIZED_STATE_S_pplus3_low31", f"{late_extra:08X}")

    for length in (13, 169):
        matches = sum(forward_pass(p, length, early, early_extra, late,
                                   late_extra) for p in range(396, 621))
        print("PRINTER_ONLY", length, "phases", 225, "matches", matches)
        assert matches == 0

    earlier_high, checkpoint, x170 = source_extension(filename)
    for length in (5, 10, 17, 34, 85, 170):
        matches = sum(backward_pass(p, length, early, earlier_high, late,
                                    late_extra, x170, checkpoint)
                      for p in range(397, 621))
        print("PRINTER_PLUS_ORDERED_AX", length, "phases", 224,
              "matches", matches)
        assert matches == 0

    print("NO_K04_COUPON_OR_K08_CAPTION_RECOVERED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_extra_late31_residue_sieve.py case.zip")
    main(sys.argv[1])
