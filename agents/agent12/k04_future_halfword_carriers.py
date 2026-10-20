"""Source-ordered two-u16 candidate future MT donor falsifier; no missing-target reads."""
import json
import pathlib
import collections
import struct

base = pathlib.Path(__file__).resolve().parents[2] / "resources" / "evidence"

def urshift(y, shift):
    v = y
    for _ in range(5):
        v = y ^ (v >> shift)
    return v & 0xffffffff

def ulshift(y, shift, mask):
    v = y
    for _ in range(5):
        v = y ^ ((v << shift) & mask)
    return v & 0xffffffff

def untemper(y):
    return urshift(ulshift(ulshift(urshift(y, 18), 15, 0xefc60000),
                            7, 0x9d2c5680), 11)

records = []
transfers = collections.defaultdict(dict)
for line in (base / "transfers/transfer-audit.jsonl").read_text().splitlines():
    x = json.loads(line)
    if x["kind"] != "CHUNK":
        continue
    group = transfers[x["transfer"]]
    if x["seq"] not in group or x["attempt"] > group[x["seq"]]["attempt"]:
        group[x["seq"]] = x
for transfer, group in transfers.items():
    for i in range(0, 8, 2):
        if i in group and i + 1 in group:
            records.append((f"{transfer} seq{i},{i+1}",
                            bytes.fromhex(group[i]["checkpoint"] + group[i+1]["checkpoint"])))

telemetry = collections.defaultdict(dict)
for line in (base / "telemetry/freeze-export.jsonl").read_text().splitlines():
    x = json.loads(line)
    if x.get("field") != "DIAG_WORD" or x.get("quality") != "GOOD" or x.get("state") != "HOLD":
        continue
    group = telemetry[x["tag"]]
    if x["seq"] not in group or x["revision"] > group[x["seq"]]["revision"]:
        group[x["seq"]] = x
for tag, group in telemetry.items():
    for i in range(0, 8, 2):
        if i in group and i + 1 in group:
            records.append((f"telemetry {tag} seq{i},{i+1}",
                            struct.pack(">HH", group[i]["value"], group[i+1]["value"])))

candidates = []
for name, bs in records:
    views = [("as-is", bs), ("halfword-reverse", bs[1::-1] + bs[3:1:-1]),
             ("word-reverse", bs[::-1]), ("swap-halves", bs[2:] + bs[:2])]
    for orientation, word in views:
        candidates.append((name, orientation, untemper(int.from_bytes(word, "little"))))

relations = [("1412^1866", 0xffffffff, 0xbd2761f8),
             ("1185^1412", 0xbfffffff, 0x359ec0c7),
             ("1411^1865", 0x9fffffff, 0x0cde27b9)]

assert len(records) == 20 and len(candidates) == 80
assert untemper(0x00000000) == 0
print("original ordered u16 pairs:", len(records), "oriented MT views:", len(candidates))
for label, mask, target in relations:
    hits = []
    minimum = 33
    for i, a in enumerate(candidates):
        for j, b in enumerate(candidates):
            if i == j:
                continue
            discrepancy = (a[2] ^ b[2] ^ target) & mask
            minimum = min(minimum, discrepancy.bit_count())
            if discrepancy == 0:
                hits.append((a[:2], b[:2]))
    print(label, "hits:", len(hits), "minimum mismatching bits:", minimum)
    assert not hits
