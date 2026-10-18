"""Read-only search for verbatim alternate K04 XOR-mask carriers (Agent 35).

Original-source witness model: retain the ACK-selected RECOVER payload; vary
only the reported mask, using raw 16-byte windows or decoded ASCII-hex windows
from the original 43 files. A candidate must satisfy the unchanged K04 SHA256.
The test cannot authenticate an undocumented mask source by itself.
"""
from __future__ import annotations

import argparse
import configparser
from hashlib import sha256
import json
from pathlib import Path
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--root", type=Path,
                    default=Path(__file__).resolve().parents[1] / "resources",
                    help="Extracted original ZIP root, or current repository resources")
BASE = parser.parse_args().root
# Keep the source population fixed even when an extracted case has generated
# candidates or work products alongside its 43 preservation members.
manifest = json.loads(Path(__file__).with_name("h17-source-blob-manifest.json").read_text(encoding="utf-8"))
source_paths = {item["path"] for item in manifest["files"]}
discovered = sorted(p for p in BASE.rglob("*") if p.is_file())
files = [p for p in discovered if p.relative_to(BASE).as_posix() in source_paths]
records = {p.relative_to(BASE).as_posix(): p.read_bytes() for p in files}

route = json.loads(records["evidence/recovery-routing.json"])
target = bytes.fromhex(json.loads(records["acceptance.json"])["slot_sha256"]["K04"])
mask = bytes.fromhex(route["K04"]["masked_component"])
labels = configparser.ConfigParser()
labels.read_string(records["evidence/archive-labels.ini"].decode())
job = labels["printer_routes_2026-09-01_to_2026-10-03"]["ESC-N"]
rows = []
for line in records["evidence/print/spool-reconstruction.log"].decode().splitlines():
    m = re.search(
        r"JOB=(\S+) ATTEMPT=(\d+) STATE=(\w+) CLASS=(\w+) PAYLOAD=([0-9A-F]{32})",
        line,
    )
    if m and m.group(1) == job and m.group(3) == "ACK" and m.group(4) == "RECOVER":
        rows.append((int(m.group(2)), bytes.fromhex(m.group(5))))
assert rows
payload = max(rows, key=lambda row: row[0])[1]


def hash_from_mask(candidate):
    return sha256(bytes(a ^ b for a, b in zip(payload, candidate))).digest()


controls = {
    "original": target,
    "raw_control": hash_from_mask(records["START_HERE.md"][:16]),
    "hex_control": hash_from_mask(mask),
}
counts = {"raw_windows": 0, "hex_windows": 0}
hits = {name: [] for name in controls}
for name, data in records.items():
    for i in range(max(0, len(data) - 15)):
        counts["raw_windows"] += 1
        digest = hash_from_mask(data[i:i + 16])
        for label, expected in controls.items():
            if digest == expected:
                hits[label].append((name, i, "raw"))
    for match in re.finditer(rb"[0-9A-Fa-f]{32,}", data):
        for i in range(len(match.group()) - 31):
            counts["hex_windows"] += 1
            candidate = bytes.fromhex(match.group()[i:i + 32].decode("ascii"))
            digest = hash_from_mask(candidate)
            for label, expected in controls.items():
                if digest == expected:
                    hits[label].append((name, match.start() + i, "ascii_hex"))

assert ("START_HERE.md", 0, "raw") in hits["raw_control"]
assert any(hit[0] == "evidence/recovery-routing.json" and
           hit[2] == "ascii_hex" for hit in hits["hex_control"])
print(json.dumps({
    "input_file_count": len(records),
    "ignored_non_source_files": len(discovered) - len(files),
    **counts,
    "original_commitment_matches": hits["original"],
    "control_match_counts": {
        "raw": len(hits["raw_control"]),
        "ascii_hex": len(hits["hex_control"]),
    },
    "selected_payload": payload.hex().upper(),
    "retained_mask": mask.hex().upper(),
}, indent=2))
