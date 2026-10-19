"""Source-pinned TRP2 bad-CRC one/two-bit diagnosis; read-only, no slot hashes."""
from pathlib import Path
from itertools import combinations
import hashlib
import struct
import sys
import zipfile
import zlib

RAW_SHA256 = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"


def valid_crc(record):
    return zlib.crc32(record[:20]) == int.from_bytes(record[20:24], "little")


def flip(record, bit_positions):
    data = bytearray(record)
    for bit in bit_positions:
        data[bit // 8] ^= 1 << (bit % 8)
    return bytes(data)


def repairs(record, degree):
    for positions in combinations(range(24 * 8), degree):
        if valid_crc(flip(record, positions)):
            yield positions


def main(input_file):
    if input_file.suffix.lower() == ".zip":
        with zipfile.ZipFile(input_file) as archive:
            raw = archive.read("evidence/recorder/trip-recorder.raw")
    else:
        raw = input_file.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == RAW_SHA256
    assert raw[:8] == b"TRP2DUMP"
    assert struct.unpack_from("<HHI", raw, 8) == (2, 24, 88)
    assert len(raw) == 16 + 88 * 24
    bad = []
    for index in range(88):
        rec = raw[16 + 24 * index:16 + 24 * (index + 1)]
        if valid_crc(rec):
            continue
        seq = struct.unpack_from("<I", rec, 8)[0]
        recorded = int.from_bytes(rec[20:24], "little")
        mismatch = zlib.crc32(rec[:20]) ^ recorded
        one = list(repairs(rec, 1))
        two = list(repairs(rec, 2))
        bad.append((index, seq, mismatch, one, two))
        print(f"record={index} seq={seq} syndrome={mismatch:08X} 1bit={one} 2bit_count={len(two)}")
    assert len(bad) == 4
    assert [row[1] for row in bad] == [900, 901, 903, 902]
    assert all(row[2] == 0x100 and row[3] == [(168,)] and not row[4] for row in bad)

    # Positive control: a deliberately flipped original control bit has an
    # unambiguous data-bit syndrome and is not misclassified as a CRC fault.
    pristine = raw[16:40]
    assert valid_crc(pristine)
    damaged = flip(pristine, [99])
    assert list(repairs(damaged, 1)) == [(99,)]
    print("PASS: four checksum-bit syndromes and synthetic data-bit control")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("resources/evidence/recorder/trip-recorder.raw"))
