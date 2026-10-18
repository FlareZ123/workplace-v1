"""SFT: verify the GF(2) XOR span of the original H-17 spool payloads.

Read-only source check. A full-rank span is not a printer recovery rule.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import operator
import re
from functools import reduce
from pathlib import Path
from zipfile import ZipFile

EXPECTED_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
ROW = re.compile(
    r"^(\S+) JOB=\S+ ATTEMPT=\d+ STATE=\w+ CLASS=\w+ "
    r"PAYLOAD=([0-9A-F]{32}) DEST=\w+$"
)


def load_spool(source: Path) -> bytes:
    if source.is_file() and source.suffix.lower() == ".zip":
        with ZipFile(source) as archive:
            return archive.read("evidence/print/spool-reconstruction.log")
    if source.is_dir():
        return (source / "evidence/print/spool-reconstruction.log").read_bytes()
    return source.read_bytes()


def parse(source: bytes) -> tuple[list[int], list[int], list[int]]:
    all_rows: list[int] = []
    regular: list[int] = []
    tail: list[int] = []
    for line in source.decode("ascii").splitlines():
        if line.startswith("#"):
            continue
        match = ROW.fullmatch(line)
        if match is None:
            raise ValueError(f"Unexpected source spool line: {line[:80]}")
        timestamp, hex_value = match.groups()
        value = int(hex_value, 16)
        all_rows.append(value)
        if timestamp.endswith("+00:00"):
            regular.append(value)
        elif timestamp.endswith("Z"):
            tail.append(value)
        else:
            raise ValueError(f"Unexpected source timestamp: {timestamp}")
    if (len(all_rows), len(regular), len(tail)) != (133, 128, 5):
        raise ValueError("Expected 128 regular and five tail original printer rows")
    return all_rows, regular, tail


def basis(values: list[int]) -> dict[int, tuple[int, int]]:
    """MSB-oriented elimination with a witness row-selection bitmask."""
    pivot: dict[int, tuple[int, int]] = {}
    for index, original in enumerate(values):
        word = original
        selection = 1 << index
        while word:
            lead = word.bit_length() - 1
            if lead not in pivot:
                pivot[lead] = (word, selection)
                break
            word ^= pivot[lead][0]
            selection ^= pivot[lead][1]
    return pivot


def independent_rank(values: list[int]) -> int:
    """Different LSB-first row-swapping elimination cross-check."""
    matrix = values[:]
    rank = 0
    for bit in range(128):
        pivot = next((i for i in range(rank, len(matrix))
                      if (matrix[i] >> bit) & 1), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for i in range(rank + 1, len(matrix)):
            if (matrix[i] >> bit) & 1:
                matrix[i] ^= matrix[rank]
        rank += 1
    return rank


def witness(target: int, pivots: dict[int, tuple[int, int]]) -> int:
    selected = 0
    while target:
        value, selection = pivots[target.bit_length() - 1]
        target ^= value
        selected ^= selection
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path,
                        default=Path(__file__).resolve().parents[1] / "resources")
    args = parser.parse_args()
    raw = load_spool(args.source)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("Source spool checksum changed")
    all_rows, regular, tail = parse(raw)
    ranks = {
        "regular_128": len(basis(regular)),
        "tail_5": len(basis(tail)),
        "all_133": len(basis(all_rows)),
    }
    for label, values in (
        ("regular_128", regular), ("tail_5", tail), ("all_133", all_rows)
    ):
        assert ranks[label] == independent_rank(values)
    assert ranks == {"regular_128": 128, "tail_5": 5, "all_133": 128}

    # Completely unrelated, predeclared synthetic target; no acceptance search.
    target = int.from_bytes(
        hashlib.sha256(b"independent XOR span control, NOT a coupon").digest()[:16],
        "big",
    )
    chosen = witness(target, basis(regular))
    actual = reduce(operator.xor,
                    (v for i, v in enumerate(regular) if (chosen >> i) & 1), 0)
    assert actual == target
    print(json.dumps({
        "source_sha256": digest,
        "row_counts": {"regular": 128, "tail": 5, "all": 133},
        "gf2_ranks": ranks,
        "kernel_dimension_all_rows": len(all_rows) - ranks["all_133"],
        "xor_subsets_per_target_all_rows": 2 ** (len(all_rows) - ranks["all_133"]),
        "synthetic_control": "PASS",
        "synthetic_control_subset_size": chosen.bit_count(),
        "K04_recovered": False,
    }, indent=2))


if __name__ == "__main__":
    main()
