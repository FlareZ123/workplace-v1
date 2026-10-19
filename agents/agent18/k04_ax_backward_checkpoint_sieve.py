"""K04 AX-7778 one-checkpoint backward short-residue seed-array exclusion.

Run: python agents/agent18/k04_ax_backward_checkpoint_sieve.py original-case.zip
Read-only original spool and transfer audit; no selected row129, REC8 hashes, mask, nonce.
Conditional on 16 AX checkpoint records having contiguous source MT indices.
"""
import hashlib
import json
import random
import re
import struct
import sys
from zipfile import ZipFile

from k04_ax_31bit_seed_sieve import (
    BASE, M, compatible, inverse_pair, mixing, seed_word,
    source_words, untemper,
)

TRANSFER = "evidence/transfers/transfer-audit.jsonl"
TRANSFER_SHA = "32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf"
INV1 = pow(1664525, -1, 1 << 32)
INV2 = pow(1566083941, -1, 1 << 32)


def inverse_xor(value):
    return value ^ (value >> 30)


def backward(current, prior, index, key, key_index):
    second = ((current + index) ^ mixing(prior, 1566083941)) & M
    first_mixed = (((second - key - key_index) & M) ^ BASE[index])
    first = inverse_xor((first_mixed * INV1) & M)
    original_mixed = first ^ ((prior + index - 1) & M)
    return inverse_xor((original_mixed * INV2) & M)


def twist(bit, next_word):
    mixed = ((bit & 1) << 31) | (next_word & 0x7FFFFFFF)
    return ((mixed >> 1) ^ (0x9908B0DF if mixed & 1 else 0)) & M


def temper(word):
    word ^= word >> 11
    word ^= (word << 7) & 0x9D2C5680
    word ^= (word << 15) & 0xEFC60000
    return (word ^ (word >> 18)) & M


def source_extension(filename):
    with ZipFile(filename) as archive:
        transfer_raw = archive.read(TRANSFER)
        assert hashlib.sha256(transfer_raw).hexdigest() == TRANSFER_SHA
        records = [json.loads(line) for line in transfer_raw.decode().splitlines()]
        spool = archive.read("evidence/print/spool-reconstruction.log").decode()
    lines = [line for line in spool.splitlines() if line.startswith("2026-")]

    def row(index):
        assert index in (10, 34, 64)
        payload = bytes.fromhex(
            re.search(r"PAYLOAD=([0-9A-F]{32})", lines[index]).group(1)
        )
        return [untemper(value) for value in struct.unpack("<4I", payload)]

    r10, r34, r64 = row(10), row(34), row(64)
    mixed = [inverse_pair(r34[j], r64[j]) for j in range(4)]
    predecessor = (mixed[0] & 0x7FFFFFFF) | (mixed[1] & 0x80000000)
    first_mixed = inverse_pair(predecessor, r10[1])
    original_early_highbit = first_mixed & 0x80000000

    checkpoints = sorted(
        (
            record for record in records
            if record.get("kind") == "CHUNK"
            and record.get("transfer") == "AX-7778"
        ),
        key=lambda record: (record["seq"], record["attempt"]),
    )
    assert len(checkpoints) == 16
    ax_checkpoint = int.from_bytes(
        bytes.fromhex(checkpoints[10]["checkpoint"]), "little"
    )
    assert checkpoints[10]["seq"] == 5 and checkpoints[10]["attempt"] == 1
    assert ax_checkpoint == 0x7A53
    return original_early_highbit, ax_checkpoint, r10[0]


def predict(phase, key_length, early, late, highbit, checkpoint, x170):
    assert key_length in (13, 169)
    keys = {}
    for j in (2, 3):
        index = phase - 1 + j
        key_index = (index - 1) % key_length
        keys[key_index] = (
            seed_word(*late[j - 2:j + 1], index) - key_index
        ) & M
    index = phase - 167
    key_index = (index - 1) % key_length
    assert key_index in keys

    before = backward(early[1], early[0], index, keys[key_index], key_index)
    highbit_match = (before & 0x80000000) == highbit
    checkpoint_match = any(
        (temper(x170 ^ twist(bit, before)) >> 16) == checkpoint
        for bit in (0, 1)
    )
    return highbit_match, checkpoint_match, before


def positives():
    for length in (13, 169):
        seed = sum(
            ((j * 2654435761 + 0x12345678) & M) << (32 * j)
            for j in range(length)
        )
        for phase in (535, 555, 584, 605, 621):
            state = random.Random(seed).getstate()[1][:624]
            generator = random.Random(seed)
            stream = [generator.getrandbits(32) for _ in range(phase - 169)]
            check = stream[phase - 397] >> 16
            x170 = untemper(stream[phase - 170])
            ok, checkpoint_ok, state_before = predict(
                phase, length, state[phase - 168:phase - 166],
                state[phase - 1:phase + 3],
                state[phase - 169] & 0x80000000, check, x170,
            )
            assert ok and checkpoint_ok and state_before == state[phase - 169]
    print("synthetic_backward_checkpoint_controls_PASS", 10)


def main(filename):
    early, _, late = source_words(filename)
    highbit, checkpoint, x170 = source_extension(filename)
    positives()
    for length in (13, 169):
        checks = [
            predict(phase, length, early, late, highbit, checkpoint, x170)
            for phase in range(535, 622)
        ]
        high_hits = sum(result[0] for result in checks)
        checkpoint_hits = sum(result[1] for result in checks)
        both = sum(result[0] and result[1] for result in checks)
        print(
            "seed_array_words", length, "phases", len(checks),
            "early_highbit_matches", high_hits,
            "AX_checkpoint_matches", checkpoint_hits,
            "joint_matches", both,
        )
        assert (high_hits, checkpoint_hits, both) == (49, 0, 0)
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_ax_backward_checkpoint_sieve.py original-case.zip")
    main(sys.argv[1])
