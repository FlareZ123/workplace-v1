"""Source-only PTW serial-pair to printer MT19937 exact-recurrence check.

Run from this repository using Python 3. Original K04 ACK attempt 2,
mask and acceptance commitments are never read as target inputs.
"""
import hashlib
import json
import random
import re
from collections import defaultdict
from pathlib import Path

E = Path(__file__).resolve().parents[2] / "resources" / "evidence"
P = E / "print" / "spool-reconstruction.log"
S = E / "maintenance" / "seal-receipts.jsonl"
assert hashlib.sha256(P.read_bytes()).hexdigest() == "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
assert hashlib.sha256(S.read_bytes()).hexdigest() == "c00944558636fbcc7e91b81e8e838ffd13fcd5a30d121b41951888766a8a0e32"


def untemper(y):
    x = y
    for _ in range(5):
        x = y ^ (x >> 18)
    y = x
    for _ in range(5):
        x = y ^ ((x << 15) & 0xEFC60000)
    y = x
    for _ in range(5):
        x = y ^ ((x << 7) & 0x9D2C5680)
    y = x
    for _ in range(5):
        x = y ^ (x >> 11)
    return x & 0xFFFFFFFF


def twist(a, b):
    x = ((a & 0x80000000) | (b & 0x7FFFFFFF)) >> 1
    return x ^ (0x9908B0DF if b & 1 else 0)


r = random.Random(1729)
control = [untemper(r.getrandbits(32)) for _ in range(625)]
assert control[624] == control[397] ^ twist(control[0], control[1])
print("synthetic_MT_recurrence_control=PASS")

lines = [s for s in P.read_text().splitlines() if "JOB=" in s]
assert len(lines) == 133
words = []
for row, line in enumerate(lines):
    if row == 129:
        continue  # Withhold the disputed selected original.
    value = bytes.fromhex(re.search(r"PAYLOAD=([A-F0-9]{32})", line).group(1))
    words.extend((row, j, untemper(int.from_bytes(value[4*j:4*j+4], "little"))) for j in range(4))
assert len(words) == 528

printer_xor_pairs = defaultdict(list)
for i, (ra, wa, va) in enumerate(words):
    for rb, wb, vb in words[i+1:]:
        if ra < rb:
            printer_xor_pairs[va ^ vb].append(((ra, wa), (rb, wb)))
assert sum(len(x) for x in printer_xor_pairs.values()) == 138336

serials = {
    int(o["permit"][4:]): bytes.fromhex(o["serial"][3:])
    for line in S.read_text().splitlines()
    if (o := json.loads(line))["permit"] != "PTW-417"
}
assert set(serials) == set(range(390, 417))
found = []
for endian in ("little", "big"):
    for n in range(390, 416):
        a = untemper(int.from_bytes(serials[n], endian))
        b = untemper(int.from_bytes(serials[n+1], endian))
        for hit in printer_xor_pairs.get(twist(a, b), ()):
            found.append((endian, n, n+1, hit))

print("source_permit_pairs=26; endian_forms=2")
print("source_printer_words=528; source_xor_pairs=138336")
print("source_exact_32bit_twist_matches=", len(found))
for item in found:
    print(item)
assert not found, "new potential source bridge: investigate provenance before target inference"
