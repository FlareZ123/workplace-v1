"""Exact K04 target-rank attack with two source-record metadata rejection samplers.

Run: python agents/agent38/k04_joint_sampler_target_rank.py original-case.zip

Conditional model: single MT19937 state stream, row44-row43 start distance
11, no extra draws from RECOVER tail row128->129->130, CPython-style
three-bit rejection selection of a 4-member CLASS array (index3 may alias
LABEL), two-bit rejection selection of 3 DEST labels. Source row129 and
all REC8 acceptance/routing values are withheld.
"""
import re
import sys
from pathlib import Path
from zipfile import ZipFile

AGENTS = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(AGENTS / "agent49"), str(AGENTS / "agent23")]
from k04_gf2_target_identifiability import (
    START, symbolic_words, elimination, gf2_rank, check_mt_recurrence,
)
from k04_mt_inverse_peel import groups, rows
from k04_mt_rowstart import SPOOL

def reduce_fully(vector, basis):
    """Canonical GF(2) quotient representative, reducing ALL known pivots.

    Unlike stopping at the first unconstrained leading bit, descend through
    the remaining pivot positions so that quotient ranks cannot be inflated.
    """
    rhs = 0
    residual = 0
    while vector:
        pivot = vector.bit_length() - 1
        if pivot in basis:
            equation, answer = basis[pivot]
            vector ^= equation
            rhs ^= answer
        else:
            bit = 1 << pivot
            residual |= bit
            vector ^= bit
    return residual, rhs

def temper_symbolic(bits):
    def right(value, shift):
        return value[shift:] + [0] * shift
    def left(value, shift, mask):
        return [value[i-shift] if i >= shift and mask & (1 << i)
                else 0 for i in range(32)]
    for shifted in (
        lambda x: right(x, 11),
        lambda x: left(x, 7, 0x9D2C5680),
        lambda x: left(x, 15, 0xEFC60000),
        lambda x: right(x, 18),
    ):
        other = shifted(bits)
        bits = [a ^ b for a, b in zip(bits, other)]
    return bits

def equations_for_sampler(codes, start, span, dest_code, class_code, split):
    """Split span hidden draws into DEST until accepted, then CLASS.

    DEST rejects top2=3, accepts named code. CLASS n=4 rejects top3 in
    4..7 (hence tempered top bit=1), then accepts a named code.
    """
    equations = []
    def fixed(position, value, width):
        for i in range(width):
            bit = 31 - i
            equations.append((codes[position][bit],
                              (value >> (width-i-1)) & 1))
    for position in range(start, start + split - 1):
        fixed(position, 3, 2)
    fixed(start + split - 1, dest_code, 2)
    for position in range(start + split, start + span - 1):
        equations.append((codes[position][31], 1))
    fixed(start + span - 1, class_code, 3)
    return equations

def main(source):
    check_mt_recurrence()
    words = rows(source)
    assert len(words) == 133 and words[129] == []
    anchors = groups(source, words)
    left = next(entries for entries in anchors.values()
                if (43, 0) in entries)
    right = next(entries for entries in anchors.values()
                 if (44, 0) in entries)
    with ZipFile(source) as archive:
        text = archive.read(SPOOL).decode()
    records = [line for line in text.splitlines() if line.startswith("2026-")]
    assert len(records) == 133
    labels = [(re.search(r"CLASS=([A-Z]+)", x).group(1),
               re.search(r"DEST=([a-z]+)", x).group(1))
              for x in records]
    assert (labels[43], labels[44], labels[96], labels[97]) == (
        ("STORES", "bench"), ("STORES", "desk"),
        ("RECOVER", "store"), ("LABEL", "store"),
    )

    # Original 42-witness anchored group equalities:
    # s128=s43+623, s130=s44+620, s97=s44+394, s96=s43+393.
    # Assuming no extra draws in both row128->129 and row129->130
    # forces s44-s43=11, g43=7 and g96=8.
    state = symbolic_words(692)
    entries = left + [(row, index + 11) for row, index in right]
    original = [
        (state[index + col][bit], (word >> bit) & 1)
        for row, index in entries for col, word in enumerate(words[row])
        for bit in range(32)
    ]
    basis, dependent = elimination(original)
    assert len(basis) == 1123 and dependent == 285
    target = [state[627+col][bit] for col in range(4) for bit in range(32)]
    assert gf2_rank([reduce_fully(v, basis)[0] for v in target]) == 128

    gap_words = list(range(4, 11)) + list(range(397, 405))
    codes = {index: temper_symbolic(state[index]) for index in gap_words}
    feasible = []
    for split43 in range(1, 7):
        first = equations_for_sampler(codes, 4, 7, 2, 1, split43)
        for split96 in range(1, 8):
            for label97_code in (0, 3):
                second = equations_for_sampler(
                    codes, 397, 8, 0, label97_code, split96
                )
                try:
                    expanded, _ = elimination(original + first + second)
                except AssertionError:
                    continue
                projection = [reduce_fully(v, expanded)[0] for v in target]
                rank = gf2_rank(projection)
                individually_fixed = sum(v == 0 for v in projection)
                feasible.append((
                    split43, split96, label97_code, len(expanded),
                    rank, individually_fixed,
                ))

    assert len(feasible) == 10, feasible
    assert {(a, b, c) for a, b, c, *_ in feasible} == {
        (a, 1, c) for a in range(1, 6) for c in (0, 3)
    }
    assert all(rank == 128 and fixed == 0
               for _, _, _, _, rank, fixed in feasible)
    print("row129_and_REC8_withheld", True)
    print("conditional_gap_s44_minus_s43", 11)
    print("conditional_target_position", 627)
    print("metadata_sampler_n_CLASS", 4)
    print("sampled_gap_43_to_44", 7)
    print("sampled_gap_96_to_97", 8)
    print("candidate_partitions", 84)
    print("consistent_partitions", len(feasible))
    print("surviving_CLASS97_codes", [0, 3])
    print("surviving_DEST96_first_draw", True)
    print("candidate_branch_target_rank", 128)
    print("candidate_branch_fixed_target_bits", 0)
    print("conditional_K04_coupon_still_free", True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_joint_sampler_target_rank.py original-case.zip")
    main(Path(sys.argv[1]))
