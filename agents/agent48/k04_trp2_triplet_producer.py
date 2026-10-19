"""Source-ordered TRP2 triplets against paired MT19937 printer recurrences.

SFT: python agents/agent48/k04_trp2_triplet_producer.py original-export.zip
The source-selected printer row129, recovery mask and acceptance hashes are excluded.
"""
from collections import defaultdict
from pathlib import Path
import hashlib
import random
import re
import struct
import sys
import zipfile
import zlib

ALL = 0xffffffff
A = 0x9908b0df
SHA_TRP = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
SHA_SPOOL = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def untemper(v):
    def right(x, shift):
        y = x
        for _ in range(6):
            y = x ^ (y >> shift)
        return y & ALL
    def left(x, shift, mask):
        y = x
        for _ in range(6):
            y = x ^ ((y << shift) & mask)
        return y & ALL
    return right(left(left(right(v, 18), 15, 0xefc60000), 7, 0x9d2c5680), 11)


def twist(x, y):
    mix = (x & 0x80000000) | (y & 0x7fffffff)
    return ((mix >> 1) ^ (A if mix & 1 else 0)) & ALL


def recorder(raw):
    assert raw[:8] == b"TRP2DUMP"
    ver, size, count = struct.unpack_from("<HHI", raw, 8)
    assert (ver, size, count, len(raw)) == (2, 24, 88, 16 + 24 * 88)
    results = []
    for i in range(count):
        block = raw[16 + i * 24:16 + (i + 1) * 24]
        ts, node, event, latch, seq, value, aux, crc = struct.unpack("<IHBBI4sII", block)
        results.append({
            "i": i, "ts": ts, "node": node, "event": event, "latch": latch,
            "seq": seq, "x": untemper(int.from_bytes(value, "little")),
            "crc_ok": zlib.crc32(block[:20]) == crc,
        })
    return results


def printer(raw):
    payloads = re.findall(rb"PAYLOAD=([0-9A-F]{32})", raw)
    assert len(payloads) == 133
    rows = [tuple(untemper(v) for v in struct.unpack("<4I", bytes.fromhex(p.decode())))
            for p in payloads]
    rows[129] = ()
    return rows


def families(records):
    result = {"file": [records],
              "timestamp": [sorted(records, key=lambda r: (r["ts"], r["i"]))]}
    for keys in (("node", "event"), ("node", "event", "latch")):
        grouped = defaultdict(list)
        for row in records:
            grouped[tuple(row[k] for k in keys)].append(row)
        for order in ("seq", "ts", "i"):
            result["_".join(keys) + "_" + order] = [
                sorted(group, key=lambda r: (r[order], r["i"]))
                for group in grouped.values()
            ]
    return result


def pair_index(rows):
    result = defaultdict(list)
    for mid, m in enumerate(rows):
        if not m:
            continue
        for end in range(mid + 1, len(rows)):
            e = rows[end]
            if not e:
                continue
            for col in range(3):
                result[(m[col] ^ e[col], m[col + 1] ^ e[col + 1])].append(
                    (mid, end, col))
    return result


def synthetic_control():
    for seed in (1, 0xABCDEF012345, 0xffffffff):
        r = random.Random(seed)
        x = [untemper(r.getrandbits(32)) for _ in range(1300)]
        at = 311
        donors = x[at:at + 4]
        middle = x[at + 397:at + 401]
        end = x[at + 624:at + 628]
        assert (twist(donors[0], donors[1]), twist(donors[1], donors[2])) == (
            middle[0] ^ end[0], middle[1] ^ end[1])
        assert twist(donors[2], donors[3]) == middle[2] ^ end[2]
    print("synthetic_triplet_positive=3")


def main(source):
    synthetic_control()
    with zipfile.ZipFile(source) as z:
        raw_recorder = z.read("evidence/recorder/trip-recorder.raw")
        raw_spool = z.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw_recorder).hexdigest() == SHA_TRP
    assert hashlib.sha256(raw_spool).hexdigest() == SHA_SPOOL
    records, rows = recorder(raw_recorder), printer(raw_spool)
    fingerprints = pair_index(rows)
    assert sum(map(len, fingerprints.values())) == 25938
    print("source_order_pairs", sum(map(len, fingerprints.values())))
    for family, groups in families(records).items():
        triplets = valid = hits = holds = 0
        for group in groups:
            for i in range(len(group) - 2):
                a, b, c = group[i:i + 3]
                triplets += 1
                if not all(r["crc_ok"] for r in (a, b, c)):
                    continue
                valid += 1
                key = (twist(a["x"], b["x"]), twist(b["x"], c["x"]))
                for mid, end, col in fingerprints.get(key, ()):
                    hits += 1
                    if i + 3 < len(group) and col <= 1:
                        d = group[i + 3]
                        if d["crc_ok"]:
                            expected = rows[mid][col + 2] ^ twist(c["x"], d["x"])
                            holds += expected == rows[end][col + 2]
        print(family, "triplets", triplets, "crc_good_triplets", valid,
              "paired_recurrences", hits, "heldout_fullword", holds)
        assert hits == holds == 0
    print("selected_row129_withheld=True commitment_unused=True")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_trp2_triplet_producer.py original-export.zip")
    main(Path(sys.argv[1]))
