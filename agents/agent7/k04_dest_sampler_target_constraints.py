"""K04 original-source DEST rejection sampler and ancestor-window gate.

Run: python agents/agent7/k04_dest_sampler_target_constraints.py original-case.zip
Reads unchanged SHA-pinned printer spool via existing Agent23/6 modules.
Withholds selected row129 payload. Does not access commitments, XOR mask,
K08 nonce/caption, or verifier.
"""
from itertools import product
from pathlib import Path
import re
import sys
from zipfile import ZipFile

root = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(root / "agent23"), str(root / "agent6")]
from k04_mt_inverse_peel import groups, rows
from k04_mt_ternary_class_gate import close_group, temper
from k04_mt_rowstart import SPOOL

DEST = {0: "store", 1: "desk", 2: "bench"}


def reconstructed(source):
    with ZipFile(source) as archive:
        originals = [line for line in archive.read(SPOOL).decode().splitlines()
                     if line.startswith("2026-")]
    assert len(originals) == 133
    labels = [
        (re.search(r"CLASS=([A-Z]+)", line).group(1),
         re.search(r"DEST=([a-z]+)", line).group(1))
        for line in originals
    ]
    words = rows(source)
    assert len(words) == 133 and words[129] == []
    observed = {}
    count = 0
    for entries in groups(source, words).values():
        full, increment = close_group(entries, words)
        count += increment
        for row, start in entries:
            observed[row] = (start, full)
    assert count == 65
    return labels, observed


def dest_observations(labels, indexed):
    resolved, unresolved = [], []
    for row, (start, full) in indexed.items():
        if row >= 128 or start + 4 not in full:
            continue
        seen = []
        for step in range(4, 12):
            if start + step not in full:
                break
            code = temper(full[start + step]) >> 30
            seen.append(code)
            if code != 3:
                break
        if seen[-1] == 3:
            unresolved.append((row, labels[row][1], seen))
        else:
            resolved.append((row, labels[row][1], seen, DEST[seen[-1]]))
    resolved.sort()
    unresolved.sort()
    assert len(resolved) == 13 and len(unresolved) == 4
    assert {row for row, *_ in resolved} == {
        53, 80, 82, 83, 84, 92, 95, 96, 97, 98, 99, 116, 126}
    assert all(label == prediction for _, label, _, prediction in resolved)
    assert [x for x in resolved if x[0] == 83][0][2] == [3, 2]
    assert [x for x in unresolved if x[0] == 94][0][2] == [3, 3]
    assert all(values[-1] == 3 for _, _, values in unresolved)
    return resolved, unresolved


def state(indexed, row, offset):
    start, complete = indexed[row]
    return temper(complete[start + offset])


def donor_patterns():
    # Under d=11, p=627 and *exactly* the two ordinary samplers:
    # row43 DEST=bench finishes at one of X[4..8]; row44 CLASS=STORES
    # accepts X[10], after a rejection at already-known X[9].
    available = set()
    counts = {}
    for dest_finish in range(4, 9):
        count = 0
        for codes in product(range(8), repeat=4):
            good = True
            for j, code in enumerate(codes):
                position = 4 + j
                if position < dest_finish and code not in (6, 7):
                    good = False
                if position == dest_finish and code not in (4, 5):
                    good = False
                if position > dest_finish and code not in (3, 4, 5, 6, 7):
                    good = False
            if good:
                available.add(codes)
                count += 1
        counts[dest_finish] = count
    assert counts == {4: 250, 5: 100, 6: 40, 7: 16, 8: 16}
    assert len(available) == 422

    # Row96 DEST=store settles at X[397]. Known X[398]/X[399]
    # reject CLASS; row97 CLASS=LABEL accepts X[404]. Hence hidden
    # X[400..403] all have high3 class codes 3..7.
    b_count = 5 ** 4
    assert b_count == 625
    return counts, len(available), b_count


def main(source):
    labels, indexed = reconstructed(source)
    resolved, unresolved = dest_observations(labels, indexed)
    for row, label, codes, prediction in resolved:
        print("DEST_RESOLVED", row, label, "top2", codes,
              "predicted", prediction)
    for row, label, codes in unresolved:
        print("DEST_PARTIAL", row, label, "top2", codes)
    print("original_source_resolved", len(resolved), "of",
          len(resolved) + len(unresolved))

    # The following observations are unaffected by selected row129,
    # which never enters the source-derived MT closure.
    assert labels[43][1] == "bench"
    assert labels[44][0] == "STORES"
    assert labels[96][1] == "store"
    assert labels[97][0] == "LABEL"
    assert state(indexed, 44, -2) >> 29 == 7
    assert state(indexed, 44, -1) >> 29 == 1
    assert state(indexed, 96, 4) >> 30 == 0
    assert state(indexed, 96, 5) >> 29 == 5
    assert state(indexed, 96, 6) >> 29 == 6
    counts, a, b = donor_patterns()
    print("conditional_target_placement", "d=11,p=627")
    print("row43_to_row44_destination_end_counts", counts)
    print("donor_A_fourword_tempered_high3_patterns", a, "of", 8 ** 4)
    print("donor_B_fourword_tempered_high3_patterns", b, "of", 8 ** 4)
    print("joint_conditional_high3_patterns", a * b, "of", 8 ** 8)
    print("direct_K04_target_bits_recovered", 0)
    print("K04_K08", "UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python agents/agent7/k04_dest_sampler_target_constraints.py "
            "original-case.zip"
        )
    main(Path(sys.argv[1]))
