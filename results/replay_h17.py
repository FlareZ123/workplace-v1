"""Replay the H-17 recovery components from original local evidence.

Python 3 standard library; no writes, network access, or equipment interaction.
Run from a repository checkout: python results/replay_h17.py
The generated JSON includes source-derived intermediate values and acceptance status.
"""
from __future__ import annotations

import configparser
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1] / "resources"
E = ROOT / "evidence"
ROUTING = json.loads((E / "recovery-routing.json").read_text(encoding="utf-8"))
TARGETS = json.loads((ROOT / "acceptance.json").read_text(encoding="utf-8"))


def email(ref):
    return (E / "mail" / (ref + ".eml")).read_text(encoding="utf-8")


def records(name):
    return [json.loads(s) for s in (E / name).read_text(encoding="utf-8").splitlines() if s.strip()]


def head16(data):
    return hashlib.sha256(data).digest()[:16].hex().upper()


def winners(rows, key, rank, n):
    selected = {}
    for row in rows:
        i = row[key]
        if i in range(n) and (i not in selected or row[rank] > selected[i][rank]):
            selected[i] = row
    assert set(selected) == set(range(n)), (key, selected)
    return [selected[i] for i in range(n)]


def in_window(ts, config):
    timestamp = datetime.fromisoformat(ts).astimezone(timezone.utc)
    return (datetime.fromisoformat(config["start_utc"]) <= timestamp
            < datetime.fromisoformat(config["end_utc_exclusive"]))


def reduce_k01():
    pairs = re.findall(r"WN-14\s*/\s*group\s+([A-D])\s*/\s*([0-9A-F]{8})",
                       email("03") + "\n" + email("06"))
    assert len(pairs) == 4 and len(dict(pairs)) == 4
    assert "A, then B, then C, then D" in " ".join(email("14").split())
    groups = dict(pairs)
    return "".join(groups[i] for i in "ABCD"), {"ink_groups": groups}


def reduce_k02():
    cfg = ROUTING["K02"]
    filtered = [r for r in records("telemetry/freeze-export.jsonl")
                if r["tag"] == "LT-204" and r["field"] == "DIAG_WORD"
                and r["quality"] == "GOOD" and r["state"] == "HOLD"
                and r["unit"] == "raw_u16" and in_window(r["ts"], cfg)]
    selected = winners(filtered, "seq", "revision", 8)
    ints = [r["value"] for r in selected]
    raw = struct.pack(">8H", *ints)
    return head16(raw), {"raw_hex": raw.hex().upper(), "values": ints,
                         "revisions": [r["revision"] for r in selected]}


def reduce_k03():
    text = " ".join(email("04").split())
    match = re.search(r"witness walk was ([ABCD](?:,\s*[ABCD]){3})", text)
    assert match
    order = [s.strip() for s in match.group(1).split(",")]
    rows = [r for r in records("maintenance/seal-receipts.jsonl")
            if r["permit"] == "PTW-417" and r["state"] == "CLOSED"
            and r["fitment"] == "AS_LEFT" and r["signed"] is True]
    chosen = [max((r for r in rows if r["bay"] == bay),
                  key=lambda r: r["revision"]) for bay in order]
    serials = "|".join(r["serial"] for r in chosen)
    return head16(serials.encode("ascii")), {"bay_order": order, "serials": serials,
                                             "revisions": [r["revision"] for r in chosen]}


def reduce_k04_diagnostic():
    labels = configparser.ConfigParser()
    labels.read(E / "archive-labels.ini", encoding="utf-8")
    job = labels["printer_routes_2026-09-01_to_2026-10-03"]["ESC-N"]
    lines = (E / "print/spool-reconstruction.log").read_text(encoding="utf-8").splitlines()
    rows = [dict(re.findall(r"\b(\w+)=(\S+)", line)) for line in lines]
    acknowledged = [r for r in rows if r.get("JOB") == job
                    and r.get("STATE") == "ACK" and r.get("CLASS") == "RECOVER"]
    assert acknowledged and "last acknowledged attempt" in " ".join(email("16").lower().split())
    row = max(acknowledged, key=lambda r: int(r["ATTEMPT"]))
    payload = bytes.fromhex(row["PAYLOAD"])
    mask = bytes.fromhex(ROUTING["K04"]["masked_component"])
    assert len(payload) == len(mask) == 16
    component = bytes(a ^ b for a, b in zip(payload, mask)).hex().upper()
    return component, {"logical_route": "ESC-N", "job": job, "attempt": row["ATTEMPT"],
                       "payload_hex": payload.hex().upper(),
                       "mask_hex": mask.hex().upper()}


