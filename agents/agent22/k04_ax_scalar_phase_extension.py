"""Source-only AX-7778 two-cycle scalar-seeded MT19937 exclusion.

Usage: python agents/agent22/k04_ax_scalar_phase_extension.py original-case.zip

Original selected row129, K04 mask, REC8 commitments and K08 text withheld.
Conditional group placements: printer row10 at p-170, row34 at p,
row64 at p+227. See Agent36/9 AX checkpoint bridges.
"""
import hashlib
import json
import random
import re
import struct
import sys
import zipfile

MASK = 0xFFFFFFFF
MAGIC = 0x9908B0DF
SPOOL_HASH = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
TRANSFER_HASH = "32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf"


def inverse(a, b):
    x = a ^ b
    parity = x >> 31
    return (((x ^ (MAGIC if parity else 0)) << 1) | parity) & MASK


def pair(left, right):
    halves = [inverse(a, b) for a, b in zip(left, right)]
    return [(halves[i] & 0x7FFFFFFF) | (halves[i + 1] & 0x80000000)
            for i in range(len(halves) - 1)]


def untemper(value):
    x = value
    for shift, mask, left in ((18, MASK, False),
                              (15, 0xEFC60000, True),
                              (7, 0x9D2C5680, True),
                              (11, MASK, False)):
        original = x
        for _ in range(6):
            x = (original ^ (((x << shift) & mask) if left else x >> shift)) & MASK
    return x


def temper(value):
    value ^= value >> 11
    value ^= (value << 7) & 0x9D2C5680
    value ^= (value << 15) & 0xEFC60000
    return (value ^ (value >> 18)) & MASK


def scalar_initial(seed):
    result = [seed & MASK]
    for i in range(1, 624):
        previous = result[-1]
        result.append((1812433253 * (previous ^ (previous >> 30)) + i) & MASK)
    return result


def python_initial(seed):
    key = []
    while seed:
        key.append(seed & MASK)
        seed >>= 32
    if not key:
        key = [0]
    state = scalar_initial(19650218)
    i, j = 1, 0
    for _ in range(max(624, len(key))):
        previous = state[i - 1]
        state[i] = ((state[i] ^ ((previous ^ (previous >> 30)) * 1664525))
                    + key[j] + j) & MASK
        i += 1
        j = (j + 1) % len(key)
        if i == 624:
            state[0] = state[623]
            i = 1
    for _ in range(623):
        previous = state[i - 1]
        state[i] = ((state[i] ^ ((previous ^ (previous >> 30)) * 1566083941))
                    - i) & MASK
        i += 1
        if i == 624:
            state[0] = state[623]
            i = 1
    state[0] = 0x80000000
    return state


def scalar_outputs(initial, count):
    state = initial.copy()
    result = []
    for number in range(count):
        i = number % 624
        if i == 0:
            for j in range(624):
                y = (state[j] & 0x80000000) | (state[(j + 1) % 624] & 0x7FFFFFFF)
                state[j] = (state[(j + 397) % 624] ^ (y >> 1)
                            ^ (MAGIC if y & 1 else 0)) & MASK
        result.append(state[i])
    return result


def two_cycle_pair(outputs, p):
    first_inverse = pair(outputs[p:p + 4], outputs[p + 227:p + 231])
    return pair(first_inverse, outputs[p - 169:p - 166])


def synthetic():
    phases = (396, 397, 535, 621, 624, 700, 789, 790)
    for p in phases:
        for seed in (0, 5489, 0xFFFFFFFF):
            state = scalar_initial(seed)
            outputs = scalar_outputs(state, p + 231)
            assert two_cycle_pair(outputs, p) == state[p - 168:p - 166], (p, seed)
        seed = (1 << 381) + 0x123456789ABCDEF
        state = python_initial(seed)
        rng = random.Random(seed)
        outputs = [untemper(rng.getrandbits(32)) for _ in range(p + 231)]
        assert two_cycle_pair(outputs, p) == state[p - 168:p - 166], p
    print("SYNTHETIC_TWO_CYCLE_32_CONTROLS_PASS")


def original(case):
    with zipfile.ZipFile(case) as archive:
        spool = archive.read("evidence/print/spool-reconstruction.log")
        transfer = archive.read("evidence/transfers/transfer-audit.jsonl")
    assert hashlib.sha256(spool).hexdigest() == SPOOL_HASH
    assert hashlib.sha256(transfer).hexdigest() == TRANSFER_HASH
    lines = [line for line in spool.decode().splitlines() if line.startswith("2026-")]
    assert len(lines) == 133

    def row(index):
        assert index in (10, 34, 64)
        value = re.search(r"PAYLOAD=([0-9A-F]{32})", lines[index]).group(1)
        return [untemper(word) for word in struct.unpack("<4I", bytes.fromhex(value))]

    ancestor = pair(row(34), row(64))
    assert ancestor == [0xBFD3ACA1, 0xEF2DD8BC, 0x611914B2]
    audit = [json.loads(line) for line in transfer.decode().splitlines()]
    chunks = sorted((rec for rec in audit if rec.get("kind") == "CHUNK"
                     and rec.get("transfer") == "AX-7778"),
                    key=lambda rec: (rec["seq"], rec["attempt"]))
    assert len(chunks) == 16
    for i, word in enumerate(ancestor):
        checkpoint = int.from_bytes(bytes.fromhex(chunks[11 + i]["checkpoint"]), "little")
        assert (temper(word) >> 16) == checkpoint

    initialized_pair = pair(ancestor, row(10)[1:])
    assert initialized_pair == [0x0A9DE247, 0xFBBBB07E]
    implied_index = (initialized_pair[1] - 1812433253 *
                     (initialized_pair[0] ^ (initialized_pair[0] >> 30))) & MASK
    assert implied_index == 0x29686B7B
    assert implied_index > 623

    print("SOURCE_TWO_CYCLE_INITIAL_PAIR", " ".join(f"{x:08X}" for x in initialized_pair))
    print("SOURCE_SCALAR_REQUIRED_REGISTER_INDEX", implied_index)
    print("SCALAR_INIT_FIRST_REGISTER_P_396_TO_790_NO_MATCH")
    print("SELECTED_ROW129_AND_ACCEPTANCE_WITHHELD")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python k04_ax_scalar_phase_extension.py original-case.zip")
    synthetic()
    original(sys.argv[1])
