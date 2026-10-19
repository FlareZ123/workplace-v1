"""Check novel hidden K04/K08 carrier: unused bits of ZIP DEFLATE final bytes.

Usage: python agents/agent40/k08_zip_deflate_pad.py original-case.zip
Original exported 43-member ZIP remains read-only and SHA256-pinned.
This checks compressed-source physical bits, distinct from decoded member scans.
Python 3 standard library only, works on Windows 11.
"""
import hashlib
import io
import struct
import sys
import zipfile
import zlib
from pathlib import Path

CASE_SHA = "a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec"


def compressed_entry(archive_bytes, info):
    offset = info.header_offset
    assert archive_bytes[offset:offset + 4] == b"PK\x03\x04"
    name_bytes, extra_bytes = struct.unpack_from("<HH", archive_bytes, offset + 26)
    start = offset + 30 + name_bytes + extra_bytes
    assert info.compress_type == 8 and info.flag_bits == 0
    result = archive_bytes[start:start + info.compress_size]
    assert len(result) == info.compress_size and result
    return start, result


def bit_slack(compressed, original_plaintext):
    """Count high final-byte bits safely mutable without decoded-byte changes.

    For each contiguous high-bit set, flip *every* such bit, and compare the
    exact raw-DEFLATE expansion with independent original ZIP plaintext.
    """
    assert zlib.decompress(compressed, -15) == original_plaintext
    unused = 0
    for count in range(1, 8):
        edited = bytearray(compressed)
        edited[-1] ^= ((1 << count) - 1) << (8 - count)
        try:
            identical = zlib.decompress(edited, -15) == original_plaintext
        except zlib.error:
            identical = False
        if not identical:
            break
        unused = count
    bits = compressed[-1] >> (8 - unused) if unused else 0
    return unused, bits


def audit(archive_bytes):
    output = []
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        assert len(archive.infolist()) == 43
        assert archive.testzip() is None
        for entry in archive.infolist():
            _, compressed = compressed_entry(archive_bytes, entry)
            plain = archive.read(entry.filename)
            unused, bits = bit_slack(compressed, plain)
            output.append((entry.filename, unused, bits))
    return output


def main(path):
    original = path.read_bytes()
    assert hashlib.sha256(original).hexdigest() == CASE_SHA
    source = audit(original)
    assert len(source) == 43
    assert sum(n for _, n, _ in source) == 151
    assert all(value == 0 for _, _, value in source)

    # A single planted bit in an ignored final-byte position is detectable
    # and leaves all 43 ZIP-decompressed records and CRC32 values unchanged.
    with zipfile.ZipFile(io.BytesIO(original)) as archive:
        entry = archive.getinfo("acceptance.json")
        start, compressed = compressed_entry(original, entry)
    assert bit_slack(compressed, zlib.decompress(compressed, -15)) == (7, 0)
    modified = bytearray(original)
    modified[start + entry.compress_size - 1] ^= 0x80
    planted = audit(bytes(modified))
    assert sum(n for _, n, _ in planted) == 151
    assert [(p, n) for p, n, _ in source] == [(p, n) for p, n, _ in planted]
    assert [(p, v) for p, _, v in planted if v != 0] == [
        ("acceptance.json", 0b1000000)
    ]

    print("source_files", len(source))
    print("DEFLATE_unused_bit_capacity", sum(n for _, n, _ in source))
    print("nonzero_unused_fields", sum(value != 0 for _, _, value in source))
    print("synthetic_planted_padding_bit", "PASS")
    print("selected_K04_ACK_or_K08_phrase_read", False)
    print("original_REC8_missing_K04_K08_UNCHANGED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python agents/agent40/k08_zip_deflate_pad.py original-case.zip")
    main(Path(sys.argv[1]))
