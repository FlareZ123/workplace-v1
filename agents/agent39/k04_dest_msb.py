"""Decode one new K04 hidden MT word from the post-payload DEST field.

Run: python agents/agent39/k04_dest_msb.py original-case.zip
Target row129 is excluded inside the original-source row decoder; this code
never opens any archive acceptance commitment, route mask or K08 material.
"""
import re
import sys
from pathlib import Path
from zipfile import ZipFile

agents = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(agents / "agent31"))
from k04_mt_recursive_peel import rows, groups, close_group, temper

SPOOL = "evidence/print/spool-reconstruction.log"
DEST = {"store": 0, "desk": 1, "bench": 2}
LOW31 = 0x7FFFFFFF
HIGH = 0x80000000


def main(source):
    with ZipFile(source) as z:
        lines = [line for line in z.read(SPOOL).decode().splitlines()
                 if line.startswith("2026-")]
    assert len(lines) == 133
    labels = [DEST[re.search(r"DEST=([a-z]+)", line).group(1)]
              for line in lines]

    values = rows(source)
    assert not values[129]
    group_list = list(groups(source, values).values())
    candidates = []
    for entries in group_list:
        state, _ = close_group(entries, values)
        for row, start in entries:
            if row >= 128:
                continue
            mask, bits = state.get(start + 4, (0, 0))
            if mask != LOW31:
                continue
            indices = (temper(bits) >> 30,
                       temper(bits | HIGH) >> 30)
            matching = [bit for bit, index in enumerate(indices)
                        if index == labels[row]]
            candidates.append((row, bits, indices, matching))
    assert [(r, f"{bits:08X}", indices, matching)
            for r, bits, indices, matching in candidates] == [
                (21, "5BC5D6E4", (2, 0), [0]),
                (39, "1EC545CA", (1, 3), [0]),
            ]

    # Row39 remains ambiguous: the second branch is a rejected DEST=3
    # that can be followed by another sampled output. Row21 is different:
    # both branches accept (0 or 2). Its retained DEST=bench forces MSB=0
    # under the candidate standard two-bit rejection sampler model.
    row, lower31, (a, b), accepted = candidates[0]
    assert row == 21 and a < 3 and b < 3 and accepted == [0]
    inferred = lower31
    assert temper(inferred) == 0x9ACC8EED

    print("row129_withheld", True)
    print("partial_output_row21_plus4", f"{lower31:08X}",
          "known_bits", 31)
    print("possible_two_bit_samples", a, b)
    print("original_row21_destination_index", labels[21])
    print("conditional_new_complete_untempered_output", f"{inferred:08X}")
    print("conditional_new_tempered_output", f"{temper(inferred):08X}")
    print("row39_alternative_rejection_unresolved", True)
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python agents/agent39/k04_dest_msb.py original-case.zip")
    main(Path(sys.argv[1]))
