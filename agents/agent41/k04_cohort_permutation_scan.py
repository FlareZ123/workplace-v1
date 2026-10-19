"""K04 original-source CRC-aware recorder-latch permutation cracking SFT.

Run: python agents/agent41/k04_cohort_permutation_scan.py
C compiler and OpenSSL libcrypto required. Original selected row129 withheld.
The original acceptance K04 SHA is used only for checking finished coupons.
"""
from datetime import datetime, timezone
from hashlib import sha256
from itertools import permutations
from pathlib import Path
from random import Random
import json
import re
import struct
import subprocess
import tempfile
import zlib

import k04_low31_crossrun as prior

ROOT = Path(__file__).resolve().parents[2] / "resources"
E = ROOT / "evidence"
FILES = {
    "spool": E / "print/spool-reconstruction.log",
    "recorder": E / "recorder/trip-recorder.raw",
    "procedure": E / "procedures/RC-17-scans.txt",
}


def records(data):
    assert data[:8] == b"TRP2DUMP"
    assert struct.unpack("<HHI", data[8:16]) == (2, 24, 88)
    result = []
    for i in range(88):
        b = data[16+24*i:16+24*(i+1)]
        timestamp, node, event, latch, seq = struct.unpack("<IHBBI", b[:12])
        result.append({
            "i": i, "node": node, "event": event, "latch": latch, "seq": seq,
            "valid": zlib.crc32(b[:20]) == struct.unpack("<I", b[20:24])[0],
            "state": prior.untemper(int.from_bytes(b[12:16], "little")) & 0x7FFFFFFF,
        })
    return result


def permutations_in_source_cohorts(rows, include_bad):
    """Enumerate all 4! within-cohort source word orderings.

    Four original node49/event82 sequence cohorts, each has one latch0..3.
    Cohort900 contains four bad-CRC raw records and is auxiliary-only.
    """
    runs = []
    for ids in (range(200, 204), range(300, 304),
                range(900, 904), range(990, 994)):
        cohort = [
            next(row for row in rows if row["node"] == 49
                 and row["event"] == 82 and row["seq"] == seq)
            for seq in ids
        ]
        assert sorted(row["latch"] for row in cohort) == [0, 1, 2, 3]
        if not include_bad and any(not row["valid"] for row in cohort):
            continue
        for ordered in permutations(cohort):
            label = f"seq{ids.start}-records-" + "-".join(
                str(row["i"]) for row in ordered)
            runs.append((tuple(row["state"] for row in ordered), label))
    assert len(runs) == (96 if include_bad else 72)
    return runs


def temper(word):
    word ^= word >> 11
    word ^= (word << 7) & 0x9D2C5680
    word ^= (word << 15) & 0xEFC60000
    return (word ^ (word >> 18)) & 0xFFFFFFFF


def invoke(executable, runs, novel, x3, mask, commitment):
    with tempfile.TemporaryDirectory() as dirname:
        filename = Path(dirname) / "runs.bin"
        with filename.open("wb") as f:
            f.write(struct.pack("<II", len(runs), novel))
            for words, label in runs:
                f.write(struct.pack("<4I", *words))
            f.write(struct.pack("<I", x3))
            f.write(mask)
            f.write(commitment)
        result = subprocess.run(
            [str(executable), str(filename)],
            check=True, capture_output=True, text=True)
        return result.stdout.strip()


def main():
    data = {key: filename.read_bytes() for key, filename in FILES.items()}
    assert all(sha256(data[key]).hexdigest() == prior.SHA[key]
               for key in FILES)
    rows = records(data["recorder"])
    old = prior.recorder_runs(data["recorder"]) + prior.procedure_runs(data["procedure"])
    assert len(old) == 298

    spool = [line for line in data["spool"].decode().splitlines()
             if line.startswith("2026-")]
    assert len(spool) == 133
    row43 = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", spool[43])[1])
    x3 = prior.untemper(int.from_bytes(row43[12:16], "little"))
    spool[129] = "[WITHHELD: selected K04 printer row]"

    route = json.loads((E / "recovery-routing.json").read_text())
    acceptance = json.loads((ROOT / "acceptance.json").read_text())
    mask = bytes.fromhex(route["K04"]["masked_component"])
    commitment = bytes.fromhex(acceptance["slot_sha256"]["K04"])

    with tempfile.TemporaryDirectory() as dirname:
        executable = Path(dirname) / "cohort_scan"
        subprocess.run(
            ["cc", "-O3", str(Path(__file__).with_suffix(".c")),
             "-lcrypto", "-o", str(executable)], check=True)

        # Independent actual Python MT19937 seeded synthetic true target.
        generator = Random(20261019)
        states = [prior.untemper(generator.getrandbits(32))
                  for _ in range(635)]
        payload = b"".join(temper(x).to_bytes(4, "little")
                           for x in states[627:631])
        coupon = bytes(a ^ b for a, b in zip(payload, mask))
        synthetic = [
            (tuple(x & 0x7FFFFFFF for x in states[4:8]), "early"),
            (tuple(x & 0x7FFFFFFF for x in states[400:404]), "late"),
        ]
        synthetic_out = invoke(executable, synthetic, 2, states[3],
                               mask, sha256(coupon).digest())
        assert "HIT early=0 late=1" in synthetic_out, synthetic_out
        print("ACTUAL_CPYTHON_SEEDED_SYNTHETIC_TARGET_PASS")

        valid = permutations_in_source_cohorts(rows, False)
        output = invoke(executable, valid + old, len(valid),
                        x3, mask, commitment)
        print("ORIGINAL_CRC_VALID_COHORTS", output)
        assert "TESTED=6156288 HITS=0" in output

        full = permutations_in_source_cohorts(rows, True)
        output = invoke(executable, full + old, len(full),
                        x3, mask, commitment)
        print("ORIGINAL_BAD_CRC_AS_AUXILIARY_ONLY", output)
        assert "TESTED=8503296 HITS=0" in output
    print("SELECTED_K04_ROW129_WITHHELD; NO_ACCEPTED_K04")


if __name__ == "__main__":
    main()
