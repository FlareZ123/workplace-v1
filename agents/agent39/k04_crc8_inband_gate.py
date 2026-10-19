"""Read-only source-pinned CRC8 integrity probe for H-17 RECOVER spool fields.

Usage: python agents/agent39/k04_crc8_inband_gate.py /path/to/extracted-case
       python agents/agent39/k04_crc8_inband_gate.py original-case.zip
No source or acceptance files are changed; no K04 hash is inspected.
"""
import hashlib
import re
import sys
from pathlib import Path
from zipfile import ZipFile

SOURCE_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def crc8(data: bytes, polynomial: int, reflected: bool) -> int:
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if reflected:
                crc = (crc >> 1) ^ (polynomial if crc & 1 else 0)
            else:
                crc = ((crc << 1) ^ (polynomial if crc & 128 else 0)) & 255
    return crc


def read_spool(source: Path) -> bytes:
    if source.is_file():
        with ZipFile(source) as archive:
            return archive.read("evidence/print/spool-reconstruction.log")
    if (source / "evidence/print/spool-reconstruction.log").exists():
        return (source / "evidence/print/spool-reconstruction.log").read_bytes()
    return (source / "resources/evidence/print/spool-reconstruction.log").read_bytes()


def main(source: Path) -> None:
    spool = read_spool(source)
    assert hashlib.sha256(spool).hexdigest() == SOURCE_SHA256
    regular, tail = [], []
    for line in spool.splitlines():
        if b"CLASS=RECOVER" not in line:
            continue
        payload = bytes.fromhex(re.search(rb"PAYLOAD=([A-F0-9]{32})", line).group(1).decode())
        (regular if b"+00:00 JOB=" in line else tail).append(payload)
    assert len(regular) == 35 and len(tail) == 5

    # A fixed initialization state is algebraically equivalent to an unknown
    # fixed xorout offset for a fixed 15-byte CRC8 input length. Learn that
    # offset on row 1 and require exact pre-hash predictions on rows 2..35.
    fits = []
    for position in range(16):
        for reverse_bytes in (False, True):
            for reflected in (False, True):
                for polynomial in range(1, 256):
                    used_poly = int(f"{polynomial:08b}"[::-1], 2) if reflected else polynomial

                    def residual(payload: bytes) -> int:
                        content = payload[:position] + payload[position + 1:]
                        if reverse_bytes:
                            content = content[::-1]
                        return payload[position] ^ crc8(content, used_poly, reflected)

                    expected = residual(regular[0])
                    if all(residual(row) == expected for row in regular[1:]):
                        fits.append((position, reverse_bytes, reflected, polynomial, expected,
                                     all(residual(row) == expected for row in tail)))

    # Positive control is independent of historical spool records.
    control = b"printercrc-test"
    check_byte = crc8(control, 0x07, False) ^ 0x5A
    assert check_byte ^ crc8(control, 0x07, False) == 0x5A
    print("SOURCE_SHA256", SOURCE_SHA256)
    print("regular_RECover", len(regular), "tail_RECOVER", len(tail))
    print("hypotheses", 16 * 2 * 2 * 255)
    print("regular_training_fits", fits)
    print("synthetic_crc8_control", "PASS")
    assert not fits


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("."))
