"""K04 MT metadata: resolve two independently reconstructed 31-bit hidden words.

Run: python agents/agent30/k04_metadata_highbits.py original-case.zip

No selected spool row129, K04 coupon mask or REC8 commitments are loaded.
The full-MT predecessor/selector interpretation is conditional.
"""
import re
import sys
from pathlib import Path
from zipfile import ZipFile

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "agent31"))
from k04_mt_recursive_peel import rows, groups, close_group, temper

ALL = 0xFFFFFFFF
LOW31 = 0x7FFFFFFF
SPOOL = "evidence/print/spool-reconstruction.log"
LABELS = {"LABEL": 0, "STORES": 1, "RECOVER": 2}
DESTS = {"store": 0, "desk": 1, "bench": 2}


def main(source):
    values = rows(source)
    assert not values[129]
    with ZipFile(source) as archive:
        lines = [line for line in archive.read(SPOOL).decode().splitlines()
                 if line.startswith("2026-")]
    assert len(lines) == 133

    findings = []
    for entries in groups(source, values).values():
        state, _ = close_group(entries, values)
        for row, start in entries:
            if row >= 128:
                continue
            fields = (
                ("CLASS", start - 1, 29, LABELS[
                    re.search(r"CLASS=([A-Z]+)", lines[row]).group(1)]),
                ("DEST", start + 4, 30, DESTS[
                    re.search(r"DEST=([a-z]+)", lines[row]).group(1)]),
            )
            for kind, index, shift, expected in fields:
                mask, value = state.get(index, (0, 0))
                if mask != LOW31:
                    continue
                alternatives = [value, value | 0x80000000]
                matches = [x for x in alternatives
                           if (temper(x) >> shift) == expected]
                assert len(matches) == 1, (row, kind, alternatives)
                findings.append((row, kind, index - start,
                                 f"{matches[0]:08X}",
                                 tuple(temper(x) >> shift for x in alternatives),
                                 expected))
    assert findings == [
        (21, "DEST", 4, "5BC5D6E4", (2, 0), 2),
        (39, "DEST", 4, "1EC545CA", (1, 3), 1),
    ], findings

    print("source_only_31bit_metadata_highbit_recoveries", findings)
    print("selected_row129_withheld", True)
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_metadata_highbits.py original-case.zip")
    main(Path(sys.argv[1]))
