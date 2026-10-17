"""Test K04 spool reconstruction against bounded independent bit errors.

Read-only standard-library diagnostic. A failed test does not certify the
printer buffer; a passing hash would still need source/provenance review.
"""
import argparse
import configparser
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "resources"
EVIDENCE = ROOT / "evidence"


def routed_component():
    routing = json.loads((EVIDENCE / "recovery-routing.json").read_text())
    labels = configparser.ConfigParser()
    labels.read(EVIDENCE / "archive-labels.ini")
    job = labels["printer_routes_2026-09-01_to_2026-10-03"]["ESC-N"]
    rows = [dict(field.split("=", 1) for field in line.split()
                 if "=" in field)
            for line in (EVIDENCE / "print/spool-reconstruction.log").read_text().splitlines()]
    acks = [row for row in rows if row.get("JOB") == job
            and row.get("STATE") == "ACK" and row.get("CLASS") == "RECOVER"]
    row = max(acks, key=lambda r: int(r["ATTEMPT"]))
    payload = bytes.fromhex(row["PAYLOAD"])
    mask = bytes.fromhex(routing["K04"]["masked_component"])
    assert len(payload) == len(mask) == 16
    return job, row["ATTEMPT"], bytes(p ^ m for p, m in zip(payload, mask))


def run(max_flips):
    job, attempt, base = routed_component()
    target = bytes.fromhex(json.loads((ROOT / "acceptance.json").read_text())["slot_sha256"]["K04"])
    counts = {}
    for weight in range(max_flips + 1):
        count = 0
        for positions in itertools.combinations(range(128), weight):
            candidate = bytearray(base)
            for bit in positions:
                candidate[bit // 8] ^= 1 << (bit % 8)
            count += 1
            if hashlib.sha256(candidate).digest() == target:
                return {"matched": True, "candidate": candidate.hex().upper(),
                        "flipped_bit_positions": positions,
                        "counts_by_weight": {**counts, str(weight): count}}
        counts[str(weight)] = count
        print(f"tested Hamming weight {weight}: {count}", flush=True)
    return {"matched": False, "job": job, "ACK_attempt": attempt,
            "base_component": base.hex().upper(), "max_flips": max_flips,
            "counts_by_weight": counts, "total_checked": sum(counts.values())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-flips", type=int, choices=range(6), default=4)
    args = parser.parse_args()
    print(json.dumps(run(args.max_flips), indent=2))
