"""Falsify the 72-consecutive-node50-control hypothesis with original printer words.

Run: python agents/agent38/k04_node50_sequence_contradiction.py original-case.zip
Source row129, original REC8 routing, nonce, commitments, verifier withheld.
"""
import hashlib
import random
import re
import struct
import sys
import zlib
from zipfile import ZipFile

ALL = 0xFFFFFFFF
A = 0x9908B0DF
SPOOL = "evidence/print/spool-reconstruction.log"
REC = "evidence/recorder/trip-recorder.raw"


def ur(y, shift):
    x = y
    for _ in range(6):
        x = y ^ (x >> shift)
    return x & ALL


def ul(y, shift, mask):
    x = y
    for _ in range(6):
        x = y ^ ((x << shift) & mask)
    return x & ALL


def untemper(y):
    return ur(ul(ul(ur(y, 18), 15, 0xEFC60000),
                 7, 0x9D2C5680), 11)


def twist(left, right):
    y = (left & 0x80000000) | (right & 0x7FFFFFFF)
    return ((y >> 1) ^ (A if y & 1 else 0)) & ALL


def untwist(delta):
    bit = delta >> 31
    return (((delta ^ (A if bit else 0)) << 1) | bit) & ALL


def implied_midwords(row91, row121):
    mixed = [untwist(a ^ b) for a, b in zip(row91[:3], row121[:3])]
    return [(mixed[j] & 0x7FFFFFFF) | (mixed[j+1] & 0x80000000)
            for j in range(2)]


def node50_predictions(row7, controls):
    return [row7[j] ^ twist(controls[66+j], controls[67+j])
            for j in range(4)]


def synthetic_positive_control():
    rng = random.Random(0xE5E4A321B9)
    source = [untemper(rng.getrandbits(32)) for _ in range(1600)]
    base = 700
    row7 = source[base:base+4]
    row38 = source[base+230:base+234]
    row91 = source[base+624:base+628]
    row121 = source[base+851:base+855]
    controls = {j: source[base-463+j] for j in range(72)}
    assert row121[3] == row91[3] ^ twist(row38[0], row38[1])
    assert ((untwist(row7[3] ^ row38[0]) & 0x7FFFFFFF)
            == (controls[70] & 0x7FFFFFFF))
    assert implied_midwords(row91, row121) == source[base+228:base+230]
    assert node50_predictions(row7, controls) == source[base+227:base+231]
    print("SYNTHETIC_TRUE_CONSECUTIVE_MT_PASS", True)


def main(source):
    synthetic_positive_control()
    with ZipFile(source) as archive:
        spool = archive.read(SPOOL)
        recorder = archive.read(REC)
    assert hashlib.sha256(spool).hexdigest() == (
        "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
    )
    assert hashlib.sha256(recorder).hexdigest() == (
        "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
    )
    lines = [x for x in spool.decode().splitlines() if x.startswith("2026-")]
    assert len(lines) == 133

    def printer(row):
        assert row != 129
        payload = re.search(r"PAYLOAD=([0-9A-F]{32})", lines[row]).group(1)
        return [untemper(w) for w in
                struct.unpack("<4I", bytes.fromhex(payload))]

    row7, row38, row91, row121 = map(printer, (7, 38, 91, 121))
    controls = {}
    for i in range(88):
        data = recorder[16+i*24:16+(i+1)*24]
        timestamp, node, event, latch, seq, word, aux, crc = (
            struct.unpack("<IHBBI4sII", data)
        )
        if node == 50:
            assert zlib.crc32(data[:20]) == crc
            assert seq not in controls
            controls[seq] = untemper(int.from_bytes(word, "little"))
    assert set(controls) == set(range(72))

    # Two established MT correspondences. The first is a full 32-bit
    # original printer recurrence witness, implying s91-s38=394 and
    # s121-s38=621. The second is the earlier node50 seq70 low31 bridge
    # conditionally placing s38-s7=230. Neither assumes seq67/68 adjacency.
    assert row121[3] == row91[3] ^ twist(row38[0], row38[1])
    assert ((untwist(row7[3] ^ row38[0]) & 0x7FFFFFFF)
            == (controls[70] & 0x7FFFFFFF))

    # Hence s91-s7=624 and s121-s7=851. Inverse MT twist applied
    # to printer row91/121 pairs yields full X[s7+228] and X[s7+229],
    # independently of all node50 controls except the seq70 alignment.
    authentic = implied_midwords(row91, row121)
    # A 72-word contiguous node50 seq-order model places seq[j] at
    # X[s7-463+j]. It therefore predicts X[s7+227..230] using the
    # four intact original row7 words and node50 seq66..70.
    sequential = node50_predictions(row7, controls)
    assert sequential[3] == row38[0]
    assert authentic == [0xE18DCD4D, 0x820D840E]
    assert sequential[1:3] == [0x7BEE882D, 0xF1522284]

    for position, known, predicted in zip((228, 229),
                                           authentic, sequential[1:3]):
        delta = known ^ predicted
        print("MT_position", position,
              "printer_derived", f"{known:08X}",
              "node50_sequential_model", f"{predicted:08X}",
              "contradictory_bits", delta.bit_count(),
              "xor", f"{delta:08X}")
    mismatches = sum((a ^ b).bit_count()
                     for a, b in zip(authentic, sequential[1:3]))
    assert mismatches == 31
    print("SOURCE_CONTRADICTS_72_CONSECUTIVE_NODE50_MODEL", True)
    print("SELECTED_PRINTER_ROW129_WITHHELD", True)
    print("K04_K08_UNRESOLVED", True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python k04_node50_sequence_contradiction.py original-case.zip"
        )
    main(sys.argv[1])
