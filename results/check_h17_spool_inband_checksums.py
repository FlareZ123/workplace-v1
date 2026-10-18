"""Bounded in-band checksum test for the original H-17 spool payloads.

Read-only case-evidence analysis. The 16-byte PAYLOAD has no independently
authenticated checksum; this tests one possible *internal* integrity structure.
"""
from collections import Counter, defaultdict
from pathlib import Path
import re
import zlib

root = Path(__file__).resolve().parents[1]
source = root / "resources/evidence/print/spool-reconstruction.log"
rows = []
for line in source.read_text(encoding="utf-8").splitlines():
    match = re.search(r"\bCLASS=(\w+).*\bPAYLOAD=([0-9A-F]{32})\b", line)
    if match:
        rows.append((
            match.group(1),
            line.split()[0].endswith("Z"),
            bytes.fromhex(match.group(2)),
        ))
assert len(rows) == 133
assert sum(cls == "RECOVER" for cls, _, _ in rows) == 40

checksums = {
    "crc32": zlib.crc32,
    "adler32": zlib.adler32,
}


def variants(payload):
    for location in ("prefix", "suffix"):
        data, stored = (payload[4:], payload[:4]) if location == "prefix" else (
            payload[:-4], payload[-4:]
        )
        for name, checksum in checksums.items():
            calculated = checksum(data)
            for endian in ("big", "little"):
                yield (name, location, endian), int.from_bytes(stored, endian) ^ calculated


# Synthetic controls validate exact CRC32 and a uniform fixed-XOR checksum.
for example in (b"Hello world!", b"1234567890ab"):
    plain = example + zlib.crc32(example).to_bytes(4, "big")
    masked = example + (zlib.crc32(example) ^ 0xA5A5A5A5).to_bytes(4, "big")
    assert dict(variants(plain))[("crc32", "suffix", "big")] == 0
    assert dict(variants(masked))[("crc32", "suffix", "big")] == 0xA5A5A5A5

cohorts = {
    "ALL": [payload for _, _, payload in rows],
    "REGULAR": [payload for _, tail, payload in rows if not tail],
    "Z-TAIL": [payload for _, tail, payload in rows if tail],
    "RECOVER": [payload for cls, _, payload in rows if cls == "RECOVER"],
    "RECOVER-Z-TAIL": [
        payload for cls, tail, payload in rows if cls == "RECOVER" and tail
    ],
}
assert {name: len(values) for name, values in cohorts.items()} == {
    "ALL": 133, "REGULAR": 128, "Z-TAIL": 5,
    "RECOVER": 40, "RECOVER-Z-TAIL": 5,
}

for name, payloads in cohorts.items():
    offsets = defaultdict(list)
    for payload in payloads:
        for variant, offset in variants(payload):
            offsets[variant].append(offset)
    for variant, values in sorted(offsets.items()):
        counts = Counter(values)
        print(name, len(payloads), variant,
              "plain_matches", counts[0],
              "largest_shared_xor_offset", max(counts.values()))
