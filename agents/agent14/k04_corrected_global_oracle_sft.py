"""Correct the rank of K04's hypothetical nonpayload MT high-bit oracle.

Run from the repository root:
    python agents/agent14/k04_corrected_global_oracle_sft.py [original-case.zip]

Reads the original intact printer source, omits selected row129, and never
reads original acceptance, mask, K08 or verification material. Stdlib only.
"""
import hashlib
import json
import random
import re
import struct
import sys
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MAG = 0x9908B0DF


class Rank:
    def __init__(self, equations=()):
        self.pivots = {}
        for vector in equations:
            self.add(vector)

    def add(self, vector):
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in self.pivots:
                self.pivots[pivot] = vector
                return 1
            vector ^= self.pivots[pivot]
        return 0

    def contains(self, vector):
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in self.pivots:
                return False
            vector ^= self.pivots[pivot]
        return True

    def quotient(self, targets):
        joined = Rank()
        joined.pivots = self.pivots.copy()
        before = len(joined.pivots)
        for vector in targets:
            joined.add(vector)
        return len(joined.pivots) - before


def terms(limit):
    state = [[1 << (32*i+b) for b in range(32)] for i in range(624)]
    for t in range(624, limit + 1):
        old, nxt, middle = state[t-624], state[t-623], state[t-227]
        state.append([
            middle[b]
            ^ (old[31] if b == 30 else nxt[b+1] if b < 30 else 0)
            ^ (nxt[0] if (MAG >> b) & 1 else 0)
            for b in range(32)
        ])
    return state


def temper(word):
    for direction, shift, mask in (
        (-1, 11, 0xFFFFFFFF),
        (1, 7, 0x9D2C5680),
        (1, 15, 0xEFC60000),
        (-1, 18, 0xFFFFFFFF),
    ):
        next_word = word.copy()
        for bit in range(32):
            source_bit = bit-shift if direction == 1 else bit+shift
            if 0 <= source_bit < 32 and (mask >> bit) & 1:
                next_word[bit] ^= word[source_bit]
        word = next_word
    return word


def untemper(y):
    y ^= y >> 18
    y ^= (y << 15) & 0xEFC60000
    for _ in range(7):
        y ^= (y << 7) & 0x9D2C5680
    for _ in range(3):
        y ^= y >> 11
    return y & 0xFFFFFFFF


def spool_bytes(path):
    if path is None:
        raw = (ROOT / "resources/evidence/print/spool-reconstruction.log").read_bytes()
    else:
        with ZipFile(path) as archive:
            raw = archive.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw).hexdigest() == SPOOL_SHA
    return raw


def verify_original_source(rows, starts):
    symbolic = terms(starts[-1] + 3)
    affine = {}
    for row, start in enumerate(starts):
        if row == 129:
            continue
        match = re.search(r"PAYLOAD=([0-9A-Fa-f]{32})", rows[row])
        assert match is not None
        packed = bytes.fromhex(match.group(1))
        for offset, raw_word in enumerate(struct.unpack("<4I", packed)):
            untempered = untemper(raw_word)
            for bit, expression in enumerate(symbolic[start + offset]):
                value = (untempered >> bit) & 1
                while expression:
                    pivot = expression.bit_length() - 1
                    if pivot not in affine:
                        affine[pivot] = expression, value
                        break
                    old, old_value = affine[pivot]
                    expression ^= old
                    value ^= old_value
                else:
                    assert value == 0, "Intact original source contradicts fixture"
    assert len(affine) == 15305
    print("ORIGINAL_SOURCE_SHA_PINNED rank=15305 contradictions=0")


