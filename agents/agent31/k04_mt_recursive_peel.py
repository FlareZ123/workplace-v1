"""Recursive MT19937 inversion of the source-pinned H17 printer records.

Run: python agents/agent31/k04_mt_recursive_peel.py original-case.zip
Relies on Agent 23's 42-witness source-only row group discovery. Withholds
selected row129 throughout. Never reads a REC8 commitment, mask or K08 nonce.
"""
import sys
from pathlib import Path
from zipfile import ZipFile
import re

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_inverse_peel import rows, groups, inverse_twist
from k04_mt_rowstart import twist

ALL = 0xFFFFFFFF


def close_group(entries, values, withheld=None):
    observed = {}
    for row, offset in entries:
        for column, word in enumerate(values[row]):
            if (row, column) != withheld:
                position = offset + column
                assert position not in observed or observed[position] == word
                observed[position] = word
    state = {p: (ALL, word) for p, word in observed.items()}

    def add(p, mask, bits):
        old_mask, old_bits = state.get(p, (0, 0))
        assert not ((old_bits ^ bits) & old_mask & mask), ("inconsistent", p)
        if (old_mask | mask) == old_mask:
            return False
        state[p] = (old_mask | mask, old_bits | bits)
        return True

    while True:
        changed = False
        for end, (mask, value) in list(state.items()):
            middle = end - 227
            if mask == ALL and state.get(middle, (0, 0))[0] == ALL:
                mixed = inverse_twist(value ^ state[middle][1])
                first = end - 624
                changed |= add(first, 0x80000000, mixed & 0x80000000)
                changed |= add(first + 1, 0x7FFFFFFF, mixed & 0x7FFFFFFF)
        for first, (mask, value) in list(state.items()):
            if not mask & 0x80000000:
                continue
            successor = state.get(first + 1, (0, 0))
            middle = state.get(first + 397, (0, 0))
            end = state.get(first + 624, (0, 0))
            if successor[0] & 0x7FFFFFFF == 0x7FFFFFFF:
                delta = twist(value >> 31, successor[1])
                if middle[0] == ALL:
                    changed |= add(first + 624, ALL, middle[1] ^ delta)
                if end[0] == ALL:
                    changed |= add(first + 397, ALL, end[1] ^ delta)
        if not changed:
            break

    complete = {
        p: value for p, (mask, value) in state.items()
        if p not in observed and mask == ALL
    }
    return state, complete


def temper(value):
    value ^= value >> 11
    value ^= (value << 7) & 0x9D2C5680
    value ^= (value << 15) & 0xEFC60000
    value ^= value >> 18
    return value & ALL


def main(path):
    values = rows(path)
    assert not values[129]
    clusters = groups(path, values)
    recovered = sum(len(close_group(group, values)[1]) for group in clusters.values())
    assert recovered == 65, recovered

    tested = predicted = 0
    for entries in clusters.values():
        if len(entries) < 2:
            continue
        for row, offset in entries:
            for column, source_word in enumerate(values[row]):
                tested += 1
                state, _ = close_group(entries, values, (row, column))
                mask, candidate = state.get(offset + column, (0, 0))
                if mask == ALL:
                    predicted += 1
                    assert candidate == source_word, (row, column)
    assert (tested, predicted) == (264, 84), (tested, predicted)

    with ZipFile(path) as archive:
        lines = [line for line in archive.read("evidence/print/spool-reconstruction.log").decode().splitlines() if line.startswith("2026-")]
    assert len(lines) == 133
    immediately_before = []
    preceding_rejections = []
    earlier_rejections = []
    for entries in clusters.values():
        state, _ = close_group(entries, values)
        for row, start in entries:
            if row < 128 and state.get(start - 1, (0, 0))[0] == ALL:
                index = temper(state[start - 1][1]) >> 30
                label = re.search(r"CLASS=([A-Z]+)", lines[row]).group(1)
                assert index == int(label == "RECOVER"), (row, label, index)
                immediately_before.append((row, label, index))
                if state.get(start - 2, (0, 0))[0] == ALL:
                    preceding_rejections.append((row, temper(state[start - 2][1]) >> 30))
                if state.get(start - 3, (0, 0))[0] == ALL:
                    earlier_rejections.append((row, temper(state[start - 3][1]) >> 30))
    assert len(immediately_before) == 12 and all(x in (0, 1) for _, _, x in immediately_before)
    assert len(preceding_rejections) == 6 and all(x >= 2 for _, x in preceding_rejections)
    assert earlier_rejections == [(4, 3)]

    print("selected_row129_withheld", True)
    print("recursive_new_full_words", recovered, "previous_single_pass", 30)
    print("intact_word_holdouts", tested, "predicted", predicted, "mismatches", 0)
    print("regular_pre_payload_accepted_2bit", immediately_before)
    print("earlier_rejection_2bit", preceding_rejections)
    print("two_rejections_before_row", earlier_rejections)
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
