"""Bounded K04 donor-fragment gate on one original-source-consistent MT layout.

Usage (from an installed checkout): python agents/agent21/k04_p955_donor17_sft.py case.zip
Read-only: row129, K04 digest, route mask, K08 wording all withheld.
The p955 single-MT chronology remains an unauthenticated counterfactual.
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agents" / "agent33"))
from k04_global_target_projection import (
    source_rows, state_expressions, tempered_expressions, temper, untemper,
)


def residual(basis: dict[int, int], expr: int, value: int = 0) -> int:
    v = (expr << 1) | (value & 1)
    while v and (pivot := v.bit_length() - 1) in basis:
        v ^= basis[pivot]
    return v


def insert(basis: dict[int, int], expr: int, value: int) -> None:
    v = residual(basis, expr, value)
    assert v != 1, "Source contradiction or inconsistent counterfactual fragment"
    if v:
        basis[v.bit_length() - 1] = v


def quotient(basis: dict[int, int], expressions: list[list[int]]) -> int:
    union = dict(basis)
    for word in expressions:
        for expr in word:
            v = residual(union, expr, 0)
            if v > 1:
                union[v.bit_length() - 1] = v
    return len(union) - len(basis)


def main(case_zip: Path) -> None:
    path = ROOT / "agents" / "agent5" / "k04_crosssource_six_vectors.json"
    starts = json.loads(path.read_text(encoding="utf-8"))["row_starts"]["955"]
    assert len(starts) == 133 and (starts[96], starts[97], starts[129]) == (721, 733, 955)
    assert starts[96] + 7 == starts[129] - 227

    # Agent33's original SHA-pinned reader removes selected row129 before analysis.
    observations = source_rows(case_zip)
    states = state_expressions(max(starts) + 3)
    original = {}
    for row, words in enumerate(observations):
        for j, printed_state in enumerate(words):
            for bit, expr in enumerate(states[starts[row] + j]):
                insert(original, expr, (printed_state >> bit) & 1)
    target = [tempered_expressions(states[starts[129] + j]) for j in range(4)]
    donor = tempered_expressions(states[starts[96] + 7])
    baseline = quotient(original, target)
    assert baseline == 128, baseline

    print("Original source rank:", len(original), "baseline unknown target bits:", baseline)
    assert len(original) == 15369

    families = {
        "tempered donor bit30": [30],
        "tempered donor bit15": [15],
        "tempered donor bits30 and15": [30, 15],
        "tempered donor highest16": list(range(31, 15, -1)),
        "tempered donor highest17": list(range(31, 14, -1)),
        "tempered donor highest20": list(range(31, 11, -1)),
    }
    expected = [128, 128, 127, 128, 127, 127]
    for (label, bits), rank in zip(families.items(), expected):
        augmented = dict(original)
        for bit in bits:
            insert(augmented, donor[bit], 0)
        got = quotient(augmented, target)
        assert got == rank, (label, got, rank)
        print(label, "new linear constraints", len(augmented) - len(original),
              "unknown target bits", got)
    oracle = dict(original)
    insert(oracle, states[starts[96] + 7][30], 0)
    assert quotient(oracle, target) == 127
    print("Untempered bit30 ideal positive control: one target parity fixed")

    # Convert the seven unprinted state-bit donors into the exact 32 native
    # *tempered* print bits needed to constrain four coupon parities.
    # This completion chooses free MT state variables as zero. It supplies no
    # historical donor values; it keeps artificial reads source-compatible.
    support30 = [bit for bit in range(32) if (untemper(1 << bit) >> 30) & 1]
    support31 = [bit for bit in range(32) if (untemper(1 << bit) >> 31) & 1]
    assert support30 == [15, 30]
    assert support31 == [2, 9, 16, 17, 20, 24, 27, 31]
    completion = 0
    for pivot in sorted(original):
        equation = original[pivot]
        other_vars = (equation >> 1) ^ (1 << (pivot - 1))
        bit = (equation & 1) ^ ((other_vars & completion).bit_count() & 1)
        completion |= bit << (pivot - 1)

    fragment_basis = dict(original)
    for j in range(4):
        middle = tempered_expressions(states[starts[96] + 7 + j])
        for bit in support30:
            expr = middle[bit]
            insert(fragment_basis, expr, (expr & completion).bit_count() & 1)
        if j:
            early = tempered_expressions(states[starts[43] + 3 + j])
            for bit in support31:
                expr = early[bit]
                insert(fragment_basis, expr, (expr & completion).bit_count() & 1)
        expected_rank = 127 - j
        assert quotient(fragment_basis, target) == expected_rank
        print("Native donor fragments through parity", j,
              "source-only hypothetical observed bits", len(fragment_basis) - len(original),
              "unknown target bits", expected_rank)

    # Independent true-MT stream positive controls, without any H-17 target data.
    for seed in (0, 17, 20261003, 314159, 0xC0FFEE):
        rng = random.Random(seed)
        stream = [untemper(rng.getrandbits(32)) for _ in range(960)]
        printed = temper(stream[955])
        target_parity = ((printed >> 30) ^ (printed >> 15)) & 1
        donor_parity = ((stream[728] >> 30) ^ (stream[331] >> 31)) & 1
        assert target_parity == donor_parity
    print("Five independent seeded MT parity controls: PASS")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
