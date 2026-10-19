"""Source-only K04 conditional post-payload DEST high-bit completion (row39).

Run: python agents/agent49/k04_dest_partial_row39.py original-case.zip
Uses the original, SHA-pinned printer extraction and existing 42-witness
closure; selected row129 and original commitments remain unread.
"""
import re
import sys
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent31"))
from k04_mt_recursive_peel import close_group, groups, rows, temper

DEST = {"store": 0, "desk": 1, "bench": 2}
ALL = 0xFFFFFFFF


def main(path):
    values = rows(path)
    assert len(values) == 133 and values[129] == []
    with ZipFile(path) as z:
        lines = [
            line for line in z.read("evidence/print/spool-reconstruction.log")
            .decode("ascii").splitlines() if line.startswith("2026-")
        ]
    assert len(lines) == 133
    clusters = groups(path, values)

    fully_decoded = []
    partial = []
    for entries in clusters.values():
        state, _ = close_group(entries, values)
        for row, start in entries:
            if row >= 128:
                continue
            destination = re.search(r"DEST=([a-z]+)", lines[row]).group(1)
            mask, bits = state.get(start + 4, (0, 0))
            if mask == ALL:
                value = temper(bits) >> 30
                fully_decoded.append((row, destination, value))
            elif mask == 0x7FFFFFFF:
                possible = [
                    (high, temper(bits | (high << 31)) >> 30)
                    for high in (0, 1)
                ]
                partial.append((row, destination, start + 4, bits, possible))

    accepted = [(r, label, idx) for r, label, idx in fully_decoded if idx < 3]
    assert len(fully_decoded) == 17 and len(accepted) == 13
    assert all(DEST[label] == index for _, label, index in accepted)

    matches = [item for item in partial if item[0] == 39]
    assert len(matches) == 1
    row, label, position, lowbits, possibilities = matches[0]
    assert label == "desk" and lowbits == 0x1EC545CA
    assert possibilities == [(0, 1), (1, 3)]
    high = next(high for high, index in possibilities if index == DEST[label])
    untempered = lowbits | (high << 31)
    predicted = temper(untempered)
    assert predicted == 0x594A9B30

    print("source_row", row, "destination", label)
    print("relative_postpayload_index", position)
    print("known_untempered_bits", "31/32")
    print("competing_two_bit_indices", possibilities)
    print("model_conditioned_state_word", f"{untempered:08X}")
    print("model_conditioned_output_word", f"{predicted:08X}")
    print("independent_complete_DEST_controls", f"{len(accepted)}/{len(accepted)}")
    print("source_selected_K04_row_withheld", True)
    print("acceptance_unchecked_K04_K08_missing", True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: k04_dest_partial_row39.py original-case.zip")
    main(Path(sys.argv[1]))
