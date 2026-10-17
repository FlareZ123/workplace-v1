"""Read-only Hamming geometry of the three same-job H-17 RECOVER attempts."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPOOL = ROOT / "resources/evidence/print/spool-reconstruction.log"
JOB = "PS-261003-0417"


def main() -> None:
    rows = []
    for line in SPOOL.read_text(encoding="utf-8").splitlines():
        fields = dict(re.findall(r"(\w+)=([^ ]+)", line))
        if fields.get("JOB") == JOB and fields.get("CLASS") == "RECOVER":
            rows.append(fields)
    rows.sort(key=lambda rec: int(rec["ATTEMPT"]))
    assert [r["ATTEMPT"] for r in rows] == ["1", "2", "3"]
    bits = [int(rec["PAYLOAD"], 16) for rec in rows]
    pairs = [(bits[0] ^ bits[1]).bit_count(),
             (bits[0] ^ bits[2]).bit_count(),
             (bits[1] ^ bits[2]).bit_count()]
    majority = (bits[0] & bits[1]) | (bits[0] & bits[2]) | (bits[1] & bits[2])
    edits = [(b ^ majority).bit_count() for b in bits]
    assert sum(pairs) == 2 * sum(edits)
    assert max(edits) == max(pairs) // 2
    for row in rows:
        print("attempt", row["ATTEMPT"], row["STATE"], row["PAYLOAD"])
    print("pair distances (1,2), (1,3), (2,3):", pairs)
    print("minimum total edits to one common 128-bit ancestor:", sum(edits))
    print("one common center distances:", edits)
    print("minimum covering radius:", max(edits))


if __name__ == "__main__":
    main()