def corrected_oracle(starts):
    symbolic = terms(starts[-1] + 3)
    source = Rank()
    intact = set()
    for row, first in enumerate(starts):
        if row == 129:
            continue
        for pos in range(first, first + 4):
            assert pos not in intact
            intact.add(pos)
            for expression in symbolic[pos]:
                source.add(expression)

    target_positions = set(range(starts[129], starts[129] + 4))
    target = [
        expression
        for pos in sorted(target_positions)
        for expression in temper(symbolic[pos])
    ]
    missing = [
        pos for pos in range(len(symbolic))
        if pos not in intact and pos not in target_positions
    ]

    table = []
    for width in (0, 2, 3, 8, 16, 20, 22, 24, 26, 28, 30, 31, 32):
        basis = Rank()
        basis.pivots = source.pivots.copy()
        for pos in missing:
            if width:
                for expression in temper(symbolic[pos])[-width:]:
                    basis.add(expression)
        rank = basis.quotient(target)
        fixed = sum(basis.contains(expression) for expression in target)
        table.append((width, len(basis.pivots), rank, fixed))
    return table


def published_method_counterexample():
    # This reproduces the incorrect second-stage elimination in Agent24's
    # target_rank: it does not re-reduce against source after each target XOR.
    source = {1: 0b0011}
    independent = {}
    for target in (0b0100, 0b0111):
        while target and target.bit_length() - 1 in source:
            target ^= source[target.bit_length() - 1]
        while target:
            pivot = target.bit_length() - 1
            if pivot not in independent:
                independent[pivot] = target
                break
            target ^= independent[pivot]
    assert len(independent) == 2
    assert Rank((0b0011,)).quotient((0b0100, 0b0111)) == 1
    print("MINIMAL_BUG_WITNESS published=2 corrected=1")


def synthetic_controls():
    generator = random.Random(0xC261003)
    for _ in range(256):
        source = [generator.getrandbits(9) for _ in range(generator.randrange(8))]
        target = [generator.getrandbits(9) for _ in range(generator.randrange(8))]
        def closure(items):
            result = {0}
            for value in items:
                result |= {existing ^ value for existing in list(result)}
            return result
        base, joined = closure(source), closure(source + target)
        assert len(joined) == len(base) * (1 << Rank(source).quotient(target))
    for _ in range(256):
        value = generator.getrandbits(32)
        symbolic = temper([1 << bit for bit in range(32)])
        result = sum(((((expression & value).bit_count() & 1) << bit))
                     for bit, expression in enumerate(symbolic))
        expected = value ^ (value >> 11)
        expected ^= (expected << 7) & 0x9D2C5680
        expected ^= (expected << 15) & 0xEFC60000
        expected ^= expected >> 18
        assert result == (expected & 0xFFFFFFFF)
    print("POSITIVE_CONTROLS GF2_span=256/256 MT_temper=256/256")


def main():
    fixture = json.loads((ROOT / "results/h17-k04-source-consistent-index955.json").read_text())
    starts = fixture["row_starts"]
    assert len(starts) == 133 and starts[129] == 955
    raw = spool_bytes(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
    rows = [line for line in raw.decode().splitlines() if "PAYLOAD=" in line]
    assert len(rows) == 133
    published_method_counterexample()
    synthetic_controls()
    verify_original_source(rows, starts)
    table = corrected_oracle(starts)
    assert table == [
        (0,15305,128,0), (2,15828,128,0), (3,16071,128,0),
        (8,17286,128,0), (16,19185,127,0), (20,19381,95,0),
        (22,19479,79,4), (24,19577,63,5), (26,19675,47,10),
        (28,19773,31,15), (30,19870,16,40), (31,19919,8,52),
        (32,19968,0,128),
    ], table
    for width, source_rank, quotient, individual in table:
        print("ORACLE", width, "augmented_rank", source_rank,
              "actual_target_quotient", quotient, "fixed_target_bits", individual)
    assert corrected_oracle([6*r for r in range(133)])[0][2:] == (32,96)
    print("SYNTHETIC_H6_96FIXED_32UNKNOWN PASS")
    print("NO_ACTUAL_ORACLE_VALUES; NO_ORIGINAL_K04_BITS_RECOVERED")


if __name__ == "__main__":
    main()
