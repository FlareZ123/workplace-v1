"""Agent 41: reproducible K04 two-window low31 seven-bit completion scan.

Source SHA-pinned original TRP2, RC17 and printer files; selected row129 fully
withheld. This driver compiles k04_low31_crossrun.c, then tests 298x298x128
source-derived coupon assignments against the unchanged original K04 SHA256.
Linux/CI requirements: C compiler and libcrypto development library.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import struct
import subprocess
import tempfile
import zlib

ROOT = Path(__file__).resolve().parents[2] / "resources"
E = ROOT / "evidence"
FILES = {
    "spool": E / "print/spool-reconstruction.log",
    "recorder": E / "recorder/trip-recorder.raw",
    "procedure": E / "procedures/RC-17-scans.txt",
}
SHA = {
    "spool": "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083",
    "recorder": "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba",
    "procedure": "a4b649fdbb6909115fb9505133012b5c1dda42141aafc1c6ec756199ddf1fc6d",
}


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


def recorder_runs(data):
    assert data[:8] == b"TRP2DUMP"
    assert struct.unpack("<HHI", data[8:16]) == (2, 24, 88)
    records = []
    for i in range(88):
        raw = data[16+24*i:16+24*(i+1)]
        ts, node, event, latch, seq = struct.unpack("<IHBBI", raw[:12])
        records.append({
            "i": i, "ts": ts, "node": node, "event": event,
            "latch": latch, "seq": seq,
            "valid": zlib.crc32(raw[:20]) == struct.unpack("<I", raw[20:24])[0],
            "state": untemper(int.from_bytes(raw[12:16], "little")),
        })

    groups = {}

    def collect(label, items):
        valid = [r for r in items if r["valid"]]
        for j in range(len(valid)-3):
            block = valid[j:j+4]
            indexes = tuple(r["i"] for r in block)
            groups.setdefault(indexes, (
                tuple(r["state"] for r in block), label))

    collect("recorder-file", records)
    collect("recorder-time", sorted(records, key=lambda x: (x["ts"], x["i"])))
    for node in (49, 50):
        cohort = [r for r in records if r["node"] == node]
        collect(f"node{node}-seq", sorted(cohort,
                key=lambda x: (x["seq"], x["latch"], x["i"])))
        collect(f"node{node}-file", cohort)
        collect(f"node{node}-time", sorted(cohort,
                key=lambda x: (x["ts"], x["i"])))
        for event in {r["event"] for r in cohort}:
            batch = [r for r in cohort if r["event"] == event]
            collect(f"node{node}-event{event}-seq", sorted(batch,
                    key=lambda x: (x["seq"], x["latch"], x["i"])))

    assert len(groups) == 291, len(groups)
    start = int(datetime(2026, 10, 3, 21, 14,
                         tzinfo=timezone.utc).timestamp())
    eligible = [
        r for r in records if r["node"] == 49 and r["event"] == 82
        and r["valid"] and start <= r["ts"] < start + 8
    ]
    latest = [
        max((r for r in eligible if r["latch"] == latch),
            key=lambda r: r["seq"])
        for latch in range(4)
    ]
    ordered = list(groups.values())
    # The explicit K05 latch sequence repeats one naturally enumerated run.
    ordered.append((tuple(r["state"] for r in latest),
                    "K05-latch-ordered-repeat"))
    assert len(ordered) == 292
    return ordered


def procedure_runs(data):
    pages = []
    for page in data.decode("utf-8").split("\f"):
        header = re.search(r"REV ([^ /]+) / SECTION ([A-Z]+)", page)
        token = re.search(r"Footer control strip:\s*([0-9A-F]{8})", page)
        if header and token:
            state = untemper(int.from_bytes(bytes.fromhex(token[1]), "little"))
            pages.append((header[1], header[2], state))
    assert len(pages) == 12
    service = ("DRAIN", "ISOLATE", "PURGE", "VERIFY")
    result = []
    for rev in ("B", "C", "D-draft"):
        entries = [v for v in pages if v[0] == rev]
        assert len(entries) == 4
        result.append((tuple(v[2] for v in entries), f"RC17-{rev}-scan"))
        result.append((tuple(v[2] for v in sorted(
            entries, key=lambda x: service.index(x[1]))),
            f"RC17-{rev}-service"))
    return result


def main():
    data = {k: file.read_bytes() for k, file in FILES.items()}
    assert all(sha256(data[k]).hexdigest() == SHA[k] for k in FILES)
    runs = recorder_runs(data["recorder"]) + procedure_runs(data["procedure"])
    assert len(runs) == 298
    source_rows = [line for line in data["spool"].decode("ascii").splitlines()
                   if "PAYLOAD=" in line]
    assert len(source_rows) == 133
    retained43 = re.search(r"PAYLOAD=([0-9A-F]{32})", source_rows[43])[1]
    x3 = untemper(int.from_bytes(bytes.fromhex(retained43)[12:16], "little"))
    source_rows[129] = "[WITHHELD]"
    route = json.loads((E / "recovery-routing.json").read_text())
    acceptance = json.loads((ROOT / "acceptance.json").read_text())
    mask = bytes.fromhex(route["K04"]["masked_component"])
    commitment = bytes.fromhex(acceptance["slot_sha256"]["K04"])

    with tempfile.TemporaryDirectory() as temp:
        t = Path(temp)
        binary = t / "witnesses.bin"
        with binary.open("wb") as out:
            out.write(struct.pack("<I", len(runs)))
            for states, label in runs:
                out.write(struct.pack("<4I", *(x & 0x7FFFFFFF
                                              for x in states)))
            out.write(struct.pack("<I", x3))
            out.write(mask)
            out.write(commitment)

        executable = t / "scan"
        source = Path(__file__).with_suffix(".c")
        subprocess.run(["cc", "-O3", str(source), "-lcrypto",
                        "-o", str(executable)], check=True)
        result = subprocess.run([str(executable), str(binary)],
                                check=True, capture_output=True, text=True)
        print(result.stdout)
        assert "TESTED=11366912 HITS=0" in result.stdout
    print("PASS pinned unchanged sources; selected row129 withheld; no accepted K04")


if __name__ == "__main__":
    main()
