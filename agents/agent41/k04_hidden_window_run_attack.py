"""Targeted K04 paired-hidden-window attack with original 4-byte control runs.

Agent41, 19 Oct 2026. Source-derived candidate corpus and synthetic control.
Never reads the selected row129 payload; original files are read-only.
"""
from collections import defaultdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import struct
import zlib
from random import Random

HASHES = {
    "spool": "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083",
    "recorder": "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba",
    "procedure": "a4b649fdbb6909115fb9505133012b5c1dda42141aafc1c6ec756199ddf1fc6d",
}
SERVICE = ("DRAIN", "ISOLATE", "PURGE", "VERIFY")


def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9D2C5680
    x ^= (x << 15) & 0xEFC60000
    return (x ^ (x >> 18)) & 0xFFFFFFFF


def untemper(y):
    x = y ^ (y >> 18)
    x ^= (x << 15) & 0xEFC60000
    z = x
    for _ in range(5):
        z = x ^ ((z << 7) & 0x9D2C5680)
    x = z
    for _ in range(3):
        z = x ^ (z >> 11)
    return z & 0xFFFFFFFF


def twist(a, b):
    x = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return (x >> 1) ^ (0x9908B0DF if b & 1 else 0)


def predict(x3, early, late):
    # Conditional d=11,p=627: row129 state p+j equals middle
    # p-227+j XOR twist(earlier p-624+j, earlier p-623+j).
    states = [late[j] ^ twist(x3 if j == 0 else early[j-1], early[j])
              for j in range(4)]
    return b"".join(temper(x).to_bytes(4, "little") for x in states)


def recorder_runs(data):
    assert data[:8] == b"TRP2DUMP"
    version, size, count = struct.unpack("<HHI", data[8:16])
    assert (version, size, count) == (2, 24, 88)
    r = []
    for i in range(count):
        b = data[16+24*i:16+24*(i+1)]
        ts, node, event, latch, seq = struct.unpack("<IHBBI", b[:12])
        r.append(dict(i=i, ts=ts, node=node, event=event, latch=latch,
                      seq=seq, valid=zlib.crc32(b[:20]) == struct.unpack("<I", b[20:24])[0],
                      state=untemper(int.from_bytes(b[12:16], "little"))))
    runs = {}
    def collect(label, items):
        v = [x for x in items if x["valid"]]
        for j in range(len(v)-3):
            block = v[j:j+4]
            indexes = tuple(x["i"] for x in block)
            runs.setdefault(indexes, (tuple(x["state"] for x in block), label))
    collect("recorder-file", r)
    collect("recorder-time", sorted(r, key=lambda x:(x["ts"], x["i"])))
    for node in (49, 50):
        s = [x for x in r if x["node"] == node]
        collect(f"node{node}-seq", sorted(s,key=lambda x:(x["seq"],x["latch"],x["i"])))
        collect(f"node{node}-file", s)
        collect(f"node{node}-time", sorted(s,key=lambda x:(x["ts"],x["i"])))
        for event in {x["event"] for x in s}:
            cohort = [x for x in s if x["event"] == event]
            collect(f"node{node}-event{event}-seq",
                    sorted(cohort,key=lambda x:(x["seq"],x["latch"],x["i"])))
    assert len(runs) == 291, len(runs)
    start = int(datetime(2026,10,3,21,14,0,tzinfo=timezone.utc).timestamp())
    eligible = [x for x in r if x["node"] == 49 and x["event"] == 82 and x["valid"]
                and start <= x["ts"] < start+8]
    latest = [max((x for x in eligible if x["latch"] == j),key=lambda x:x["seq"])
              for j in range(4)]
    # K05 latest-per-latch order is already among the natural recorder runs.
    # Preserve it as a separately labelled, intentionally repeated assignment.
    result = list(runs.values())
    assert len(result) == 291
    result.append((tuple(x["state"] for x in latest), "K05-latch-repeated"))
    return result


def procedure_runs(text):
    pages = []
    for page in text.split("\f"):
        header = re.search(r"REV ([^ /]+) / SECTION ([A-Z]+)", page)
        strip = re.search(r"Footer control strip:\s*([0-9A-F]{8})", page)
        if header and strip:
            pages.append((header[1], header[2],
                          untemper(int.from_bytes(bytes.fromhex(strip[1]),"little"))))
    assert len(pages) == 12
    result = []
    for rev in ("B", "C", "D-draft"):
        p = [x for x in pages if x[0] == rev]
        assert len(p)==4
        result.append((tuple(x[2] for x in p),f"RC17-{rev}-scan"))
        result.append((tuple(x[2] for x in sorted(p,key=lambda x:SERVICE.index(x[1]))),
                       f"RC17-{rev}-service"))
    return result


def main():
    root = Path(__file__).resolve().parents[2] / "resources"
    paths = {"spool":root/"evidence/print/spool-reconstruction.log",
             "recorder":root/"evidence/recorder/trip-recorder.raw",
             "procedure":root/"evidence/procedures/RC-17-scans.txt"}
    data = {k: p.read_bytes() for k,p in paths.items()}
    assert all(sha256(data[k]).hexdigest()==HASHES[k] for k in paths)
    rows = [x for x in data["spool"].decode("ascii").splitlines() if "PAYLOAD=" in x]
    assert len(rows) == 133
    x3 = untemper(int.from_bytes(bytes.fromhex(
        re.search(r"PAYLOAD=([0-9A-F]{32})",rows[43])[1])[12:16],"little"))
    rows[129] = "[WITHHELD]"  # Never use the suspect coupon.
    runs = recorder_runs(data["recorder"]) + procedure_runs(data["procedure"].decode("utf-8"))
    assert len(runs)==298, len(runs)

    g = Random(33221)
    sample = [untemper(g.getrandbits(32)) for _ in range(632)]
    assert predict(sample[3],sample[4:8],sample[400:404]) == b"".join(
        temper(w).to_bytes(4,"little") for w in sample[627:631])

    route = json.loads((root/"evidence/recovery-routing.json").read_text())
    acceptance = json.loads((root/"acceptance.json").read_text())
    mask = bytes.fromhex(route["K04"]["masked_component"])
    want = bytes.fromhex(acceptance["slot_sha256"]["K04"])
    hits = []
    for early,label_early in runs:
        for late,label_late in runs:
            payload = predict(x3,early,late)
            coupon = bytes(a^b for a,b in zip(payload,mask))
            if sha256(coupon).digest()==want:
                hits.append((label_early,label_late,coupon.hex().upper()))
    assert not hits, hits
    print("PASS synthetic exact four-word MT reconstruction")
    print("CRC-valid recorder and RC17 ordered runs:", len(runs))
    print("Source-selected K04 two-window pairs tested:",len(runs)**2)
    print("Original K04 commitment matches:",len(hits))
    print("Original selected row129 payload and original verifier never read or changed")


if __name__ == "__main__":
    main()
