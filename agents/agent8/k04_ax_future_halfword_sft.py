"""K04 forward-state future-donor fingerprint: AX checkpoint halfwords.

Run: python agents/agent8/k04_ax_future_halfword_sft.py original-case.zip
Source-only: does not inspect the disputed K04 spool coupon, any acceptance
hash, route mask, K08 nonce, or the verifier.

The four XOR constraints come from Agent29's original-source, row129-withheld
index955 GF(2) model; they are conditional on that producer chronology.
"""
import hashlib
import json
import re
import struct
import sys
import zlib
from itertools import combinations
from pathlib import Path
from zipfile import ZipFile

SOURCE_DIGESTS = {
    "evidence/transfers/transfer-audit.jsonl":
        "32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf",
    "evidence/recorder/trip-recorder.raw":
        "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba",
    "evidence/procedures/RC-17-scans.txt":
        "a4b649fdbb6909115fb9505133012b5c1dda42141aafc1c6ec756199ddf1fc6d",
}
# (future-state pair, known XOR mask, known XOR value).
RELATIONS = (
    ("1412/1866", 0xFFFFFFFF, 0xBD2761F8),
    ("1185/1412", 0xBFFFFFFF, 0x359EC0C7),
    ("1185/1866", 0xBFFFFFFF, 0x88B9A13F),
    ("1411/1865", 0x9FFFFFFF, 0x0CDE27B9),
)


def temper(word):
    word ^= word >> 11
    word ^= (word << 7) & 0x9D2C5680
    word ^= (word << 15) & 0xEFC60000
    word ^= word >> 18
    return word & 0xFFFFFFFF


def untemper(word):
    def right(value, shift):
        current = value
        for _ in range(5):
            current = value ^ (current >> shift)
        return current & 0xFFFFFFFF

    def left(value, shift, mask):
        current = value
        for _ in range(5):
            current = value ^ ((current << shift) & mask)
        return current & 0xFFFFFFFF

    return right(left(left(right(word, 18), 15, 0xEFC60000),
                      7, 0x9D2C5680), 11)


def possible_high16(mask, known_delta, full_state):
    """All legal high 16 bits after tempering an XOR-related MT word."""
    absent = [1 << bit for bit in range(32) if not mask & (1 << bit)]
    base = known_delta & mask
    return {
        temper(full_state ^ base ^
               sum(bit for position, bit in enumerate(absent)
                   if selection & (1 << position))) >> 16
        for selection in range(1 << len(absent))
    }


def original_fields(archive):
    data = {name: archive.read(name) for name in SOURCE_DIGESTS}
    for name, digest in SOURCE_DIGESTS.items():
        assert hashlib.sha256(data[name]).hexdigest() == digest, name

    recorder = data["evidence/recorder/trip-recorder.raw"]
    assert recorder[:8] == b"TRP2DUMP" and len(recorder) == 16 + 88 * 24
    controls = []
    for i in range(88):
        row = recorder[16 + 24*i:16 + 24*(i+1)]
        crc_good = zlib.crc32(row[:20]) == struct.unpack_from("<I", row, 20)[0]
        controls.append((f"TRP2 row{i} CRC={crc_good}", row[12:16]))
    for j, section in enumerate(
            data["evidence/procedures/RC-17-scans.txt"].decode().split("\f")):
        match = re.search(r"Footer control strip: ([0-9A-F]{8})", section)
        if match:
            controls.append((f"RC17 section{j}", bytes.fromhex(match.group(1))))
    assert len(controls) == 100

    rows = [json.loads(line) for line in
            data["evidence/transfers/transfer-audit.jsonl"].decode().splitlines()]
    checkpoint_fields = [
        (f"{r['transfer']}/s{r['seq']}/a{r['attempt']}", bytes.fromhex(r["checkpoint"]))
        for r in rows if r["kind"] == "CHUNK"
    ]
    assert len(checkpoint_fields) == 64
    return controls, checkpoint_fields


def test_mask_projection():
    # Independently chosen states with BOTH completions of each unknown bit.
    for _, mask, delta in RELATIONS:
        for state in (0, 0x12345678, 0xDEADBEEF, 0xFFFFFFFF):
            absent = [1 << bit for bit in range(32) if not mask & (1 << bit)]
            expected = possible_high16(mask, delta, state)
            for choice in range(1 << len(absent)):
                completion = sum(bit for index, bit in enumerate(absent)
                                 if choice & (1 << index))
                assert temper(state ^ (delta & mask) ^ completion) >> 16 in expected
    assert temper(untemper(0xDEADBEEF)) == 0xDEADBEEF


def run(path):
    test_mask_projection()
    with ZipFile(path) as archive:
        controls, ax = original_fields(archive)
    full = [(label, endian, untemper(int.from_bytes(raw, endian)))
            for label, raw in controls for endian in ("little", "big")]
    half = [(label, endian, int.from_bytes(raw, endian))
            for label, raw in ax for endian in ("little", "big")]
    print("original full32 fields", len(controls), "orientations", len(full))
    print("original AX half16 fields", len(ax), "orientations", len(half))
    for pair, mask, delta in RELATIONS:
        cross = [(src, ori, dest, axori)
                 for src, ori, state in full
                 for dest, axori, value in half
                 if value in possible_high16(mask, delta, state)]
        ax_ax = {}
        for endian in ("little", "big"):
            oriented = [(label, int.from_bytes(raw, endian)) for label, raw in ax]
            options = possible_high16(mask, delta, 0)
            ax_ax[endian] = [
                (a[0], b[0]) for a, b in combinations(oriented, 2)
                if (a[1] ^ b[1]) in options
            ]
        print(pair, f"masked_state_XOR={delta:08X}", f"mask={mask:08X}",
              "cross_full32_AX16", len(cross),
              "AX_AX_little", len(ax_ax["little"]),
              "AX_AX_big", len(ax_ax["big"]))
        for matched in cross:
            print("  source_paired_collision", *matched)
        assert not ax_ax["little"] and not ax_ax["big"]
        expected_counts = {"1412/1866": 0, "1185/1412": 1,
                           "1185/1866": 0, "1411/1865": 2}
        assert len(cross) == expected_counts[pair]
        if pair == "1185/1412":
            assert cross == [("TRP2 row17 CRC=True", "little",
                              "AX-7778/s4/a1", "little")]
    print("ALL_AX_AX_PAIRS_NEGATIVE", True)
    print("historically_indexed_target_donors", 0, "recovered_K04_bits", 0)


if __name__ == "__main__":
    run(Path(sys.argv[1]))
