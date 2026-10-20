"""K02 original telemetry as hypothetical future K04 MT halfword witnesses.

Run: python -m agents.agent2.k04_k02_future_halfwords ORIGINAL_43_MEMBER.zip
Selected printer row129, K04/K08 hash commitments, mask, and verifier are withheld.
P955 is a printer-payload-consistent research fixture, not a historical producer.
"""
import hashlib
import json
import re
import struct
import sys
import zipfile
from datetime import datetime
from pathlib import Path

from agents.agent50.k04_late_three_lane_k05_sft import (
    Basis, MIN, MAX, STARTS, expressions, untemper,
)

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
TRP_SHA = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
TELEMETRY_SHA = "3787dbd6bab3930ea5293c25a995175161a1c0d7683daad29f498026e057639f"


def temper(y):
    y ^= y >> 11
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 15) & 0xEFC60000
    y ^= y >> 18
    return y & 0xFFFFFFFF


def k02_halfwords(raw):
    start = datetime.fromisoformat("2026-10-03T21:13:40+00:00")
    end = datetime.fromisoformat("2026-10-03T21:13:48+00:00")
    chosen = {}
    for line in raw.splitlines():
        item = json.loads(line)
        if (item.get("tag"), item.get("field"), item.get("quality"),
                item.get("state")) != ("LT-204", "DIAG_WORD", "GOOD", "HOLD"):
            continue
        if not start <= datetime.fromisoformat(item["ts"]) < end:
            continue
        seq = item["seq"]
        if not 0 <= seq <= 7:
            continue
        if seq not in chosen or item["revision"] > chosen[seq]["revision"]:
            chosen[seq] = item
    assert len(chosen) == 8
    values = [chosen[seq]["value"] for seq in range(8)]
    assert values == [57765, 58484, 47831, 59475, 41704, 50973, 13079, 54535]
    return values


def trp_controls(raw):
    assert raw[:8] == b"TRP2DUMP"
    assert struct.unpack_from("<I", raw, 12)[0] == 88
    found = {}
    for record in range(88):
        part = raw[16 + 24*record:16 + 24*(record+1)]
        if struct.unpack_from("<H", part, 4)[0] == 49 and part[6] == 82:
            seq = struct.unpack_from("<I", part, 8)[0]
            found[seq] = untemper(struct.unpack_from("<I", part, 12)[0])
    return found


def main(case):
    with zipfile.ZipFile(case) as original:
        spool = original.read("evidence/print/spool-reconstruction.log")
        trp = original.read("evidence/recorder/trip-recorder.raw")
        telemetry = original.read("evidence/telemetry/freeze-export.jsonl")
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    assert hashlib.sha256(trp).hexdigest() == TRP_SHA
    assert hashlib.sha256(telemetry).hexdigest() == TELEMETRY_SHA
    assert len(STARTS) == 133 and STARTS[9] == 76 and STARTS[129] == 955

    source = [struct.unpack("<4I", bytes.fromhex(
        re.search(rb"PAYLOAD=([0-9A-F]{32})", line).group(1).decode("ascii")))
        for line in spool.splitlines() if b"PAYLOAD=" in line]
    assert len(source) == 133
    halfwords = k02_halfwords(telemetry)
    controls = trp_controls(trp)
    symbolic = expressions()
    basis = Basis()

    for row, words in enumerate(source):
        if row == 129:
            continue
        for column, printed in enumerate(words):
            state = untemper(printed)
            for bit, expr in enumerate(symbolic[STARTS[row]+column-MIN]):
                basis.add(expr, (state >> bit) & 1)
    assert len(basis.b) == 15305
    for first, offset in ((200, -396), (900, -395), (990, -394)):
        for delta in range(4):
            state = controls[first+delta]
            position = STARTS[9] + offset + 3*delta
            for bit, expr in enumerate(symbolic[position-MIN]):
                basis.add(expr, (state >> bit) & 1)
    assert len(basis.b) == 15433

    tempered_weights = [temper(1 << bit) for bit in range(32)]
    future = []
    for position in range(1182, MAX+1):
        expressions_at = symbolic[position-MIN]
        known_mask = known_bits = 0
        for bit in range(16, 32):
            expr = 0
            for source_bit, weight in enumerate(tempered_weights):
                if weight & (1 << bit):
                    expr ^= expressions_at[source_bit]
            value = basis.predict(expr)
            if value is not None:
                known_mask |= 1 << (bit-16)
                known_bits |= value << (bit-16)
        future.append((known_mask, known_bits))

    def scan(observed):
        comparisons = matching = 0
        for i in range(6):
            control_run = observed[i:i+3]
            for j in range(len(future)-2):
                predictions = future[j:j+3]
                if sum(mask.bit_count() for mask, _ in predictions) < 32:
                    continue
                comparisons += 1
                if all(((sample ^ value) & mask) == 0
                       for sample, (mask, value) in zip(control_run, predictions)):
                    matching += 1
        return comparisons, matching

    native = scan(halfwords)
    swapped = scan([((x & 0xFF) << 8) | (x >> 8) for x in halfwords])
    assert native == (1302, 0), native
    assert swapped == (1302, 0), swapped

    # Synthetic direct-copy positive, injected at a genuinely constrained triple.
    first = next(i for i in range(len(future)-2)
                 if sum(mask.bit_count() for mask, _ in future[i:i+3]) >= 32)
    constructed = [value for _, value in future[first:first+3]]
    assert all(((v ^ expected) & mask) == 0
               for v, (mask, expected) in zip(constructed, future[first:first+3]))

    print("Source-only printer rank", 15305)
    print("Rank with previously established 12 early TRP2 controls", len(basis.b))
    print("K02 original selected halfwords", [f"{x:04X}" for x in halfwords])
    print("Future upper16 three-word alignments (>=32 independently fixed bits):")
    print("native", native, "byte_swapped", swapped)
    print("Synthetic predicted contiguous triple PASS")
    print("Selected printer row129 withheld; K04 bits recovered 0/128; K08 exact words 0")
    print("Conditional p955 already fails ordinary two-sampler producer metadata")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m agents.agent2.k04_k02_future_halfwords ORIGINAL.zip")
    main(Path(sys.argv[1]))
