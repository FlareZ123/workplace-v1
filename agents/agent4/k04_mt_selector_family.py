"""Source-only K04 producer-selector family test; selected row129 withheld.

Run: python agents/agent4/k04_mt_selector_family.py original-case.zip
Requires existing Agent 23 / Agent 6 source-verified MT recurrence routines.
Never reads REC8 commitments, printer mask, or selected ACK payload.
"""
import re
import sys
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent6"))
from k04_mt_ternary_class_gate import close_group, temper
from k04_mt_inverse_peel import groups, rows
from k04_mt_rowstart import SPOOL

LABEL_INDEX = {"LABEL": 0, "STORES": 1, "RECOVER": 2}


def evidence(source):
    with ZipFile(source) as archive:
        lines = [line for line in archive.read(SPOOL).decode().splitlines()
                 if line.startswith("2026-")]
    assert len(lines) == 133
    words = rows(source)
    assert words[129] == []
    accepted, rejected = [], []
    for entries in groups(source, words).values():
        full, _ = close_group(entries, words)
        for row, start in entries:
            if row >= 128 or start - 1 not in full:
                continue
            klass = re.search(r"CLASS=([A-Z]+)", lines[row]).group(1)
            accepted.append((row, klass, temper(full[start - 1])))
            for distance in range(2, 20):
                if start - distance not in full:
                    break
                rejected.append((row, distance, temper(full[start - distance])))
    accepted.sort()
    rejected.sort()
    assert len(accepted) == 12
    assert len(rejected) == 7
    assert all(value >> 29 == LABEL_INDEX[klass]
               for _, klass, value in accepted)
    assert all(value >> 29 >= 3 for _, _, value in rejected)
    return accepted, rejected


def surviving_stdlib_ranges(accepted, rejected, maximum=4096):
    found = []
    for n in range(2, maximum + 1):
        k = n.bit_length()  # CPython Random._randbelow(n)
        mapping = {}
        valid = True
        for _, klass, value in accepted:
            number = value >> (32 - k)
            if number >= n or (number in mapping and mapping[number] != klass):
                valid = False
                break
            mapping[number] = klass
        if valid and all((value >> (32 - k)) >= n
                         for _, _, value in rejected):
            found.append((n, mapping))
    return found


def main(source):
    accepted, rejected = evidence(source)
    family = surviving_stdlib_ranges(accepted, rejected)
    indices2 = {}
    for _, klass, output in accepted:
        indices2.setdefault(output >> 30, set()).add(klass)
    # Two observed distinct CLASS labels map to the same two-bit outcome.
    assert any(len(labels) > 1 for labels in indices2.values())
    assert [n for n, _ in family if n <= 64] == [4, 8, 16, 32, 64]
    assert len(family) == 21
    print("selected_row_129_withheld", True)
    print("original_source_sample", len(accepted), "accepted", len(rejected), "rejected")
    print("CPython_choice_of_exactly_three_labels", "INCOMPATIBLE")
    print("stdlib_randbelow_survivors_2_through_4096", [n for n, _ in family])
    print("smallest_stdlib_sampler", family[0])
    print("custom_getrandbits_3_reject_at_3", "CONSISTENT")
    print("historical_producer_identity", "UNPROVEN")
    print("K04_K08", "MISSING")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_mt_selector_family.py original-case.zip")
    main(Path(sys.argv[1]))
