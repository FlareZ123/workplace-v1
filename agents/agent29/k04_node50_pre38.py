"""Recover two conditional hidden MT19937 output words before printer row38.

Read-only SFT: python agents/agent29/k04_node50_pre38.py case-export.zip
Selected row129, route/mask, K08 and acceptance commitments are not read.
"""
import hashlib
import random
import re
import struct
import sys
import zipfile
import zlib

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
REC_SHA = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"


def undo_right(value, shift):
    result = value
    for _ in range(6):
        result = value ^ (result >> shift)
    return result & 0xFFFFFFFF


def undo_left(value, shift, mask):
    result = value
    for _ in range(6):
        result = value ^ ((result << shift) & mask)
    return result & 0xFFFFFFFF


def untemper(value):
    return undo_right(undo_left(undo_left(undo_right(value, 18), 15, 0xEFC60000),
                                7, 0x9D2C5680), 11)


def temper(value):
    value ^= value >> 11
    value ^= (value << 7) & 0x9D2C5680
    value ^= (value << 15) & 0xEFC60000
    return (value ^ (value >> 18)) & 0xFFFFFFFF


def twist(left, right):
    mixed = (left & 0x80000000) | (right & 0x7FFFFFFF)
    return (mixed >> 1) ^ (0x9908B0DF if mixed & 1 else 0)


def main(path):
    with zipfile.ZipFile(path) as source:
        spool = source.read("evidence/print/spool-reconstruction.log")
        recorder = source.read("evidence/recorder/trip-recorder.raw")
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    assert hashlib.sha256(recorder).hexdigest() == REC_SHA
    lines = [line for line in spool.decode().splitlines()
             if line.startswith("2026-")]
    assert len(lines) == 133
    assert "DEST=desk" in lines[37] and "CLASS=RECOVER" in lines[38]

    def state_row(number):
        payload = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})",
                                         lines[number]).group(1))
        return [untemper(x) for x in struct.unpack("<4I", payload)]

    row7 = state_row(7)
    row38 = state_row(38)
    controls = {}
    for i in range(88):
        raw = recorder[16 + 24*i:16 + 24*(i + 1)]
        _, node, _, _, seq, opaque, _, crc = struct.unpack("<IHBBI4sII", raw)
        if node == 50:
            assert zlib.crc32(raw[:20]) == crc and seq not in controls
            controls[seq] = untemper(int.from_bytes(opaque, "little"))
    assert set(controls) == set(range(72))

    # Independent Python-generator positive control for the exact phase arithmetic.
    rng = random.Random(123456789)
    words = [untemper(rng.getrandbits(32)) for _ in range(1300)]
    for j in range(4):
        t = 500 - 397 + j
        assert words[t + 624] == words[t + 397] ^ twist(words[t], words[t + 1])
    print("synthetic_recurrence", "PASS")

    prediction = {}
    for j in range(4):
        prediction[j - 3] = row7[j] ^ twist(controls[66 + j], controls[67 + j])
    assert prediction[0] == row38[0]
    assert temper(prediction[-1]) >> 29 == 2
    for position in (-3, -2, -1, 0):
        value = prediction[position]
        coded = temper(value)
        print("row38_rel", position, "untempered", f"{value:08X}",
              "tempered", f"{coded:08X}", "CLASS3", coded >> 29,
              "DEST2", coded >> 30)
    assert prediction[-3] == 0x3586854C
    assert prediction[-2] == 0x7BEE882D
    assert temper(prediction[-2]) >> 29 == 1
    assert temper(prediction[-2]) >> 30 == 0
    print("conditional_no_extra_draw_two_sampler", "FALSIFIED_AT_ROW37_TO_38")
    print("selected_row129_and_original_commitments_unread", True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_node50_pre38.py original-case.zip")
    main(sys.argv[1])
