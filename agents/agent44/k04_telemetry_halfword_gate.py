"""Source-only MT19937 telemetry halfword bridge probe.

Run: python agents/agent44/k04_telemetry_halfword_gate.py original-export.zip
Withholds disputed printer row129, route mask and all acceptance commitments.
"""
import collections
import hashlib
import itertools
import json
import random
import re
import sys
import zipfile

EXPECTED_SPOOL = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
EXPECTED_TELEMETRY = "3787dbd6bab3930ea5293c25a995175161a1c0d7683daad29f498026e057639f"
MASK = (1 << 32) - 1


def untemper(y):
    for shift, mask in ((18, None), (15, 0xEFC60000), (7, 0x9D2C5680), (11, None)):
        raw = y
        for _ in range(6):
            y = raw ^ ((y >> shift) if mask is None else ((y << shift) & mask))
    return y & MASK


def temper(y):
    y ^= y >> 11
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 15) & 0xEFC60000
    return (y ^ (y >> 18)) & MASK


def ancestor_low31(middle, end):
    mixed = middle ^ end
    untwisted = mixed ^ (0x9908B0DF if mixed >> 31 else 0)
    return ((untwisted << 1) | (mixed >> 31)) & 0x7FFFFFFF


def ordered_triples(records):
    groups = []
    for revision in (1, 2, 3, 4):
        groups.append((f"revision{revision}", sorted(
            (r for r in records if r["revision"] == revision), key=lambda r: r["seq"])))
    for seq in range(8):
        groups.append((f"seq{seq}", sorted(
            (r for r in records if r["seq"] == seq), key=lambda r: r["revision"])))
    groups.extend([
        ("retrieval", records),
        ("acquisition", sorted(records, key=lambda r: (r["ts"], r["seq"], r["revision"]))),
        ("seqrev", sorted(records, key=lambda r: (r["seq"], r["revision"]))),
        ("revseq", sorted(records, key=lambda r: (r["revision"], r["seq"]))),
    ])
    signatures = collections.defaultdict(list)
    for name, values in groups:
        for start in range(len(values) - 2):
            signature = tuple(x["value"] for x in values[start:start + 3])
            signatures[signature].append((name, start))
    return signatures, len(groups)


def main(zip_path):
    rng = random.Random(3124)
    for _ in range(200):
        word = rng.getrandbits(32)
        assert temper(untemper(word)) == word
    with zipfile.ZipFile(zip_path) as archive:
        spool = archive.read("evidence/print/spool-reconstruction.log")
        telemetry = archive.read("evidence/telemetry/freeze-export.jsonl")
    assert hashlib.sha256(spool).hexdigest() == EXPECTED_SPOOL
    assert hashlib.sha256(telemetry).hexdigest() == EXPECTED_TELEMETRY
    records = [json.loads(line) for line in telemetry.splitlines()]
    records = [r for r in records if r["tag"] == "LT-204" and
               r["field"] == "DIAG_WORD" and r["revision"] <= 4]
    assert len(records) == 32
    signatures, group_count = ordered_triples(records)

    rows = []
    for line in spool.splitlines()[1:]:
        payload = bytes.fromhex(re.search(rb"PAYLOAD=([0-9A-F]{32})", line).group(1).decode())
        rows.append([untemper(int.from_bytes(payload[k:k + 4], "little"))
                     for k in (0, 4, 8, 12)])
    assert len(rows) == 133
    rows[129] = None

    matches = []
    checks = 0
    for a, first in enumerate(rows):
        if first is None:
            continue
        for b in range(a + 1, len(rows)):
            last = rows[b]
            if last is None:
                continue
            for i in (0, 1):
                for j in (0, 1):
                    lows = [ancestor_low31(first[i + k], last[j + k]) for k in range(3)]
                    options = [(temper(x) >> 16, temper(x | 0x80000000) >> 16)
                               for x in lows]
                    checks += 1
                    for test in itertools.product(*options):
                        if test in signatures:
                            matches.append((a, b, i, j, test, signatures[test]))
    print(json.dumps({
        "source_records": len(records),
        "source_orderings": group_count,
        "distinct_source_triples": len(signatures),
        "printer_pair_offset_windows": checks,
        "matching_3word_fingerprints": matches,
    }, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
