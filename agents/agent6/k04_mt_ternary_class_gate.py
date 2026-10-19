"""K04 source-only MT gap closure and three-way printer-class selector probe.

Run: python agents/agent6/k04_mt_ternary_class_gate.py original-case.zip
Withholds row129 and never loads original REC8 commitments, mask or target.
Imports Agent23's source-hash-pinned witness and inverse-state routines.
"""
import re
import sys
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_inverse_peel import groups, inverse_twist, rows
from k04_mt_rowstart import SPOOL

ALL = 0xFFFFFFFF
MSB = 0x80000000
LO31 = 0x7FFFFFFF
LABEL_INDEX = {"LABEL": 0, "STORES": 1, "RECOVER": 2}


def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9D2C5680
    x ^= (x << 15) & 0xEFC60000
    x ^= x >> 18
    return x & ALL


def twist(x, y):
    z = (x & MSB) | (y & LO31)
    return ((z >> 1) ^ (0x9908B0DF if z & 1 else 0)) & ALL


def close_group(entries, word_rows):
    observed = {start + j: value
                for row, start in entries
                for j, value in enumerate(word_rows[row])}
    if not observed:
        return {}, 0
    state = {p: (ALL, x) for p, x in observed.items()}

    def set_bits(p, mask, value):
        oldmask, oldvalue = state.get(p, (0, 0))
        assert ((oldvalue ^ value) & (oldmask & mask)) == 0
        new = (oldmask | mask, oldvalue | (mask & value))
        changed = new != (oldmask, oldvalue)
        state[p] = new
        return changed

    for iteration in range(40):
        changes = 0
        for p in range(min(observed) - 624, max(observed) + 1):
            am, av = state.get(p, (0, 0))
            bm, bv = state.get(p + 1, (0, 0))
            cm, cv = state.get(p + 397, (0, 0))
            dm, dv = state.get(p + 624, (0, 0))
            if cm == dm == ALL:
                mixed = inverse_twist(cv ^ dv)
                changes += set_bits(p, MSB, mixed & MSB)
                changes += set_bits(p + 1, LO31, mixed & LO31)
            if am & MSB and bm & LO31 == LO31:
                delta = twist(av, bv)
                if cm == ALL:
                    changes += set_bits(p + 624, ALL, cv ^ delta)
                if dm == ALL:
                    changes += set_bits(p + 397, ALL, dv ^ delta)
        if changes == 0:
            break
    else:
        raise AssertionError("closure did not reach a fixed point")

    full = {p: value for p, (mask, value) in state.items() if mask == ALL}
    return full, len(full) - len(observed)


def main(source):
    with ZipFile(source) as archive:
        lines = [line for line in archive.read(SPOOL).decode().splitlines()
                 if line.startswith("2026-")]
    assert len(lines) == 133
    word_rows = rows(source)
    assert not word_rows[129], "selected ACK must be entirely withheld"
    clusters = groups(source, word_rows)
    observations = []
    reconstructed = 0
    tail = []
    for entries in clusters.values():
        full, increment = close_group(entries, word_rows)
        reconstructed += increment
        for row, start in entries:
            if start - 1 not in full:
                continue
            sample = temper(full[start - 1]) >> 29
            if row >= 128:
                tail.append((row, sample))
                continue
            label = re.search(r"CLASS=([A-Z]+)", lines[row]).group(1)
            rejected = []
            for gap in range(2, 9):
                if start - gap not in full:
                    break
                rejected.append(temper(full[start - gap]) >> 29)
            observations.append((row, label, sample, rejected))

    observations.sort()
    assert len(observations) == 12
    assert reconstructed == 65
    train, heldout = observations[:6], observations[6:]
    assert all(index == LABEL_INDEX[label] for _, label, index, _ in train)
    assert all(index == LABEL_INDEX[label] for _, label, index, _ in heldout)
    rejection_values = [x for _, _, _, xs in observations for x in xs]
    assert len(rejection_values) == 7
    assert all(3 <= value < 8 for value in rejection_values)
    assert (131, 3) in tail

    print("source_only", True, "withheld_selected_row", 129)
    print("inversely_and_forward_reconstructed_full_group_relative_words", reconstructed)
    for row, label, index, rejected in observations:
        print("regular_row", row, "class", label,
              "previous_output_top3", index,
              "earlier_rejection_values", rejected)
    print("class_mapping", LABEL_INDEX)
    print("first_six_fit", len(train), "of", len(train))
    print("chronological_last_six_heldout", len(heldout), "of", len(heldout))
    print("earlier_complete_rejection_words", len(rejection_values),
          "all_ge_three", True)
    print("tail_row131_preceding_word_top3", 3,
          "not_ordinary_class_draw_because_row130_to_131_is_contiguous")
    print("selection_mechanism", "HYPOTHESIS: three-bit draw 0/1/2 accepted, 3..7 rejected")
    print("K04_K08", "UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_mt_ternary_class_gate.py original-case.zip")
    main(Path(sys.argv[1]))
