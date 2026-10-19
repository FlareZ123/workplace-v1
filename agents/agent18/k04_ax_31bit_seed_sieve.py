"""K04: cross-cycle CPython init-state 31-bit holdout, source only.

Run: python agents/agent18/k04_ax_31bit_seed_sieve.py original-case.zip

Reads only intact printer spool (SHA-256 pinned), never selected row129,
K04/K08 acceptance, mask, nonce, verifier, or draft caption.
"""
import hashlib
import random
import re
import struct
import sys
from zipfile import ZipFile

M = 0xFFFFFFFF
SOURCE = "evidence/print/spool-reconstruction.log"
SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
BASE = [19650218]
for i in range(1, 624):
    BASE.append((1812433253 * (BASE[-1] ^ (BASE[-1] >> 30)) + i) & M)


def untemper(value):
    word = value
    for shift, mask, left in (
        (18, M, False),
        (15, 0xEFC60000, True),
        (7, 0x9D2C5680, True),
        (11, M, False),
    ):
        baseline = word
        for _ in range(6):
            word = baseline ^ (
                ((word << shift) & mask) if left else word >> shift
            )
        word &= M
    return word


def inverse_pair(left, right):
    delta = left ^ right
    bit = delta >> 31
    return (((delta ^ (0x9908B0DF if bit else 0)) << 1) | bit) & M


def mixing(value, constant):
    return ((value ^ (value >> 30)) * constant) & M


def seed_word(a, b, c, index):
    prior = ((b + index - 1) ^ mixing(a, 1566083941)) & M
    current = ((c + index) ^ mixing(b, 1566083941)) & M
    return (current - (BASE[index] ^ mixing(prior, 1664525))) & M


def forward(a, b, index, key_word, key_index):
    prior = ((b + index - 1) ^ mixing(a, 1566083941)) & M
    mid = ((BASE[index] ^ mixing(prior, 1664525))
           + key_word + key_index) & M
    return ((mid ^ mixing(b, 1566083941)) - index) & M


def source_words(filename):
    with ZipFile(filename) as archive:
        raw = archive.read(SOURCE)
    assert hashlib.sha256(raw).hexdigest() == SHA
    lines = [
        line for line in raw.decode().splitlines()
        if line.startswith("2026-")
    ]
    assert len(lines) == 133

    def row(index):
        assert index != 129
        payload = bytes.fromhex(
            re.search(r"PAYLOAD=([A-F0-9]{32})", lines[index]).group(1)
        )
        return [untemper(word) for word in struct.unpack("<4I", payload)]

    r10, r34, r64 = row(10), row(34), row(64)
    pairs = [inverse_pair(r34[j], r64[j]) for j in range(4)]
    ancestors = [
        (pairs[j] & 0x7FFFFFFF) | (pairs[j + 1] & 0x80000000)
        for j in range(3)
    ]
    mixed = [inverse_pair(ancestors[j], r10[j + 1]) for j in range(3)]
    early = [
        (mixed[j] & 0x7FFFFFFF) | (mixed[j + 1] & 0x80000000)
        for j in range(2)
    ]
    assert early == [0x0A9DE247, 0xFBBBB07E]
    heldout_low31 = mixed[2] & 0x7FFFFFFF

    # Independent intact-source row3/34 first-cycle state quartet,
    # derived in agents/agent9/k04_ax7778_cycle_seed_bridge.py.
    late = [0x6CE0E225, 0xF4E8FCB2, 0xC517EB25, 0x7D3AAF35]
    assert heldout_low31 == 0x2A07F662
    return early, heldout_low31, late


def compatible(phase, key_length, early, heldout, late):
    known = {}
    for j in (2, 3):
        index = phase - 1 + j
        key_index = (index - 1) % key_length
        value = (seed_word(*late[j - 2:j + 1], index) - key_index) & M
        if key_index in known and known[key_index] != value:
            return False
        known[key_index] = value
    index = phase - 166
    key_index = (index - 1) % key_length
    if key_index not in known:
        return None
    value = forward(early[0], early[1], index, known[key_index], key_index)
    return value & 0x7FFFFFFF == heldout


def synthetic_controls():
    total = 0
    lengths = (1, 2, 3, 4, 6, 7, 8, 12, 14, 21, 24, 28, 42, 56, 84, 167, 168)
    for length in lengths:
        seed = sum(
            ((j * 2654435761 + 0x12345678) & M) << (32 * j)
            for j in range(length)
        )
        state = random.Random(seed).getstate()[1][:624]
        for phase in (535, 555, 584, 605, 621):
            assert compatible(
                phase, length, state[phase - 168:phase - 166],
                state[phase - 166] & 0x7FFFFFFF,
                state[phase - 1:phase + 3],
            ) is True, (phase, length)
            total += 1
    assert total == 85
    print("synthetic_controls_PASS", total)


def main(filename):
    early, heldout, late = source_words(filename)
    synthetic_controls()
    print("original_heldout_S_pminus166_low31", f"{heldout:08X}")
    tested = []
    for length in range(1, 170):
        checks = [
            compatible(phase, length, early, heldout, late)
            for phase in range(535, 622)
        ]
        informed = [result for result in checks if result is not None]
        if informed:
            matches = sum(informed)
            print(
                "seed_array_words", length,
                "phases", len(informed), "matches", matches
            )
            assert len(informed) == 87 and matches == 0
            tested.append(length)
    assert tested == [1, 2, 3, 4, 6, 7, 8, 12, 14, 21, 24,
                      28, 42, 56, 84, 167, 168]
    print("source_conditional_seed_lengths_EXCLUDED", len(tested))
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_ax_31bit_seed_sieve.py original-case.zip")
    main(sys.argv[1])
