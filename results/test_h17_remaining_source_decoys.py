"""Read-only H-17 synthetic decoy controls for K01, K04, K05, K06.

Supports an extracted case folder or results/ in the shared repository.
Never writes or edits original evidence. Python 3 standard library only.
"""
from __future__ import annotations

import configparser
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib

HERE = Path(__file__).resolve().parent
ROOT = HERE if (HERE / "evidence").is_dir() else HERE.parent / "resources"
EVIDENCE = ROOT / "evidence"
TARGETS = json.loads((ROOT / "acceptance.json").read_text(encoding="utf-8"))
ROUTING = json.loads((EVIDENCE / "recovery-routing.json").read_text(encoding="utf-8"))
EXPECTED = {
    "mail/03.eml": "3cf886c12e094cb0362999c5a4d93f913c848a64471f833fbddbfdc2d57ff889",
    "mail/06.eml": "6049994562a82e46afd3f0231e136a1e6911cc3040d848e32eaa5771a6f8c2f3",
    "mail/14.eml": "9c86de086a1727ca09b4df6f12cf5c634eaa22a3949424171cc50b4ef9983be5",
    "recorder/trip-recorder.raw": "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba",
    "procedures/RC-17-scans.txt": "a4b649fdbb6909115fb9505133012b5c1dda42141aafc1c6ec756199ddf1fc6d",
    "print/spool-reconstruction.log": "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083",
    "archive-labels.ini": "146fa698f44bc9b9fa7a443d8dc71a2e23ff0f883dabd01512f8ade82d3666ad",
    "recovery-routing.json": "f8fcbca73d23bf1066edb88c088f89cd24cf22e7c78a4a412166254a4764d8a5",
}


def accepted(slot: str, value: str) -> bool:
    return hashlib.sha256(bytes.fromhex(value)).hexdigest() == TARGETS["slot_sha256"][slot]


def text_source(name: str) -> str:
    return (EVIDENCE / name).read_text(encoding="utf-8")


def k01(mail03: str, mail06: str) -> str:
    pairs = re.findall(r"WN-14\s*/\s*group\s+([A-D])\s*/\s*([0-9A-F]{8})", mail03 + mail06)
    assert len(pairs) == 4 and len(dict(pairs)) == 4
    return "".join(dict(pairs)[g] for g in "ABCD")


def k05(raw: bytes) -> str:
    signature, schema, record_size, count = struct.unpack_from("<8sHHI", raw)
    assert (signature, schema, record_size) == (b"TRP2DUMP", 2, 24)
    assert len(raw) == 16 + count * record_size
    route = ROUTING["K05"]
    start = int(datetime.fromisoformat(route["start_utc"]).timestamp())
    end = int(datetime.fromisoformat(route["end_utc_exclusive"]).timestamp())
    winners: dict[int, tuple[int, bytes]] = {}
    for offset in range(16, len(raw), 24):
        record = raw[offset:offset + 24]
        ts, node, event, latch, seq, word, _aux, crc = struct.unpack("<IHBBI4sII", record)
        if zlib.crc32(record[:20]) != crc:
            continue
        if node != route["node"] or event != route["event"] or not start <= ts < end:
            continue
        if latch in range(4) and (latch not in winners or seq > winners[latch][0]):
            winners[latch] = (seq, word)
    assert set(winners) == set(range(4))
    return b"".join(winners[i][1] for i in range(4)).hex().upper()


def make_record(*, ts: int, node: int = 49, event: int = 82,
                latch: int = 0, seq: int = 9999, word: bytes = b"\x11\x22\x33\x44",
                corrupt_crc: bool = False) -> bytes:
    prefix = struct.pack("<IHBBI4sI", ts, node, event, latch, seq, word, 0)
    crc = zlib.crc32(prefix) ^ int(corrupt_crc)
    return prefix + struct.pack("<I", crc)


def appended(raw: bytes, record: bytes) -> bytes:
    header = bytearray(raw[:16])
    count = struct.unpack_from("<I", header, 12)[0]
    struct.pack_into("<I", header, 12, count + 1)
    return bytes(header) + raw[16:] + record


def k06(scans: str, order: list[str]) -> str:
    pairs = re.findall(r"DOCUMENT RC-17 / REV C / SECTION ([A-Z]+)[\s\S]*?"
                       r"Footer control strip: ([0-9A-F]{8})", scans)
    strips = dict(pairs)
    assert len(pairs) == len(strips) == len(order) == 4
    return "".join(strips[section] for section in order)


