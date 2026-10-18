"""Read-only, independent H-17 source-selection and decoy-resilience controls.

Re-derive K02, K03, and K07 without importing the repository replay. Then
inject synthetic rows into in-memory source copies, retaining all originals.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
if not (ROOT / "evidence").is_dir():
    ROOT = ROOT / "resources"
EVIDENCE = ROOT / "evidence"
ACCEPTANCE = json.loads((ROOT / "acceptance.json").read_text(encoding="utf-8"))
ROUTING = json.loads((EVIDENCE / "recovery-routing.json").read_text(encoding="utf-8"))


def original_rows(path: str) -> list[dict]:
    return [json.loads(line) for line in (EVIDENCE / path).read_text(encoding="utf-8").splitlines() if line]


def highest(rows: list[dict], identifier: str, revision: str, count: int) -> list[dict]:
    selected = {}
    for row in rows:
        i = row[identifier]
        if 0 <= i < count and (i not in selected or row[revision] > selected[i][revision]):
            selected[i] = row
    assert len(selected) == count
    return [selected[i] for i in range(count)]


def sha16(data: bytes) -> str:
    return hashlib.sha256(data).digest()[:16].hex().upper()


def derive_k02(rows: list[dict]) -> str:
    cfg = ROUTING["K02"]
    start = datetime.fromisoformat(cfg["start_utc"])
    end = datetime.fromisoformat(cfg["end_utc_exclusive"])
    accepted = [r for r in rows if r["tag"] == "LT-204" and r["field"] == "DIAG_WORD"
                and r["quality"] == "GOOD" and r["state"] == "HOLD"
                and r["unit"] == "raw_u16"
                and start <= datetime.fromisoformat(r["ts"]).astimezone(timezone.utc) < end]
    ordered = highest(accepted, "seq", "revision", 8)
    return sha16(struct.pack(">8H", *(r["value"] for r in ordered)))


def derive_k03(rows: list[dict]) -> str:
    mail = " ".join((EVIDENCE / "mail/04.eml").read_text(encoding="utf-8").split())
    match = re.search(r"witness walk was ([ABCD](?:,\s*[ABCD]){3})", mail)
    assert match is not None
    order = [s.strip() for s in match.group(1).split(",")]
    accepted = [r for r in rows if r["permit"] == "PTW-417" and r["state"] == "CLOSED"
                and r["fitment"] == "AS_LEFT" and r["signed"] is True]
    serials = "|".join(max((r for r in accepted if r["bay"] == bay),
                           key=lambda r: r["revision"])["serial"] for bay in order)
    return sha16(serials.encode("ascii"))


def derive_k07(rows: list[dict]) -> str:
    mail = " ".join((EVIDENCE / "mail/13.eml").read_text(encoding="utf-8").split())
    match = re.search(r"final custodian handoff is (AX-\d+)", mail)
    assert match is not None
    transfer = match.group(1)
    commits = [r for r in rows if r["kind"] == "COMMIT" and r["transfer"] == transfer
               and r["dry_run"] is False and r["object"] == "IR-261003-H17"]
    assert len(commits) == 1 and commits[0]["chunks"] == 8
    parts = [r for r in rows if r["kind"] == "CHUNK" and r["transfer"] == transfer
             and r["object"] == "IR-261003-H17"]
    seq = highest(parts, "seq", "attempt", 8)
    return sha16(bytes.fromhex("".join(r["checkpoint"] for r in seq)))


def main() -> None:
    checks = {
        "K02": ("telemetry/freeze-export.jsonl", derive_k02),
        "K03": ("maintenance/seal-receipts.jsonl", derive_k03),
        "K07": ("transfers/transfer-audit.jsonl", derive_k07),
    }
    baseline = {}
    source_rows = {}
    for slot, (path, fn) in checks.items():
        rows = original_rows(path)
        source_rows[slot] = rows
        baseline[slot] = fn(rows)
        assert hashlib.sha256(bytes.fromhex(baseline[slot])).hexdigest() == ACCEPTANCE["slot_sha256"][slot], slot

    tests: list[tuple[str, dict, bool]] = []
    k02 = {"ts": "2026-10-03T21:13:41+00:00", "tag": "LT-204", "field": "DIAG_WORD",
           "value": 1, "unit": "raw_u16", "quality": "GOOD", "state": "HOLD", "seq": 0, "revision": 9999}
    tests.extend([
        ("K02 high-revision SUSPECT", {**k02, "quality": "SUSPECT"}, False),
        ("K02 high-revision at exclusive end", {**k02, "ts": "2026-10-03T21:13:48+00:00"}, False),
        ("K02 high-revision valid in-window", k02, True),
    ])
    k03 = {"permit": "PTW-417", "bay": "B", "revision": 9999, "state": "CLOSED",
           "fitment": "AS_LEFT", "signed": True, "serial": "SG-00000000"}
    tests.extend([
        ("K03 unsigned higher revision", {**k03, "signed": False}, False),
        ("K03 REMOVED higher revision", {**k03, "fitment": "REMOVED"}, False),
        ("K03 signed CLOSED AS_LEFT higher revision", k03, True),
    ])
    k07 = {"kind": "CHUNK", "transfer": "AX-7782", "seq": 0, "attempt": 9999,
           "checkpoint": "0000", "bytes": 1048576, "object": "IR-261003-H17"}
    tests.extend([
        ("K07 wrong-transfer higher attempt", {**k07, "transfer": "AX-7783"}, False),
        ("K07 correct-transfer higher attempt", k07, True),
        ("K07 extra dry-run COMMIT", {"kind": "COMMIT", "transfer": "AX-7782", "dry_run": True,
                                      "object": "IR-261003-H17", "chunks": 8}, False),
    ])

    results = []
    for label, synthetic, should_change in tests:
        slot = label[:3]
        (_, derive) = checks[slot]
        candidate = derive(source_rows[slot] + [synthetic])
        observed_changed = candidate != baseline[slot]
        assert observed_changed == should_change, label
        matched = hashlib.sha256(bytes.fromhex(candidate)).hexdigest() == ACCEPTANCE["slot_sha256"][slot]
        assert matched == (not should_change), label
        results.append({"control": label, "selection": "CHANGED" if observed_changed else "UNCHANGED",
                        "original_commitment": "NO_MATCH" if observed_changed else "PASS"})
    print(json.dumps({"baseline_pass": list(checks), "controls_passed": len(results),
                      "controls": results}, indent=2))


if __name__ == "__main__":
    main()
