"""SFT: Source-only falsifier for unrestricted GF(2)-linear four-word printer state.

Execute this file with Python 3 from any working directory after placing it in
agents/agent3/ of workplace-v1. It reads no disputed late printer payload,
acceptance commitment, recovery mask, or keeper nonce. No dependencies.
"""
from __future__ import annotations

import hashlib
from functools import reduce
import random
import re
from pathlib import Path

SPOOL_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
EXPECTED_CONTRADICTION = 0x2742FF61
EXPECTED_WINDOW = 126
EXPECTED_INPUT_INDICES = [
    1, 3, 10, 12, 14, 15, 18, 20, 21, 22, 27, 31, 32, 33, 35, 36,
    37, 38, 39, 41, 42, 44, 45, 48, 49, 52, 55, 56, 58, 59, 62,
    63, 65, 67, 71, 74, 79, 84, 86, 87, 89, 91, 92, 93, 94, 95,
    97, 98, 101, 102, 103, 105, 108, 109, 111, 112, 114, 115,
    116, 117, 119, 120, 123, 124, 125, 126,
]


def input_vector(words: list[int], start: int) -> int:
    return sum(words[start + j] << (32 * j) for j in range(4))


def fit(words: list[int], count: int):
    """Fit every GF(2) linear 128-to-32 map, returning basis or contradiction."""
    basis = {}
    for t in range(count):
        x, y, certificate = input_vector(words, t), words[t + 4], 1 << t
        while x:
            pivot = x.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (x, y, certificate)
                break
            bx, by, bc = basis[pivot]
            x ^= bx
            y ^= by
            certificate ^= bc
        if not x and y:
            return basis, (t, certificate, y)
    return basis, None


def predict(basis: dict, x: int) -> int:
    y = 0
    while x:
        pivot = x.bit_length() - 1
        bx, by, _ = basis[pivot]
        x ^= bx
        y ^= by
    return y


def synthetic_check() -> None:
    random_source = random.Random(20261021)
    matrix_columns = [random_source.getrandbits(32) for _ in range(128)]

    def apply_matrix(x: int) -> int:
        result = 0
        while x:
            lowest = x & -x
            result ^= matrix_columns[lowest.bit_length() - 1]
            x ^= lowest
        return result

    source_words = [random_source.getrandbits(32) for _ in range(4)]
    for _ in range(196):
        source_words.append(apply_matrix(input_vector(source_words, len(source_words) - 4)))
    basis, contradiction = fit(source_words, 160)
    assert contradiction is None, contradiction
    predictions = [predict(basis, input_vector(source_words, t)) for t in range(160, 196)]
    actual = source_words[164:200]
    assert predictions == actual, "Synthetic held-out predictor was incorrect"
    print(f"SYNTHETIC_PASS: 36/36 withheld full 32-bit words, rank={len(basis)}")


def original_check() -> None:
    spool = Path(__file__).resolve().parents[2] / "resources" / "evidence" / "print" / "spool-reconstruction.log"
    text = spool.read_bytes()
    assert hashlib.sha256(text).hexdigest() == SPOOL_SHA256, "Original spool source changed"
    regular = []
    for line in text.decode("ascii").splitlines():
        # The selected late (18:02:00Z) row and all other late rows are
        # excluded before their PAYLOAD field is even parsed.
        if not line.startswith("2026-") or "+00:00" not in line.split(" ", 1)[0]:
            continue
        job = re.search(r"\bJOB=PS-261003-(\d+)\b", line)
        payload = re.search(r"\bPAYLOAD=([0-9A-F]{32})\b", line)
        assert job and payload
        regular.append((int(job[1]), bytes.fromhex(payload[1])))
    assert len(regular) == 128
    assert [job for job, _ in regular] == list(range(300, 428))
    words = [int.from_bytes(payload[j:j + 4], "big") for _, payload in regular for j in range(0, 16, 4)]
    assert len(words) == 512

    basis, contradiction = fit(words, 160)
    assert contradiction is not None, "Proposed unrestricted linear map unexpectedly fits"
    at, certificate, delta = contradiction
    selected = [i for i in range(160) if certificate >> i & 1]
    assert at == EXPECTED_WINDOW and delta == EXPECTED_CONTRADICTION
    assert selected == EXPECTED_INPUT_INDICES, "Exact source-only contradiction certificate changed"
    assert 0 == reduce(int.__xor__, (input_vector(words, t) for t in selected), 0)
    assert delta == reduce(int.__xor__, (words[t + 4] for t in selected), 0)
    # An affine constant is XORed once per witness window and cancels here.
    assert len(selected) % 2 == 0, "Affine offset would not cancel"
    print(f"ORIGINAL_CONTRADICTION: t={at}, prior_basis_rank={len(basis)}, "
          f"certificate_windows={len(selected)}, "
          f"predecessor_XOR=0x0, successor_XOR=0x{delta:08X}")
    print("UNRESTRICTED_HOMOGENEOUS_AND_AFFINE_FOUR_WORD_GF2_TRANSITION: EXCLUDED_FOR_CONTIGUOUS_SOURCE")
    print("AUTHENTIC_K04_BITS_RECOVERED: 0/128; AUTHENTIC_K08_WORDS: 0")


if __name__ == "__main__":
    synthetic_check()
    original_check()
