"""Bounded original-source-only retry hash-chain negative control.

The selected ESC-N / PS-261003-0417 attempt 2, K04 route mask,
original commitments and all K08 material are excluded.
Run from any directory in a checkout containing original resources/.
"""
import hashlib
import re
from pathlib import Path

source = Path(__file__).resolve().parents[2] / "resources/evidence/print/spool-reconstruction.log"
raw = source.read_bytes()
assert hashlib.sha256(raw).hexdigest() == (
    "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
), "Unexpected original spool bytes"
rows = [line for line in raw.decode().splitlines() if "JOB=PS-261003-0420 " in line]
assert len(rows) == 2
assert "ATTEMPT=1 STATE=ACK CLASS=STORES" in rows[0]
assert "ATTEMPT=2 STATE=ACK CLASS=RECOVER" in rows[1]


def payload(line: str) -> bytes:
    return bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", line).group(1))


first, heldout = map(payload, rows)
job = b"PS-261003-0420"
next_class = b"RECOVER"
attempt = b"2"
inputs = [
    ("prev-only", first),
    ("prev-job", first + job),
    ("job-prev", job + first),
    ("prev-attempt-ascii", first + attempt),
    ("prev-class", first + next_class),
    ("prev-class-attempt", first + next_class + attempt),
    ("prev-job-attempt", first + job + attempt),
    ("prev-job-attempt-class", first + job + attempt + next_class),
    ("job-prev-attempt", job + first + attempt),
    ("prev-attempt-u32be", first + (2).to_bytes(4, "big")),
    ("prev-attempt-u8", first + bytes([2])),
]
models = [(name, hashlib.sha256(data).digest()[:16]) for name, data in inputs]
models.append(("blake2s-prev-16", hashlib.blake2s(first, digest_size=16).digest()))
assert len(models) == 12

for name, candidate in models:
    print(name, candidate.hex().upper(), "MATCH" if candidate == heldout else "NO_MATCH")
matches = sum(candidate == heldout for _, candidate in models)
print("Original PS-0420 exact heldout matches:", matches, "of", len(models))
assert matches == 0
