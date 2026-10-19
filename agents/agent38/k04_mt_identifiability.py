"""Constructive MT19937 underdetermination for 128 regular H-17 spool rows.

No acceptance hash and no true K04 target ever consulted. The generated models
are demonstrations of interpolation, not evidence the printer used MT19937.
"""
import hashlib
import random
import re
import sys
import zipfile

SPOOL = "evidence/print/spool-reconstruction.log"
SOURCE_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MASK32 = (1 << 32) - 1


def undo_right(y, shift):
    x = y
    for _ in range(6):
        x = y ^ (x >> shift)
    return x & MASK32


def undo_left_masked(y, shift, mask):
    x = y
    for _ in range(6):
        x = y ^ ((x << shift) & mask)
    return x & MASK32


def untemper(y):
    y = undo_right(y, 18)
    y = undo_left_masked(y, 15, 0xEFC60000)
    y = undo_left_masked(y, 7, 0x9D2C5680)
    return undo_right(y, 11)


def output_from_state(words, count):
    assert len(words) == 624
    r = random.Random()
    r.setstate((3, tuple(words + [0]), None))
    return [r.getrandbits(32) for _ in range(count)]


def source_words(path):
    with zipfile.ZipFile(path) as archive:
        raw = archive.read(SPOOL)
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA
    ordinary, tail = [], []
    for line in raw.decode("ascii").splitlines():
        match = re.search(r"PAYLOAD=([0-9A-F]{32})", line)
        if not match:
            continue
        payload = bytes.fromhex(match.group(1))
        words = [
            int.from_bytes(payload[k:k + 4], "little")
            for k in range(0, 16, 4)
        ]
        if line.startswith("2026-10-03T") and line.split()[0].endswith("Z"):
            tail.extend(words)
        else:
            ordinary.extend(words)
    assert len(ordinary) == 512 and len(tail) == 20
    return ordinary, tail


def run(path):
    training, withheld = source_words(path)
    head = [untemper(word) for word in training]
    model_zero = head + [0] * 112
    model_one = head + [MASK32] * 112
    output_zero = output_from_state(model_zero, 532)
    output_one = output_from_state(model_one, 532)
    assert output_zero[:512] == output_one[:512] == training
    assert output_zero[512:532] != output_one[512:532]
    # Deliberate retrofitting, not an out-of-sample prediction:
    model_retrofit = head + [untemper(word) for word in withheld] + [0] * 92
    assert output_from_state(model_retrofit, 532) == training + withheld
    print("ordinary words reproduced by competing states: 512/512")
    print("zero-fill tail:", [f"{x:08X}" for x in output_zero[512:516]])
    print("one-fill tail:", [f"{x:08X}" for x in output_one[512:516]])
    print("actual tail (not predicted):", [f"{x:08X}" for x in withheld[:4]])
    print("retrofit 532/532 exact using held-out words to set free state")
    print("128 regular payloads do not identify next 20 MT words")


if __name__ == "__main__":
    run(sys.argv[1])