def k04(spool: str, job: str) -> str:
    entries = [dict(re.findall(r"\b(\w+)=(\S+)", line)) for line in spool.splitlines()]
    acknowledged = [e for e in entries if e.get("JOB") == job
                    and e.get("CLASS") == "RECOVER" and e.get("STATE") == "ACK"]
    assert acknowledged
    chosen = max(acknowledged, key=lambda e: int(e["ATTEMPT"]))
    mask = bytes.fromhex(ROUTING["K04"]["masked_component"])
    payload = bytes.fromhex(chosen["PAYLOAD"])
    assert len(mask) == len(payload) == 16
    return bytes(a ^ b for a, b in zip(payload, mask)).hex().upper()


def main() -> None:
    assert hashlib.sha256((ROOT / "acceptance.json").read_bytes()).hexdigest() == "681739241b757b471acca4c0fef9d9d97e9493883887736d5db3b92bfb0c137f"
    for name, expected in EXPECTED.items():
        digest = hashlib.sha256((EVIDENCE / name).read_bytes()).hexdigest()
        assert digest == expected, f"evidence drift: {name}"
    print("SOURCE: 8 source-file SHA256 checks PASS")

    mail03, mail06 = text_source("mail/03.eml"), text_source("mail/06.eml")
    original_k01 = k01(mail03, mail06)
    assert accepted("K01", original_k01)
    assert k01(mail03, mail06 + "\nWN-14 / standby group B / DEADBEEF") == original_k01
    assert k01(mail03, mail06.replace("1CDE7A82", "1CDE7A83")) != original_k01
    assert not accepted("K01", k01(mail03, mail06.replace("1CDE7A82", "1CDE7A83")))
    print("K01: standby decoy ignored, changed signed ink detected")

    raw = (EVIDENCE / "recorder/trip-recorder.raw").read_bytes()
    original_k05 = k05(raw)
    assert accepted("K05", original_k05)
    inside = int(datetime.fromisoformat("2026-10-03T21:14:04+00:00").timestamp())
    outside = int(datetime.fromisoformat("2026-10-03T21:14:08+00:00").timestamp())
    controls = [
        ("high sequence with corrupted CRC", make_record(ts=inside, corrupt_crc=True)),
        ("high sequence with wrong node", make_record(ts=inside, node=50)),
        ("high sequence with wrong event", make_record(ts=inside, event=83)),
        ("high sequence at exclusive upper bound", make_record(ts=outside)),
    ]
    for label, record in controls:
        assert k05(appended(raw, record)) == original_k05, label
    changed_k05 = k05(appended(raw, make_record(ts=inside)))
    assert changed_k05 != original_k05 and not accepted("K05", changed_k05)
    print("K05: 4 rejected controls ignored, valid higher sequence selected")

    labels = configparser.ConfigParser()
    labels.read(EVIDENCE / "archive-labels.ini", encoding="utf-8")
    order = labels["archive"]["service_order"].split(",")
    scans = text_source("procedures/RC-17-scans.txt")
    original_k06 = k06(scans, order)
    assert accepted("K06", original_k06)
    assert k06("\f".join(reversed(scans.split("\f"))), order) == original_k06
    changed_k06 = k06(scans.replace("Footer control strip: 5DBF40EE", "Footer control strip: 5DBF40EF"), order)
    assert changed_k06 != original_k06 and not accepted("K06", changed_k06)
    print("K06: scanner-page permutation ignored, approved control-strip change detected")

    spool = text_source("print/spool-reconstruction.log")
    job = labels["printer_routes_2026-09-01_to_2026-10-03"]["ESC-N"]
    original_k04 = k04(spool, job)
    assert original_k04 == "2CFF149C50E54557228E7DE60B3EB7C9"
    assert not accepted("K04", original_k04)
    requested = "2026-10-03T18:04:00Z JOB=" + job + " ATTEMPT=4 STATE=REQUESTED CLASS=RECOVER PAYLOAD=" + "00" * 16
    other_job = "2026-10-03T18:05:00Z JOB=PS-261003-0448 ATTEMPT=8 STATE=ACK CLASS=RECOVER PAYLOAD=" + "FF" * 16
    assert k04(spool + "\n" + requested + "\n" + other_job, job) == original_k04
    acknowledged = "2026-10-03T18:06:00Z JOB=" + job + " ATTEMPT=5 STATE=ACK CLASS=RECOVER PAYLOAD=" + "00" * 16
    assert k04(spool + "\n" + acknowledged, job) != original_k04
    print("K04: requested/other-job decoys excluded; synthetic later same-job ACK changes candidate (original fails commitment)")
    print("PASS: all original source checks and synthetic selection controls; canonical 6/8 unchanged")


if __name__ == "__main__":
    main()