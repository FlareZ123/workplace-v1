"""Original PTW-417 / PS-0417 cross-record source-only bridge test.

Agent48, 1 Nov 2026. Read-only, source-pinned; excludes disputed row129
PAYLOAD from all analyses and does not use the K04 mask, REC8 digests, or
K08 nonce. See agents/agent48/memory.md for frozen pretest predictions.

Run: python ptw417_printer_bridge_sft.py original-43-member-case.zip
"""
import hashlib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

ZIP_HASH = "a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec"
SPOOL_HASH = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MASK = 0xFFFFFFFF


def _undo_right(value, shift):
    out = value
    for _ in range(32 // shift + 2):
        out = value ^ (out >> shift)
    return out & MASK


def _undo_left(value, shift, mask):
    out = value
    for _ in range(32 // shift + 2):
        out = value ^ ((out << shift) & mask)
    return out & MASK


def untemper(value):
    value = _undo_right(value, 18)
    value = _undo_left(value, 15, 0xEFC60000)
    value = _undo_left(value, 7, 0x9D2C5680)
    return _undo_right(value, 11)


def temper(value):
    value ^= value >> 11
    value ^= (value << 7) & 0x9D2C5680
    value ^= (value << 15) & 0xEFC60000
    value ^= value >> 18
    return value & MASK


def low31_successor(middle, end):
    """Invert one MT19937 recurrence to recover ancestral successor low31."""
    mixed = untemper(middle) ^ untemper(end)
    low = mixed >> 31
    return ((((mixed ^ (0x9908B0DF if low else 0)) << 1) | low) & MASK) & 0x7FFFFFFF


def controls():
    for seed in (0, 417, 20261101):
        r = random.Random(seed)
        words = [r.getrandbits(32) for _ in range(627)]
        for i in range(3):
            assert low31_successor(words[397 + i], words[624 + i]) == (untemper(words[i + 1]) & 0x7FFFFFFF)
        for _ in range(20):
            x = r.getrandbits(32)
            assert temper(untemper(x)) == x
    return 3


def load(path):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == ZIP_HASH
    with ZipFile(path) as z:
        spool = z.read("evidence/print/spool-reconstruction.log")
        assert hashlib.sha256(spool).hexdigest() == SPOOL_HASH
        receipts = [json.loads(line) for line in z.read("evidence/maintenance/seal-receipts.jsonl").decode().splitlines() if line]
    lines = [x for x in spool.decode("ascii").splitlines() if x.startswith("2026-")]
    assert len(lines) == 133
    assert "JOB=PS-261003-0417 " in lines[129] and "ATTEMPT=2 " in lines[129]
    rows = []
    for i, line in enumerate(lines):
        if i == 129:  # skip selected coupon BEFORE parsing any payload
            rows.append(None)
            continue
        payload = bytes.fromhex(re.search(r"PAYLOAD=([A-F0-9]{32})", line).group(1))
        rows.append(tuple(int.from_bytes(payload[j:j + 4], "little") for j in range(0, 16, 4)))
    return lines, receipts, rows


def signed_serials(receipts):
    by_bay = {}
    for r in receipts:
        if r["permit"] != "PTW-417" or r["state"] != "CLOSED" or r["fitment"] != "AS_LEFT" or not r["signed"]:
            continue
        b = r["bay"]
        if b not in by_bay or by_bay[b]["revision"] < r["revision"]:
            by_bay[b] = r
    values = [bytes.fromhex(by_bay[b]["serial"][3:]) for b in "BDAC"]
    assert [s.hex().upper() for s in values] == ["D7DAD6BC", "9714519B", "7DAD0AD4", "BE8E87FD"]
    return values


def recurrence_pilot(rows, receipts):
    values = signed_serials(receipts)
    triples = [
        tuple(untemper(w) & 0x7FFFFFFF for w in words[start:start + 3])
        for words in ([int.from_bytes(v, "big") for v in values],
                      [int.from_bytes(v, "little") for v in values])
        for start in (0, 1)
    ]
    count = one = two = three = 0
    for i, row_a in enumerate(rows):
        if row_a is None:
            continue
        for j, row_b in enumerate(rows):
            if row_b is None or i == j:
                continue
            for sa in (0, 1):
                for sb in (0, 1):
                    witness = tuple(low31_successor(row_a[sa + k], row_b[sb + k]) for k in range(3))
                    count += 1
                    for target in triples:
                        matches = sum(x == y for x, y in zip(witness, target))
                        one += matches == 1
                        two += matches == 2
                        three += matches == 3
    assert (count, one, two, three) == (69168, 0, 0, 0)
    return {"ordered_intact_rowpair_windows": count, "three_word_serial_orientations": len(triples),
            "one_match": one, "two_matches": two, "three_matches": three}


def matched_job_pilot(lines, receipts):
    permits = {}
    for r in receipts:
        m = re.fullmatch(r"PTW-(\d+)", r["permit"])
        if m and 390 <= int(m.group(1)) <= 416:
            n = int(m.group(1))
            assert n not in permits
            permits[n] = bytes.fromhex(r["serial"][3:])
    assert len(permits) == 27

    jobs = {}
    for pos, line in enumerate(lines):
        if pos == 129:
            continue
        m = re.search(r"\bJOB=PS-261003-(\d+)\b", line)
        if m and 390 <= int(m.group(1)) <= 416:
            n = int(m.group(1))
            assert n not in jobs
            jobs[n] = line
    assert len(jobs) == 27
    categories = Counter()
    copied = 0
    for n in range(390, 417):
        line = jobs[n]
        assert "ATTEMPT=1 " in line and "STATE=ACK " in line
        categories[re.search(r"CLASS=(LABEL|STORES|RECOVER)", line).group(1)] += 1
        payload = bytes.fromhex(re.search(r"PAYLOAD=([A-F0-9]{32})", line).group(1))
        copied += permits[n] in payload
    assert categories == Counter({"LABEL": 13, "STORES": 3, "RECOVER": 11})
    assert copied == 0
    return {"intact_identifier_pairs": 27, "printer_class_counts": dict(categories),
            "contiguous_four_byte_serial_copies": copied}


def main(path):
    lines, receipts, rows = load(path)
    return {"synthetic_seed_controls": controls(),
            "ptw417_signed_bdac_serials": [v.hex().upper() for v in signed_serials(receipts)],
            "mt31_ancestral_bridge": recurrence_pilot(rows, receipts),
            "matched_job_copies": matched_job_pilot(lines, receipts),
            "new_authenticated_K04_bits": 0,
            "K08_final_words": 0,
            "status": "no_scope_specific_original_bridge"}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python ptw417_printer_bridge_sft.py original-case.zip")
    print(json.dumps(main(Path(sys.argv[1])), indent=2))
