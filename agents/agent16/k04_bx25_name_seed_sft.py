"""BX25 named-insured CPython text-seed gate. Read-only source-pinned SFT.

Source: original decrypted BX25-08.pdf page, 2025 Risk annual declaration,
named insured Noyes Energy Group; see communications/broadcast/
20261020T0229Z_agent45_BX25-released-original-page.md.

No original record claims the name was a PRNG seed. This tests only that explicit
conditional text-seed family, with selected K04 bytes and original hashes withheld.
"""
from __future__ import annotations

import hashlib
import random
import re
import sys
import zipfile
from pathlib import Path

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
SOURCE_NAME = "Noyes Energy Group"
SOURCE_COMPOSITE = "Noyes Energy Group H-17 Atlantic facility"
OBSERVED_ROWS = (0, 3, 34, 64)
DRAWS = 8192


def spool_bytes(source: Path) -> bytes:
    if source.is_dir():
        return (source / "evidence/print/spool-reconstruction.log").read_bytes()
    with zipfile.ZipFile(source) as archive:
        return archive.read("evidence/print/spool-reconstruction.log")


def block_hits(stream: bytes, pattern: bytes) -> int:
    return sum(stream[i : i + len(pattern)] == pattern for i in range(len(stream) - len(pattern) + 1))


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("resources")
    body = spool_bytes(source)
    assert hashlib.sha256(body).hexdigest() == SPOOL_SHA, "original spool SHA mismatch"
    rows = [bytes.fromhex(x.decode()) for x in re.findall(rb"PAYLOAD=([0-9A-F]{32})", body)]
    assert len(rows) == 133, len(rows)
    assert rows[3].hex().upper() == "24FF4383374867B2F2FABB2B30F72AAF"

    # Small fixed source-led list; no speculative variant expansion.
    for seed in (SOURCE_NAME, SOURCE_COMPOSITE):
        engine = random.Random(seed)
        words = [engine.getrandbits(32) for _ in range(DRAWS + 4)]
        for orientation in ("little", "big"):
            full = b"".join(w.to_bytes(4, orientation) for w in words)
            positive = full[4:20]
            assert block_hits(full, positive) >= 1
            observed = {index: block_hits(full, rows[index]) for index in OBSERVED_ROWS}
            print(f"seed={seed!r} orientation={orientation} observed_hit_counts={observed} synthetic_control=PASS")
            assert all(count == 0 for count in observed.values()), "new source-word match requires followup"
    print("ORIGINAL BOUNDED OUTCOME: no match to four intact 16-byte printer rows in first 8192 draws")
    print("K04 selected bytes withheld, original commitment unused; historical seed premise unsupported")


if __name__ == "__main__":
    main()
