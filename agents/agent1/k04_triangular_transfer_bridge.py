"""K04: independently ordered middle-donor -> printer -> transfer prediction.

Run: python agents/agent1/k04_triangular_transfer_bridge.py ORIGINAL_EXPORT.zip
Selected printer row129, K04 mask and all acceptance commitments are withheld.
"""
import collections
import hashlib
import json
import random
import re
import struct
import sys
import zipfile
import zlib

PINS = {
    "evidence/recorder/trip-recorder.raw": "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba",
    "evidence/procedures/RC-17-scans.txt": "a4b649fdbb6909115fb9505133012b5c1dda42141aafc1c6ec756199ddf1fc6d",
    "evidence/print/spool-reconstruction.log": "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083",
    "evidence/transfers/transfer-audit.jsonl": "32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf",
}


def untemper(value):
    for shift, mask in ((18, None), (15, 0xEFC60000), (7, 0x9D2C5680), (11, None)):
        original = value
        for _ in range(6):
            value = original ^ (value >> shift if mask is None else (value << shift) & mask)
    return value & 0xFFFFFFFF


def temper(value):
    value ^= value >> 11
    value ^= (value << 7) & 0x9D2C5680
    value ^= (value << 15) & 0xEFC60000
    return (value ^ (value >> 18)) & 0xFFFFFFFF


def twist(a, b):
    mixed = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return (mixed >> 1) ^ (0x9908B0DF if mixed & 1 else 0)


def source_runs(archive):
    raw = archive.read("evidence/recorder/trip-recorder.raw")
    records = []
    assert struct.unpack_from("<I", raw, 12)[0] == 88
    assert len(raw) == 16 + 88 * 24
    for i in range(88):
        record = raw[16 + 24 * i:16 + 24 * (i + 1)]
        if zlib.crc32(record[:20]) != struct.unpack_from("<I", record, 20)[0]:
            continue
        ts, node, event, latch, seq = struct.unpack_from("<IHBBI", record)
        records.append((i, ts, node, event, latch, seq,
                        untemper(struct.unpack_from("<I", record, 12)[0])))
    assert len(records) == 84
    sequences = [sorted(records), sorted(records, key=lambda r: (r[1], r[0]))]
    for key_fields in ((2, 3), (2, 3, 4)):
        grouped = collections.defaultdict(list)
        for record in records:
            grouped[tuple(record[k] for k in key_fields)].append(record)
        sequences.extend(sorted(group, key=lambda r: (r[5], r[0]))
                         for group in grouped.values())
    candidate_runs = set()
    for seq in sequences:
        for i in range(len(seq) - 2):
            candidate_runs.add(tuple(item[6] for item in seq[i:i + 3]))
    rc = archive.read("evidence/procedures/RC-17-scans.txt").decode()
    for revision in ("B", "C", "D-draft"):
        pages = []
        for block in rc.split("\f"):
            if "REV " + revision + " /" not in block:
                continue
            strip = re.search(r"Footer control strip: ([0-9A-F]{8})", block)
            heading = re.search(r"SECTION ([A-Z]+)", block)
            if strip and heading:
                raw_word = int.from_bytes(bytes.fromhex(strip[1]), "little")
                pages.append((heading[1], untemper(raw_word)))
        assert len(pages) == 4
        for seq in (pages, sorted(pages, key=lambda item:
                       ("DRAIN", "ISOLATE", "PURGE", "VERIFY").index(item[0]))):
            for i in range(2):
                candidate_runs.add(tuple(item[1] for item in seq[i:i + 3]))
    return candidate_runs


def test(path):
    with zipfile.ZipFile(path) as archive:
        for name, expected in PINS.items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == expected, name
        donors = source_runs(archive)
        spool = archive.read("evidence/print/spool-reconstruction.log").decode()
        audit = archive.read("evidence/transfers/transfer-audit.jsonl").decode()
    rows = []
    for line in spool.splitlines():
        matched = re.search(r"PAYLOAD=([0-9A-F]{32})", line)
        if matched:
            words = struct.unpack("<4I", bytes.fromhex(matched[1]))
            rows.append(tuple(untemper(word) for word in words))
    assert len(rows) == 133
    transfer = collections.defaultdict(list)
    for line in audit.splitlines():
        obj = json.loads(line)
        if obj["kind"] == "CHUNK":
            transfer[obj["transfer"]].append(obj)
    transfer_windows = set()
    for rows_of_transfer in transfer.values():
        rows_of_transfer.sort(key=lambda obj: (obj["seq"], obj["attempt"]))
        assert len(rows_of_transfer) == 16
        for j in range(14):
            transfer_windows.add(tuple(
                int.from_bytes(bytes.fromhex(item["checkpoint"]), "little")
                for item in rows_of_transfer[j:j + 3]))
    matches = []
    partial = []
    checks = 0
    for row_id, row in enumerate(rows):
        if row_id == 129:
            continue
        steps = tuple(twist(row[j], row[j + 1]) for j in range(3))
        for donor in donors:
            prediction = tuple(temper(donor[j] ^ steps[j]) >> 16 for j in range(3))
            checks += 1
            for observed in transfer_windows:
                if prediction == observed:
                    matches.append((row_id, donor, observed))
                elif prediction[:2] == observed[:2]:
                    partial.append((row_id, donor, observed))
    assert not matches and not partial
    rng = random.Random(0xAA8412)
    generated = [untemper(rng.getrandbits(32)) for _ in range(1000)]
    for k in (0, 10, 200):
        future = tuple(temper(generated[k + 397 + j] ^
                           twist(generated[k + j], generated[k + j + 1])) >> 16
                       for j in range(3))
        assert future == tuple(temper(generated[k + 624 + j]) >> 16
                               for j in range(3))
    print("source_threeword_middle_donor_windows", len(donors))
    print("source_transfer_high16_windows", len(transfer_windows))
    print("intact_printer_source_first_word_windows", len(rows) - 1)
    print("candidate_triplet_predictions", checks)
    print("three_high16_matches", len(matches))
    print("first_two_high16_matches", len(partial))
    print("synthetic_three_word_positive_controls", 3)
    print("selected_row129_withheld", True)


if __name__ == "__main__":
    test(sys.argv[1])
