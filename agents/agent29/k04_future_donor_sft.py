"""Original-source K04 future-state donor leverage and paired witness test.

Run: python agents/agent29/k04_future_donor_sft.py original-case.zip
Uses a committed original-data-consistent index955 source chronology.
Never reads disputed row129 payload, any K04 XOR mask, any commitment, or K08.
"""
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from zipfile import ZipFile

MASK32 = 0xFFFFFFFF
TWIST = 0x9908B0DF
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
RECORDER_SHA = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
ORIGINAL_LAYOUT = Path(__file__).resolve().parents[2] / "results" / "h17-k04-source-consistent-index955.json"


def invert_right(x, shift):
    y = x
    for _ in range(5):
        y = x ^ (y >> shift)
    return y & MASK32


def invert_left(x, shift, mask):
    y = x
    for _ in range(5):
        y = x ^ ((y << shift) & mask)
    return y & MASK32


def untemper(x):
    return invert_right(invert_left(invert_left(invert_right(x, 18), 15, 0xEFC60000),
                                    7, 0x9D2C5680), 11)


def symbolic_mt(limit):
    expressions = [[1 << (32 * i + b) for b in range(32)] for i in range(624)]
    for t in range(limit - 623):
        first, next_word, middle = expressions[t], expressions[t + 1], expressions[t + 397]
        lsb = next_word[0]
        expressions.append([
            middle[b] ^
            (first[31] if b == 30 else next_word[b + 1] if b < 30 else 0) ^
            (lsb if TWIST & (1 << b) else 0)
            for b in range(32)
        ])
    return expressions


def add_equation(basis, vector, value):
    while vector:
        key = vector.bit_length() - 1
        existing = basis.get(key)
        if existing is None:
            basis[key] = (vector, value)
            return
        vector ^= existing[0]
        value ^= existing[1]
    assert value == 0, "original intact spool contradicts the declared chronology"


def infer_bit(basis, vector):
    result = 0
    while vector:
        existing = basis.get(vector.bit_length() - 1)
        if existing is None:
            return None
        vector ^= existing[0]
        result ^= existing[1]
    return result


def add_vector(basis, vector):
    while vector:
        key = vector.bit_length() - 1
        existing = basis.get(key)
        if existing is None:
            basis[key] = vector
            return 1
        vector ^= existing
    return 0


def fixed_mask(basis, expressions):
    mask = 0
    for b, x in enumerate(expressions):
        remainder = x
        while remainder:
            value = basis.get(remainder.bit_length() - 1)
            if value is None:
                break
            remainder ^= value
        if remainder == 0:
            mask |= 1 << b
    return mask


def original_source(archive):
    spool = archive.read("evidence/print/spool-reconstruction.log")
    recorder = archive.read("evidence/recorder/trip-recorder.raw")
    procedure = archive.read("evidence/procedures/RC-17-scans.txt").decode()
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    assert hashlib.sha256(recorder).hexdigest() == RECORDER_SHA
    lines = [line for line in spool.decode().splitlines() if line.startswith("2026-")]
    assert len(lines) == 133
    values = []
    for i, line in enumerate(lines):
        if i == 129:
            values.append(None)
            continue
        payload = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", line).group(1))
        values.append([untemper(x) for x in struct.unpack("<4I", payload)])
    return values, recorder, procedure


def external_controls(recorder, procedure):
    controls = []
    for i in range(88):
        record = recorder[16 + 24*i:16 + 24*(i + 1)]
        assert len(record) == 24
        controls.append((f"TRP2 row{i}", record[12:16]))
    for j, section in enumerate(procedure.split("\f")):
        match = re.search(r"Footer control strip: ([0-9A-F]{8})", section)
        if match:
            controls.append((f"RC17 section{j}", bytes.fromhex(match.group(1))))
    assert len(controls) == 100
    oriented = []
    for field_id, (label, raw) in enumerate(controls):
        for endian in ("little", "big"):
            oriented.append((field_id, label, endian, untemper(int.from_bytes(raw, endian))))
    return oriented


def main(zip_path):
    with ZipFile(zip_path) as archive:
        original_values, recorder, procedure = original_source(archive)
    with ORIGINAL_LAYOUT.open(encoding="utf-8") as f:
        fixture = json.load(f)
    starts = fixture["row_starts"]
    assert len(starts) == 133 and starts[129] == 955
    assert fixture["source_spool_sha256"] == SPOOL_SHA
    expressions = symbolic_mt(2250)
    basis = {}
    for row, start in enumerate(starts):
        if row == 129:
            continue
        for j in range(4):
            for b, equation in enumerate(expressions[start + j]):
                add_equation(basis, equation, (original_values[row][j] >> b) & 1)
    assert len(basis) == 15305
    print("all_528_intact_words_GF2_consistent", True, "source_rank", len(basis))
    coefficients = {k: entry[0] for k, entry in basis.items()}
    target = [bit for j in range(4) for bit in expressions[starts[129] + j]]
    initial_target = coefficients.copy()
    assert sum(add_vector(initial_target, bit) for bit in target) == 128

    informative = []
    for t in range(971, 2251):
        with_word = coefficients.copy()
        for bit in expressions[t]:
            add_vector(with_word, bit)
        masks = [fixed_mask(with_word, expressions[starts[129] + j]) for j in range(4)]
        if any(masks):
            informative.append((t, masks))
    expected = [
        (1185, [0, 0, 0, 0xBFFFFFFF]),
        (1411, [0, 0, 0x9FFFFFFF, 0]),
        (1412, [0, 0, 0, MASK32]),
        (1865, [0, 0, 0x9FFFFFFF, 0]),
        (1866, [0, 0, 0, MASK32]),
        (1974, [0x40000000, 0, 0, 0]),
    ]
    assert informative == expected, informative
    print("future_single_word_target_leverage", [(p, [f"{m:08X}" for m in masks])
                                                  for p, masks in informative])

    offset = {}
    for t, masks in informative:
        for word_j, mask in enumerate(masks):
            if not mask:
                continue
            known_mask = 0
            known_constant = 0
            for b in range(32):
                inferred = infer_bit(basis, expressions[t][b] ^ expressions[starts[129]+word_j][b])
                if inferred is not None:
                    known_mask |= 1 << b
                    known_constant |= inferred << b
            assert known_mask == mask
            offset[(t, word_j)] = (known_mask, known_constant)
            print("conditional_future_relation", t, word_j,
                  f"mask={known_mask:08X}", f"offset={known_constant:08X}")
    assert offset[(1412, 3)] == (MASK32, 0x24D1E0F2)
    assert offset[(1866, 3)] == (MASK32, 0x99F6810A)

    controls = external_controls(recorder, procedure)
    constraints = [
        (1412, 1866, 3), (1185, 1412, 3),
        (1185, 1866, 3), (1411, 1865, 2),
    ]
    for left, right, word_j in constraints:
        mask_a, value_a = offset[(left, word_j)]
        mask_b, value_b = offset[(right, word_j)]
        mask = mask_a & mask_b
        target_xor = (value_a ^ value_b) & mask
        matches = [
            (a[1], a[2], b[1], b[2])
            for i, a in enumerate(controls) for b in controls[i+1:]
            if a[0] != b[0] and ((a[3] ^ b[3]) & mask) == target_xor
        ]
        assert not matches, (left, right, matches)
        print("external_pair_fingerprint", left, right, f"mask={mask:08X}",
              f"xor={target_xor:08X}", "matches", len(matches))
    print("selected_row129_unread", True, "recovered_K04_bytes", 0)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
