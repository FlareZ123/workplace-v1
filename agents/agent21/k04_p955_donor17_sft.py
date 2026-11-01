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

    # New five-native-bit target parity from two separate original-epoch
    # source gaps: output X332 (10:35-10:40), output X728 (15:00-15:05).
    # This has only conditional source provenance, never observed donor bytes.
    assert observations[43][3] == 0x59E4D0B9
    assert (observations[43][3] >> 31) == 0
    two_donors = ((starts[43] + 4, (16, 17, 24)),
                  (starts[96] + 7, (23, 30)))
    assert two_donors[0][0] == 332 and two_donors[1][0] == 728
    five_bits = dict(original)
    for index, observed_bits in two_donors:
        native = tempered_expressions(states[index])
        for bit in observed_bits:
            expr = native[bit]
            insert(five_bits, expr, (expr & completion).bit_count() & 1)
    assert len(five_bits) - len(original) == 5
    assert quotient(five_bits, target) == 127
    assert residual(five_bits, target[0][23] ^ target[0][30]) in (0, 1)
    print("Two original-gap five-native-bit oracle: selected word0 bit23 XOR bit30 fixed")

    # Complete GF(2)-linear certificate: MT twist and temper are linear in
    # the three 32-bit predecessor state words.  Zero plus every one-hot
    # vector proves the five-printed-bit identity for *every* possible state.
    def exact_identity(previous: int, following: int, middle: int) -> bool:
        mix = ((previous & 0x80000000) | (following & 0x7FFFFFFF)) >> 1
        mix ^= 0x9908B0DF if following & 1 else 0
        selected = temper(middle ^ mix)
        early = temper(following)
        mid = temper(middle)
        left = ((selected >> 23) ^ (selected >> 30)) & 1
        right = ((early >> 16) ^ (early >> 17) ^ (early >> 24)
                 ^ (mid >> 23) ^ (mid >> 30) ^ (previous >> 31)) & 1
        return left == right

    basis_vectors = ([(0, 0, 0)]
                     + [(1 << b, 0, 0) for b in range(32)]
                     + [(0, 1 << b, 0) for b in range(32)]
                     + [(0, 0, 1 << b) for b in range(32)])
    assert len(basis_vectors) == 97
    assert all(exact_identity(*triple) for triple in basis_vectors)
    print("97/97 complete three-word GF(2) basis identities: PASS")

    # Independent true-MT stream positive controls, without any H-17 target data.
    for seed in (0, 17, 20261003, 314159, 0xC0FFEE):
        rng = random.Random(seed)
        stream = [untemper(rng.getrandbits(32)) for _ in range(960)]
        printed = temper(stream[955])
        target_parity = ((printed >> 30) ^ (printed >> 15)) & 1
        donor_parity = ((stream[728] >> 30) ^ (stream[331] >> 31)) & 1
        assert target_parity == donor_parity
        for p in range(950, 956):
            yi = temper(stream[p])
            early = temper(stream[p - 623])
            middle = temper(stream[p - 227])
            lhs = ((yi >> 23) ^ (yi >> 30)) & 1
            rhs = ((early >> 16) ^ (early >> 17) ^ (early >> 24)
                   ^ (middle >> 23) ^ (middle >> 30)
                   ^ (stream[p - 624] >> 31)) & 1
            assert lhs == rhs
    print("Five independent seeded MT parity controls × six indices: PASS")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
