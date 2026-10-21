"""Read-only late-ACK counterfactual GF(2) test, using original H-17 source ZIP.

Requires the six previously published, source-fitted row-start fixtures.
Run: python agents/agent42/k04_late_ack_counterfactual_sft.py SOURCE.zip agents/agent5/k04_crosssource_six_vectors.json
Original selected row129 PAYLOAD is deliberately never parsed.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
import zipfile
from pathlib import Path

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MAGIC = 0x9908B0DF


def untemper(x: int) -> int:
    x ^= x >> 18
    x ^= (x << 15) & 0xEFC60000
    for _ in range(7):
        x ^= (x << 7) & 0x9D2C5680
    for _ in range(3):
        x ^= x >> 11
    return x & 0xFFFFFFFF


def symbolic_state(length: int) -> list[list[int]]:
    state = [[1 << (i * 32 + bit) for bit in range(32)] for i in range(624)]
    for i in range(length - 624):
        a, b, c = state[i], state[i + 1], state[i + 397]
        state.append([
            c[k] ^ (a[31] if k == 30 else b[k + 1] if k < 30 else 0)
            ^ (b[0] if (MAGIC >> k) & 1 else 0)
            for k in range(32)
        ])
    return state


def put(basis: dict[int, tuple[int, int]], x: int, bit: int) -> bool:
    while x:
        pivot = x.bit_length() - 1
        if pivot not in basis:
            basis[pivot] = (x, bit)
            return True
        v, b = basis[pivot]
        x ^= v
        bit ^= b
    if bit:
        raise AssertionError("Source observation contradicts conditional geometry")
    return False


def residual(basis: dict[int, tuple[int, int]], x: int) -> tuple[int, int]:
    bit = 0
    while x:
        pivot = x.bit_length() - 1
        if pivot not in basis:
            break
        v, b = basis[pivot]
        x ^= v
        bit ^= b
    return x, bit


def read_original(path: Path) -> list[list[int] | None]:
    with zipfile.ZipFile(path) as z:
        raw = z.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw).hexdigest() == SPOOL_SHA
    lines = [line for line in raw.decode().splitlines() if "JOB=" in line]
    assert len(lines) == 133
    result: list[list[int] | None] = []
    for index, line in enumerate(lines):
        if index == 129:
            result.append(None)
            continue
        match = re.search(r"\bPAYLOAD=([0-9A-F]{32})\b", line)
        assert match is not None
        payload = bytes.fromhex(match.group(1))
        result.append([untemper(int.from_bytes(payload[j:j + 4], "little"))
                       for j in range(0, 16, 4)])
    return result


def check(
    starts: list[int], observed: list[list[int] | None],
    expressions: list[list[int]], heldout: int,
) -> tuple[int, int, int, int, str]:
    basis: dict[int, tuple[int, int]] = {}
    rank = 0
    for row, start in enumerate(starts):
        if row == 129 or row == heldout:
            continue
        words = observed[row]
        assert words is not None
        for j, word in enumerate(words):
            for bit in range(32):
                rank += put(basis, expressions[start + j][bit], (word >> bit) & 1)

    enlarged = basis.copy()
    quotient = fixed = mismatches = 0
    mask_parts = []
    withheld = observed[heldout]
    for j in range(4):
        mask = 0
        for bit, expression in enumerate(expressions[starts[heldout] + j]):
            left, predicted = residual(basis, expression)
            if left == 0:
                fixed += 1
                mask |= 1 << bit
                if withheld is not None:
                    mismatches += int(predicted != ((withheld[j] >> bit) & 1))
            actual = 0 if withheld is None else (withheld[j] >> bit) & 1
            quotient += put(enlarged, expression, actual)
        mask_parts.append(f"{mask:08X}")
    return rank, quotient, fixed, mismatches, " ".join(mask_parts)


def synthetic_positive(expressions: list[list[int]]) -> None:
    rng = random.Random(0x4A1791)
    actual = [untemper(rng.getrandbits(32)) for _ in range(len(expressions))]
    initial = sum(word << (32 * i) for i, word in enumerate(actual[:624]))
    for index in (624, 625, 700, 760):
        inferred = sum(((initial & expr).bit_count() & 1) << bit
                       for bit, expr in enumerate(expressions[index]))
        assert inferred == actual[index]
    print("seeded MT19937 synthetic recurrence control: PASS")


def main(source_zip: Path, fixture_path: Path) -> None:
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    assert fixture["source_spool_sha256"] == SPOOL_SHA
    layouts = fixture["row_starts"]
    assert set(layouts) == {str(x) for x in range(950, 956)}
    for position, starts in layouts.items():
        assert len(starts) == 133 and starts[129] == int(position)
    expressions = symbolic_state(max(max(starts) for starts in layouts.values()) + 4)
    synthetic_positive(expressions)
    observations = read_original(source_zip)

    expected = {128: (65, 63), 129: (128, 0), 130: (97, 31),
                131: (64, 64), 132: (65, 63)}
    for position, starts in sorted(layouts.items()):
        print(f"conditional source-fitted layout {position}")
        for row, (expected_rank, expected_fixed) in expected.items():
            rank, quotient, fixed, errors, masks = check(
                starts, observations, expressions, row
            )
            assert (quotient, fixed, errors) == (expected_rank, expected_fixed, 0)
            print(f"  withheld row {row}: intact source rank={rank}, "
                  f"target quotient={quotient}/128, fixed={fixed}, "
                  f"fixed-bit errors={errors}, masks={masks}")
    print("PASS: original selected row129 remains 128/128 free.")
    print("All analogue fixed bits are retrospective, not a blind physical prediction.")


if __name__ == "__main__":
    assert len(sys.argv) == 3
    main(Path(sys.argv[1]), Path(sys.argv[2]))