def reduce_k05():
    data = (E / "recorder/trip-recorder.raw").read_bytes()
    signature, schema, record_size, count = struct.unpack_from("<8sHHI", data)
    assert (signature, schema, record_size) == (b"TRP2DUMP", 2, 24)
    assert len(data) == 16 + count * record_size
    cfg = ROUTING["K05"]
    start = int(datetime.fromisoformat(cfg["start_utc"]).timestamp())
    end = int(datetime.fromisoformat(cfg["end_utc_exclusive"]).timestamp())
    valid = []
    bad_crc = 0
    for offset in range(16, len(data), record_size):
        raw = data[offset:offset + record_size]
        ts, node, event, latch, sequence, word, auxiliary, crc = struct.unpack("<IHBBI4sII", raw)
        if zlib.crc32(raw[:20]) != crc:
            bad_crc += 1
            continue
        if node == cfg["node"] and event == cfg["event"] and start <= ts < end:
            valid.append({"latch": latch, "sequence": sequence, "word": word})
    selected = winners(valid, "latch", "sequence", 4)
    component = b"".join(r["word"] for r in selected).hex().upper()
    return component, {"record_count": count, "bad_crc": bad_crc,
                       "sequences": [r["sequence"] for r in selected],
                       "words": [r["word"].hex().upper() for r in selected]}


def reduce_k06():
    assert "revision C of RC-17" in email("11")
    labels = configparser.ConfigParser()
    labels.read(E / "archive-labels.ini", encoding="utf-8")
    order = labels["archive"]["service_order"].split(",")
    scans = (E / "procedures/RC-17-scans.txt").read_text(encoding="utf-8")
    pairs = re.findall(r"DOCUMENT RC-17 / REV C / SECTION ([A-Z]+)[\s\S]*?"
                       r"Footer control strip: ([0-9A-F]{8})", scans)
    strips = dict(pairs)
    assert len(pairs) == len(strips) == 4 and set(order) == set(strips)
    return "".join(strips[s] for s in order), {"service_order": order,
                                                "strips": [strips[s] for s in order]}


def reduce_k07():
    ref = re.search(r"final custodian handoff is (AX-\d+)", email("13"))
    assert ref
    transfer = ref.group(1)
    all_rows = records("transfers/transfer-audit.jsonl")
    commits = [r for r in all_rows if r["kind"] == "COMMIT"
               and r["transfer"] == transfer and r["dry_run"] is False
               and r["object"] == "IR-261003-H17"]
    assert len(commits) == 1 and commits[0]["chunks"] == 8
    chunks = [r for r in all_rows if r["kind"] == "CHUNK"
              and r["transfer"] == transfer and r["object"] == "IR-261003-H17"]
    chosen = winners(chunks, "seq", "attempt", 8)
    raw = "".join(r["checkpoint"] for r in chosen)
    assert len(raw) == 32
    return head16(bytes.fromhex(raw)), {"transfer": transfer,
                                        "checkpoint_hex": raw,
                                        "attempts": [r["attempt"] for r in chosen]}


def main():
    candidate = {f"K{i:02d}": None for i in range(1, 9)}
    audit = {}
    funcs = {"K01": reduce_k01, "K02": reduce_k02, "K03": reduce_k03,
             "K05": reduce_k05, "K06": reduce_k06, "K07": reduce_k07}
    for slot, func in funcs.items():
        value, detail = func()
        assert re.fullmatch(r"[0-9A-F]{32}", value)
        digest = hashlib.sha256(bytes.fromhex(value)).hexdigest()
        assert digest == TARGETS["slot_sha256"][slot], slot
        candidate[slot] = value
        audit[slot] = {"status": "PASS", "sha256": digest, **detail}
    k04, detail = reduce_k04_diagnostic()
    actual = hashlib.sha256(bytes.fromhex(k04)).hexdigest()
    assert actual != TARGETS["slot_sha256"]["K04"]
    audit["K04"] = {"status": "NO_MATCH", "excluded_component": k04,
                    "actual_sha256": actual, **detail}
    audit["K08"] = {"status": "MISSING", "explanation":
        "No authenticated exact final keeper caption in available notes and mail."}
    print(json.dumps({"candidate": candidate, "audit": audit,
                      "verified_slots": 6, "combined": "INCOMPLETE",
                      "accepted": False}, indent=2))


if __name__ == "__main__":
    main()
