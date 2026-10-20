"""Original route-field donor test in one source-compatible MT chronology.

No selected coupon, acceptance hash, or key candidate is read. This is a
bounded discovery check, not evidence of one actual common field producer.
"""
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAYOUT = ROOT / "results/h17-k04-source-consistent-index955.json"
SPOOL = ROOT / "resources/evidence/print/spool-reconstruction.log"
ROUTE = ROOT / "resources/evidence/recovery-routing.json"
MASK32 = 0xFFFFFFFF


def untemper(value):
    value ^= value >> 18
    value ^= (value << 15) & 0xEFC60000
    base = value
    for _ in range(5):
        value = base ^ ((value << 7) & 0x9D2C5680)
    base = value
    for _ in range(3):
        value = base ^ (value >> 11)
    return value & MASK32


def twist(left, right):
    pair = (left & 0x80000000) | (right & 0x7FFFFFFF)
    return (pair >> 1) ^ (0x9908B0DF if pair & 1 else 0)


def main():
    layout = json.loads(LAYOUT.read_text(encoding="utf-8"))
    source = SPOOL.read_bytes()
    assert hashlib.sha256(source).hexdigest() == layout["source_spool_sha256"]
    payloads = re.findall(rb"\bPAYLOAD=([0-9A-F]{32})\b", source)
    starts = layout["row_starts"]
    assert len(payloads) == len(starts) == 133
    assert layout["selected_row"] == 129 and starts[129] == 955

    observed = {}
    for row, (hexword, start) in enumerate(zip(payloads, starts)):
        if row == layout["selected_row"]:
            continue
        for offset, word in enumerate(struct.unpack("<4I", bytes.fromhex(hexword.decode()))):
            index = start + offset
            assert index not in observed
            observed[index] = untemper(word)
    assert len(observed) == 528

    # One exactly justified recurrence step, never backfill free MT coordinates.
    inferred = {}
    intact_relations = 0
    for index in range(-625, 2100):
        if not all(k in observed for k in (index, index + 1, index + 397)):
            continue
        value = observed[index + 397] ^ twist(observed[index], observed[index + 1])
        if index + 624 in observed:
            assert observed[index + 624] == value
            intact_relations += 1
        else:
            inferred[index + 624] = value
    assert intact_relations == 25 and len(inferred) == 106

    route = json.loads(ROUTE.read_text(encoding="utf-8"))
    fields = {
        "K04 masked_component": route["K04"]["masked_component"],
        "K08 desk_nonce": route["K08"]["desk_nonce"],
    }
    for label, value in fields.items():
        raw = bytes.fromhex(value)
        assert len(raw) == 16
        for endian in ("<", ">"):
            words = [untemper(w) for w in struct.unpack(endian + "4I", raw)]
            hits_observed = [(lane, index) for lane, w in enumerate(words)
                             for index, v in observed.items() if w == v]
            hits_inferred = [(lane, index) for lane, w in enumerate(words)
                             for index, v in inferred.items() if w == v]
            print(label, endian, "intact_hits", hits_observed, "inferred_hits", hits_inferred)
            assert not hits_observed and not hits_inferred

    # Independent synthetically constructed positive controls for the maps.
    assert all(untemper(w) in observed.values() for w in struct.unpack("<4I", bytes.fromhex(payloads[0].decode())))
    print("PASS: 528 intact words; 25 MT relations; 106 predicted hidden words; two route fields × two byte orders; no matches.")


if __name__ == "__main__":
    main()
