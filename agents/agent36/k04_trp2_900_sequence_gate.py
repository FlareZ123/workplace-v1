"""K04 TRP2 900-series producer-order falsifier, original-source-only."""
import hashlib
import random
import re
import struct
import sys
import zipfile
from pathlib import Path

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
REC_SHA = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"


def undo_right(value, shift):
    state = value
    for _ in range(6):
        state = value ^ (state >> shift)
    return state & 0xFFFFFFFF


def undo_left(value, shift, mask):
    state = value
    for _ in range(6):
        state = value ^ ((state << shift) & mask)
    return state & 0xFFFFFFFF


def untemper(value):
    return undo_right(
        undo_left(
            undo_left(undo_right(value, 18), 15, 0xEFC60000),
            7, 0x9D2C5680,
        ), 11,
    )


def predecessor_low31(middle, end):
    diff = middle ^ end
    unmixed = diff ^ (0x9908B0DF if diff >> 31 else 0)
    return (((unmixed << 1) | (diff >> 31)) & 0x7FFFFFFF)


def read_source(filename):
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("resources")
    if source.is_file():
        with zipfile.ZipFile(source) as case:
            return case.read(filename)
    return (source / filename).read_bytes()


def main():
    spool = read_source("evidence/print/spool-reconstruction.log")
    raw = read_source("evidence/recorder/trip-recorder.raw")
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    assert hashlib.sha256(raw).hexdigest() == REC_SHA

    generator = random.Random(0xC0FFEE12345)
    states = [untemper(generator.getrandbits(32)) for _ in range(640)]
    for t in range(4):
        assert predecessor_low31(states[t + 397], states[t + 624]) == states[t + 1] & 0x7FFFFFFF
    print("Actual-CPython MT synthetic controls: 4/4 PASS")

    rows = [
        struct.unpack("<4I", bytes.fromhex(s.decode("ascii")))
        for s in re.findall(rb"PAYLOAD=([0-9A-F]{32})", spool)
    ]
    assert len(rows) == 133
    expected = [
        predecessor_low31(untemper(a), untemper(b))
        for a, b in zip(rows[10], rows[41])
    ]
    assert expected == [0x348ADB23, 0x324EF3E1, 0x353CCDFC, 0x16DF5138]

    controls = {}
    count = struct.unpack_from("<I", raw, 12)[0]
    for index in range(count):
        record = raw[16 + 24 * index:16 + 24 * (index + 1)]
        node, event, seq = struct.unpack_from("<H B x I", record, 4)
        if node == 49 and event == 82 and 900 <= seq <= 903:
            payload = struct.unpack_from("<I", record, 12)[0]
            controls[seq] = (index, untemper(payload) & 0x7FFFFFFF)
    assert sorted(controls) == [900, 901, 902, 903]
    assert controls[903][1] == expected[2]

    for seq, offset in ((901, 0), (902, 1), (903, 2)):
        observed = controls[seq][1]
        predicted = expected[offset]
        print(f"seq{seq}: observed={observed:08X}, predicted={predicted:08X}, match={observed == predicted}")
    assert controls[901][1] != expected[0]
    assert controls[902][1] != expected[1]
    print("Strict consecutive 901..903 source-index order: FALSIFIED")
    print("New verified selected K04 coupon bits: 0/128")


if __name__ == "__main__":
    main()
