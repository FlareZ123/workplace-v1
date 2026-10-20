"""Source-heldout gate for the *conditional* .NET xoshiro128** printer model.

Official algorithm: dotnet/runtime Random.Xoshiro128StarStarImpl.cs, NextBytes.
No historical evidence establishes this producer; K04 row129 and commitments are
excluded from every calculation. This is a finite negative-source test.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

MASK = (1 << 32) - 1
INV5 = pow(5, -1, 1 << 32)
INV9 = pow(9, -1, 1 << 32)
SPOOL = Path(__file__).resolve().parents[2] / "resources/evidence/print/spool-reconstruction.log"
EXPECTED_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def rotl(word: int, shift: int) -> int:
    return ((word << shift) | (word >> (32 - shift))) & MASK


def rotr(word: int, shift: int) -> int:
    return ((word >> shift) | (word << (32 - shift))) & MASK


def observed_s1(output: int) -> int:
    return rotr((output * INV9) & MASK, 7) * INV5 & MASK


def advance(state: tuple[int, int, int, int]) -> tuple[tuple[int, int, int, int], int]:
    a, b, c, d = state
    value = rotl((b * 5) & MASK, 7) * 9 & MASK
    temp = (b << 9) & MASK
    c ^= a
    d ^= b
    b ^= c
    a ^= d
    c ^= temp
    d = rotl(d, 11)
    return (a, b, c, d), value


def emit(state: tuple[int, int, int, int], count: int) -> tuple[tuple[int, int, int, int], list[int]]:
    values: list[int] = []
    for _ in range(count):
        state, value = advance(state)
        values.append(value)
    return state, values


def two_rows(state: tuple[int, int, int, int], gap: int) -> list[int]:
    state, first = emit(state, 4)
    state, _ = emit(state, gap)
    _, second = emit(state, 4)
    return [observed_s1(v) for v in first + second]


def solve_initial_state(columns: list[list[int]], observed: list[int]) -> tuple[tuple[int, int, int, int] | None, int]:
    """Solve all 256 Boolean observations for the 128 initial state bits."""
    pivots: dict[int, tuple[int, int]] = {}
    rank = 0
    for bit in range(256):
        mask = sum(((columns[j][bit // 32] >> (bit % 32)) & 1) << j for j in range(128))
        rhs = (observed[bit // 32] >> (bit % 32)) & 1
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (mask, rhs)
                rank += 1
                break
            old_mask, old_rhs = pivots[pivot]
            mask ^= old_mask
            rhs ^= old_rhs
        else:
            if rhs:
                return None, rank
    assert rank == 128
    solution = 0
    for pivot in sorted(pivots):
        mask, rhs = pivots[pivot]
        value = rhs ^ ((mask & solution).bit_count() & 1)
        solution |= value << pivot
    return tuple((solution >> (32 * i)) & MASK for i in range(4)), rank


def columns_for(gap: int) -> list[list[int]]:
    return [
        two_rows(tuple(1 << (bit % 32) if i == bit // 32 else 0 for i in range(4)), gap)
        for bit in range(128)
    ]


def run() -> None:
    source = SPOOL.read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED_SHA256
    payloads = [bytes.fromhex(value.decode("ascii"))
                for value in re.findall(rb"PAYLOAD=([0-9A-F]{32})", source)]
    assert len(payloads) == 133
    regular = payloads[:128]

    state = tuple((index * 0x12345671 + 0xF19AF819) & MASK for index in range(1, 5))
    for gap in (0, 3, 16, 32):
        state2, first = emit(state, 4)
        state2, _ = emit(state2, gap)
        state2, second = emit(state2, 4)
        recovered, rank = solve_initial_state(
            columns_for(gap), [observed_s1(v) for v in first + second]
        )
        assert rank == 128 and recovered == state
        expected, _ = emit(state2, gap)
        predicted, _ = emit(recovered, 8 + gap)
        assert emit(expected, 4)[1] == emit(predicted, 4)[1]
        print(f"SYNTHETIC PASS gap={gap} rank={rank} exact_state=True heldout=True")

    for endian in ("little", "big"):
        observations = [
            observed_s1(int.from_bytes(payload[i:i + 4], endian))
            for payload in regular[:2] for i in range(0, 16, 4)
        ]
        valid: list[int] = []
        for gap in range(33):
            recovered, rank = solve_initial_state(columns_for(gap), observations)
            if recovered is not None:
                valid.append(gap)
            print(f"ORIGINAL endian={endian} gap={gap} rank_before_test_end={rank} consistent={recovered is not None}")
        assert not valid, (endian, valid)
    print("ORIGINAL PASS: 0/66 fixed-gap models agree with first two intact spool payloads")
    print("K04 selected target bytes: 0 recovered; original accepted key unchanged")


if __name__ == "__main__":
    run()
