"""SFT: source-only MT donor test for signed WN14 controls and seal serials.

Reads the original repository resources and no acceptance commitments. The disputed
printer row129 is always withheld. The source-defined signed WN14 word order is
A,B,C,D; seal serials are retained in their original JSONL order.
"""
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib

BASE = Path(__file__).resolve().parents[2] / "resources" / "evidence"
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
SEAL_SHA = "c00944558636fbcc7e91b81e8e838ffd13fcd5a30d121b41951888766a8a0e32"


def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9D2C5680
    x ^= (x << 15) & 0xEFC60000
    x ^= x >> 18
    return x & 0xFFFFFFFF


def untemper(y):
    original = y
    x = y
    for _ in range(6):
        x = y ^ (x >> 18)
    y = x
    for _ in range(6):
        x = y ^ ((x << 15) & 0xEFC60000)
    y = x
    for _ in range(6):
        x = y ^ ((x << 7) & 0x9D2C5680)
    y = x
    for _ in range(6):
        x = y ^ (x >> 11)
    assert temper(x) == original
    return x


def inverse_successor_low31(middle, end):
    d = middle ^ end
    parity = d >> 31
    d ^= 0x9908B0DF if parity else 0
    return ((d << 1) | parity) & 0x7FFFFFFF


def source_bytes(path, sha):
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == sha
    return data


def main():
    spool = source_bytes(BASE / "print/spool-reconstruction.log", SPOOL_SHA)
    seals = source_bytes(BASE / "maintenance/seal-receipts.jsonl", SEAL_SHA)
    rows = {}
    payload_lines = [line for line in spool.decode().splitlines() if "PAYLOAD=" in line]
    assert len(payload_lines) == 133
    for r, line in enumerate(payload_lines):
        if r == 129:
            continue
        payload = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", line).group(1))
        rows[r] = tuple(untemper(v) for v in struct.unpack("<4I", payload))
    assert len(rows) == 132

    ink = {}
    for filename in ("03.eml", "06.eml"):
        mail = (BASE / "mail" / filename).read_text()
        for group, value in re.findall(r"WN-14 / group ([ABCD]) / ([0-9A-F]{8})", mail):
            assert group not in ink
            ink[group] = value
    assert tuple(sorted(ink)) == ("A", "B", "C", "D")
    assert "WN-14 was signed" in (BASE / "mail/14.eml").read_text()
    serials = [json.loads(line)["serial"][3:] for line in seals.decode().splitlines()]
    assert len(serials) == 44 and len(set(serials)) == 44

    # Authentic independent positive control: CRC-valid TRP2 record26 bridges
    # intact row7 word3 / row38 word0 in the same 31-bit inverse relationship.
    dump = (BASE / "recorder/trip-recorder.raw").read_bytes()
    record = dump[16 + 26 * 24:16 + 27 * 24]
    assert zlib.crc32(record[:20]) == int.from_bytes(record[20:24], "little")
    control = untemper(int.from_bytes(record[12:16], "little")) & 0x7FFFFFFF
    assert inverse_successor_low31(rows[7][3], rows[38][0]) == control
    print("TRP2 independently observed bridge: PASS")

    fields = [("WN14", index, raw) for index, raw in enumerate(ink[k] for k in "ABCD")]
    fields += [("SEAL", index, raw) for index, raw in enumerate(serials)]
    words = [
        (label, index, endian, untemper(int.from_bytes(bytes.fromhex(raw), endian)))
        for label, index, raw in fields
        for endian in ("little", "big")
    ]
    lookup = {}
    for label, index, endian, value in words:
        lookup.setdefault(value & 0x7FFFFFFF, []).append((label, index, endian))

    full = set(word for row in rows.values() for word in row)
    direct = [(label, index, endian) for label, index, endian, value in words if value in full]
    bridge = []
    for r1 in rows:
        for r2 in rows:
            if r2 <= r1:
                continue
            for i, left in enumerate(rows[r1]):
                for j, right in enumerate(rows[r2]):
                    for match in lookup.get(inverse_successor_low31(left, right), ()):
                        bridge.append((r1, i, r2, j, *match))

    print("Source fields:", len(fields), "orientations:", len(words))
    print("Printer ordered pair/word hypotheses:", len(rows) * (len(rows) - 1) // 2 * 16)
    print("Direct full-word matches:", direct)
    print("Inverse low31 matches:", bridge)
    target = {12, 43, 66, 96, 128, 13, 44, 67, 97, 130, 131}
    print("Target-adjacent group matches:",
          [item for item in bridge if item[0] in target or item[2] in target])
    assert not direct and not bridge


if __name__ == "__main__":
    main()
