"""Source-only global MT19937 target observability for a supplied printer chronology.

Each input row_start is the first of four adjacent 32-bit MT output indexes.
The disputed selected row 129 is excluded before solving. No key commitment is read.
Standalone self-test by running the script without a source argument.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import struct
import sys
import zipfile
from pathlib import Path

SOURCE = "evidence/print/spool-reconstruction.log"
SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
A = 0x9908B0DF
MASK32 = 0xFFFFFFFF


def ur(y: int, shift: int) -> int:
    x = y
    for _ in range(6):
        x = y ^ (x >> shift)
    return x & MASK32


def ul(y: int, shift: int, mask: int) -> int:
    x = y
    for _ in range(6):
        x = y ^ ((x << shift) & mask)
    return x & MASK32


def untemper(y: int) -> int:
    return ur(ul(ul(ur(y, 18), 15, 0xEFC60000), 7, 0x9D2C5680), 11)


def temper(y: int) -> int:
    y ^= y >> 11
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 15) & 0xEFC60000
    y ^= y >> 18
    return y & MASK32


def source_rows(source: Path) -> list[list[int]]:
    with zipfile.ZipFile(source) as z:
        raw = z.read(SOURCE)
    assert hashlib.sha256(raw).hexdigest() == SHA
    rows = []
    for line in raw.splitlines():
        found = re.search(rb"PAYLOAD=([0-9A-F]{32})", line)
        if found:
            rows.append([untemper(w) for w in struct.unpack('<4I', bytes.fromhex(found.group(1).decode()))])
    assert len(rows) == 133
    rows[129] = []
    return rows


def state_expressions(max_pos: int) -> list[list[int]]:
    words = [[1 << (32 * t + b) for b in range(32)] for t in range(min(max_pos + 1, 624))]
    for t in range(624, max_pos + 1):
        p, n, m = words[t - 624], words[t - 623], words[t - 227]
        words.append([
            m[b] ^ (p[31] if b == 30 else n[b + 1] if b < 30 else 0) ^ (n[0] if (A >> b) & 1 else 0)
            for b in range(32)
        ])
    return words


def tempered_expressions(state: list[int]) -> list[int]:
    y = list(state)
    for direction, shift, mask in ((-1, 11, MASK32), (1, 7, 0x9D2C5680), (1, 15, 0xEFC60000), (-1, 18, MASK32)):
        z = list(y)
        for b in range(32):
            src = b - shift if direction == 1 else b + shift
            if 0 <= src < 32 and (mask >> b) & 1:
                z[b] ^= y[src]
        y = z
    return y


def solve_target(rows: list[list[int]], starts: list[int]) -> dict:
    if len(rows) != 133 or len(starts) != 133:
        raise ValueError("Must supply 133 rows and 133 start offsets")
    if starts[0] != 0 or any(not isinstance(s, int) for s in starts):
        raise ValueError("Starts must be nonnegative integers with s0=0")
    if any(starts[i + 1] < starts[i] + 4 for i in range(132)):
        raise ValueError("Four-output printer blocks may not overlap")
    if any(len(words) != (0 if r == 129 else 4) for r, words in enumerate(rows)):
        raise ValueError("Expected four source words per intact row and no selected row129 words")
    terms = state_expressions(max(s + 3 for s in starts))
    basis: dict[int, int] = {}

    def reduce(expr: int, value: int, working_basis: dict[int, int] | None = None) -> int:
        active_basis = basis if working_basis is None else working_basis
        v = (expr << 1) | (value & 1)
        while v:
            pivot = v.bit_length() - 1
            existing = active_basis.get(pivot)
            if existing is None:
                return v
            v ^= existing
        return 0

    observations = 0
    for r, words in enumerate(rows):
        for j, observed in enumerate(words):
            exprs = terms[starts[r] + j]
            for b, expr in enumerate(exprs):
                row = reduce(expr, observed >> b)
                if row == 1:
                    raise ValueError(f"Chronology conflicts with original MT state at spool row {r}, word {j}, bit {b}")
                if row:
                    basis[row.bit_length() - 1] = row
                observations += 1
    source_rank = len(basis)
    target_basis: dict[int, int] = dict(basis)
    fixed_bits: dict[int, int] = {}
    target_words = []
    for j in range(4):
        exprs = tempered_expressions(terms[starts[129] + j])
        for b, expr in enumerate(exprs):
            residual = reduce(expr, 0)
            target_bit = 32 * j + b
            if residual in (0, 1):
                fixed_bits[target_bit] = residual
            joint_residual = reduce(expr, 0, target_basis)
            if joint_residual > 1:
                target_basis[joint_residual.bit_length() - 1] = joint_residual
        val = sum(fixed_bits.get(32 * j + b, 0) << b for b in range(32))
        known = sum((32 * j + b in fixed_bits) << b for b in range(32))
        target_words.append({"word": j, "known_bit_mask": f"{known:08X}", "known_bit_value": f"{val:08X}"})
    return {"observed_source_bits": observations, "source_rank": source_rank,
            "target_rank_after_source": len(target_basis) - source_rank, "fixed_tempered_target_bits": len(fixed_bits),
            "selected_index": starts[129], "selected_words": target_words}


def test_quotient_rank_regression() -> None:
    """Two target expressions can add only one dimension modulo source constraints."""
    for known_bit in (0, 1):
        source_basis = {4: 0b10000 | known_bit}  # Original e3 equation, optionally affine.
        joint_basis = dict(source_basis)
        for expr in (0b101000, 0b100000):  # Targets e5 XOR e3, e5.
            row = expr << 1
            while row:
                pivot = row.bit_length() - 1
                existing = joint_basis.get(pivot)
                if existing is None:
                    if row > 1:
                        joint_basis[pivot] = row
                    break
                row ^= existing
        assert len(joint_basis) - len(source_basis) == 1
    print("Affine quotient regression PASS: correlated targets have rank one")


def test_synthetic() -> None:
    expected = {4: (128, 0), 5: (65, 58), 6: (32, 96), 7: (96, 32),
                8: (97, 28), 9: (65, 58), 10: (127, 0)}
    for separation, (expected_rank, expected_fixed) in expected.items():
        starts = [separation * i for i in range(133)]
        prng = random.Random(20261019)
        values = [untemper(prng.getrandbits(32)) for _ in range(starts[-1] + 4)]
        rows = [values[s:s + 4] for s in starts]
        ground_truth = [temper(w) for w in rows[129]]
        rows[129] = []
        result = solve_target(rows, starts)
        for item in result["selected_words"]:
            actual = ground_truth[item["word"]]
            mask = int(item["known_bit_mask"], 16)
            wanted = int(item["known_bit_value"], 16)
            assert actual & mask == wanted
        print("Comparison with prior rank fixture", separation, "previous", expected_rank, "joint", result["target_rank_after_source"], flush=True)
        assert result["fixed_tempered_target_bits"] == expected_fixed, result
        print('Seeded MT positive PASS', 'start_separation', separation,
              'target_rank', expected_rank, 'individually_fixed_bits', expected_fixed)


def main() -> None:
    test_quotient_rank_regression()
    test_synthetic()
    if len(sys.argv) == 3:
        original_zip = Path(sys.argv[1])
        starts = json.loads(Path(sys.argv[2]).read_text(encoding="utf8"))["row_starts"]
        result = solve_target(source_rows(original_zip), starts)
        print('Original source-only target projection', json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
