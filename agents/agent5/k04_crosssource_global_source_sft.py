"""SFT: replay six source-integrated global K04 MT19937 geometries.

Requires original case ZIP and the repository's existing Agent4/Agent33
source-only modules. Reads no selected row129, acceptance commitment, mask,
K08 nonce or verifier. Conditional cross-device common-MT producer only.
"""
from __future__ import annotations

import base64
import json
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from agents.agent33.k04_global_target_projection import (
    source_rows,
    state_expressions,
    tempered_expressions,
    untemper,
)
from agents.agent4.k04_cross_source_rc17_trp import source_hits


def reduce(expr: int, bit: int, basis: dict[int, int]) -> int:
    row = (expr << 1) | (bit & 1)
    while row:
        pivot = row.bit_length() - 1
        existing = basis.get(pivot)
        if existing is None:
            break
        row ^= existing
    return row


def add(expr: int, bit: int, basis: dict[int, int]) -> int:
    row = reduce(expr, bit, basis)
    assert row != 1, "Original source contradiction"
    if row:
        basis[row.bit_length() - 1] = row
        return 1
    return 0


def replay(original: Path) -> None:
    compressed = (Path(__file__).with_name("k04_crosssource_six_vectors.b64")
                  .read_text(encoding="ascii"))
    fixture = json.loads(zlib.decompress(base64.b64decode(compressed)))
    assert fixture["source_spool_sha256"] == (
        "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
    )
    rows = source_rows(original)
    assert rows[129] == [] and len(rows) == 133
    independent_rows, hits = source_hits(original)
    assert independent_rows == rows and len(hits) == 9

    terms = state_expressions(1400)
    expectations = {950: (15366, 2), 951: (15365, 2), 952: (15367, 3),
                    953: (15368, 3), 954: (15365, 2), 955: (15369, 2)}
    for index, (expected_rank, expected_gain) in expectations.items():
        starts = fixture["row_starts"][str(index)]
        assert len(starts) == 133 and starts[0] == 0 and starts[129] == index
        assert all(
            starts[r + 1] >= starts[r] + (
                7 if r == 9 else 6 if r < 127 else 4
            )
            for r in range(132)
        )
        assert starts[131] - starts[130] == 4
        assert (starts[38] - starts[7], starts[59] - starts[28]) == (230, 226)
        assert (starts[40] - starts[9], starts[63] - starts[9],
                starts[124] - starts[9]) == (229, 398, 852)

        basis: dict[int, int] = {}
        for row, values in enumerate(rows):
            for word_index, original_word in enumerate(values):
                for bit, expr in enumerate(
                    terms[400 + starts[row] + word_index]
                ):
                    add(expr, (original_word >> bit) & 1, basis)
        printer_rank = len(basis)
        assert printer_rank == expected_rank

        for name, raw_hex, crc_ok, row, word_index, later, later_index in hits:
            assert starts[later] - starts[row] == (
                227 + word_index - later_index
            ), name
            independent_word = untemper(
                int.from_bytes(bytes.fromhex(raw_hex), "little")
            )
            predecessor = 400 + starts[row] + word_index - 396
            for bit, expr in enumerate(terms[predecessor]):
                add(expr, (independent_word >> bit) & 1, basis)
        extra_directions = len(basis) - printer_rank
        assert extra_directions == expected_gain

        joined = dict(basis)
        fixed_bits = 0
        for j in range(4):
            state = terms[400 + starts[129] + j]
            for expr in tempered_expressions(state):
                if reduce(expr, 0, basis) in (0, 1):
                    fixed_bits += 1
                add(expr, 0, joined)
        target_rank = len(joined) - len(basis)
        assert target_rank == 128 and fixed_bits == 0
        print(
            f"index={index} printer_rank={printer_rank} "
            f"cross_source_added_state_directions={extra_directions} "
            f"target_rank={target_rank} fixed_target_bits={fixed_bits}",
            flush=True,
        )
    print("PASS: six source-only fixtures; K04 0/128, K08 unrecovered")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Supply original H-17 ZIP as the sole argument")
    replay(Path(sys.argv[1]))
