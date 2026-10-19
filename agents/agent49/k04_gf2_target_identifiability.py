"""Exact linear-state K04 recoverability test using only the two anchored MT groups.

Run: python agents/agent49/k04_gf2_target_identifiability.py original-case.zip
No routing, mask or REC8 commitment reads. Printer row129 fully withheld.
The MT recurrence is tested independently against CPython random.Random.
"""
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_inverse_peel import groups, rows
from k04_mt_rowstart import untemper

ALL = 0xFFFFFFFF
A = 0x9908B0DF
START = -229
STATE_BITS = 624 * 32


def twist(left, right):
    y = (left & 0x80000000) | (right & 0x7FFFFFFF)
    return (y >> 1) ^ (A if y & 1 else 0)


def check_mt_recurrence():
    for seed in (0, 1, 0x123456789ABCDEF):
        generator = random.Random(seed)
        x = [untemper(generator.getrandbits(32)) for _ in range(1300)]
        assert all(x[t + 624] == x[t + 397] ^ twist(x[t], x[t + 1])
                   for t in range(676))


def symbolic_words(last):
    # Each individual state bit is a GF(2) polynomial in the 19,968
    # free bits of an arbitrary 624-word MT stream starting at START.
    expression = {
        START + i: [1 << (32 * i + bit) for bit in range(32)]
        for i in range(624)
    }
    for output in range(START + 624, last + 1):
        t = output - 624
        middle, left, right = expression[t + 397], expression[t], expression[t + 1]
        expression[output] = [
            middle[bit]
            ^ (right[bit + 1] if bit < 30 else (left[31] if bit == 30 else 0))
            ^ (right[0] if (A >> bit) & 1 else 0)
            for bit in range(32)
        ]
    return expression


def elimination(equations):
    basis = {}
    dependent = 0
    for vector, rhs in equations:
        while vector:
            leading = vector.bit_length() - 1
            if leading not in basis:
                basis[leading] = (vector, rhs)
                break
            known, answer = basis[leading]
            vector ^= known
            rhs ^= answer
        else:
            assert not rhs, "MT constraint inconsistency"
            dependent += 1
    return basis, dependent


def reduce_expression(vector, basis):
    rhs = 0
    while vector:
        leading = vector.bit_length() - 1
        if leading not in basis:
            return vector, rhs
        known, answer = basis[leading]
        vector ^= known
        rhs ^= answer
    return 0, rhs


def gf2_rank(vectors):
    basis = {}
    for vector in vectors:
        while vector:
            leading = vector.bit_length() - 1
            if leading not in basis:
                basis[leading] = vector
                break
            vector ^= basis[leading]
    return len(basis)


def main(source):
    check_mt_recurrence()
    word_rows = rows(source)
    assert len(word_rows) == 133 and not word_rows[129]
    group_values = groups(source, word_rows)
    left = next(entries for entries in group_values.values()
                if any(row == 43 and offset == 0 for row, offset in entries))
    right = next(entries for entries in group_values.values()
                 if any(row == 44 and offset == 0 for row, offset in entries))
    assert len(left) == 5 and len(right) == 6
    assert min(offset for row, offset in left) == START
    expressions = symbolic_words(692)
    placements = 0
    for gap in range(11, 66):
        entries = left + [(row, offset + gap) for row, offset in right]
        equations = [
            (expressions[offset + column][bit], (word >> bit) & 1)
            for row, offset in entries
            for column, word in enumerate(word_rows[row])
            for bit in range(32)
        ]
        assert len(equations) == 44 * 32
        basis, dependent = elimination(equations)
        assert len(basis) == 1123 and dependent == 285

        # Positive controls: two inverse-reconstructed hidden row44
        # predecessors plus row44's originally intact first word.
        for position, expected in (
            (gap - 2, 0x27D820C7),
            (gap - 1, 0x0ACF4761),
            (gap, word_rows[44][0]),
        ):
            reduced = [reduce_expression(expr, basis)
                       for expr in expressions[position]]
            assert all(vector == 0 for vector, rhs in reduced)
            reconstructed = sum(rhs << bit
                                for bit, (vector, rhs) in enumerate(reduced))
            assert reconstructed == expected

        # Row128 starts at s43+623. Selected row129 has >=4 outputs,
        # and row130 starts at s44+620. Each candidate target begins
        # at s128+4 or later and ends at s130-1 or earlier.
        for selected_start in range(627, gap + 617):
            projections = [
                reduce_expression(expressions[selected_start + column][bit], basis)
                for column in range(4) for bit in range(32)
            ]
            assert all(coeff != 0 for coeff, rhs in projections)
            assert gf2_rank([coeff for coeff, rhs in projections]) == 128
            placements += 1
        print("gap", gap, "tested_selected_positions", gap - 10,
              "source_rank", len(basis), "target_rank", 128)
    assert placements == 1540
    print("source_only", True)
    print("selected_row129_withheld", True)
    print("distinct_position_hypotheses", placements)
    print("all_128_target_bits_independent_modulo_two_group_sources", True)
    print("scope", "arbitrary 624-word linear MT initial window; no seeding constraints")
    print("K04_K08_original_acceptance", "UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: k04_gf2_target_identifiability.py original-case.zip")
    main(Path(sys.argv[1]))
