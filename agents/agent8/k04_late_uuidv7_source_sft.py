"""Original-source-only RFC UUIDv7 timestamp serialization falsifier.

From the workplace repository root: python agents/agent8/k04_late_uuidv7_source_sft.py
Reads only intact spool row at 18:01 UTC, never selected 18:02 K04 or acceptance.
"""
from datetime import datetime
from hashlib import sha256
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SPOOL = ROOT / "resources" / "evidence" / "print" / "spool-reconstruction.log"
EXPECTED_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def as_network(data: bytes, mixed: bool) -> bytes:
    """Convert Windows GUID mixed-endian bytes to RFC order when requested."""
    if mixed:
        return data[:4][::-1] + data[4:6][::-1] + data[6:8][::-1] + data[8:]
    return data


def inspect(data: bytes) -> tuple[int, int, int]:
    return int.from_bytes(data[:6], "big"), data[6] >> 4, data[8] >> 6


def main() -> None:
    raw = SPOOL.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_SHA
    line = next(line for line in raw.decode("utf-8").splitlines()
                if line.startswith("2026-10-03T18:01:00Z "))
    match = re.search(r"PAYLOAD=([0-9A-F]{32})", line)
    assert match is not None
    source = bytes.fromhex(match.group(1))
    expected = int(datetime.fromisoformat("2026-10-03T18:01:00+00:00").timestamp() * 1000)

    # True positive: RFC v7 first six bytes are Unix milliseconds,
    # high nibble of byte6 is 7; top two bits of byte8 are 10.
    fixture = bytearray(16)
    fixture[:6] = expected.to_bytes(6, "big")
    fixture[6] = 0x70
    fixture[8] = 0x80
    assert inspect(as_network(bytes(fixture), False)) == (expected, 7, 2)
    mixed_fixture = (fixture[:4][::-1] + fixture[4:6][::-1] +
                     fixture[6:8][::-1] + fixture[8:])
    assert inspect(as_network(mixed_fixture, True)) == (expected, 7, 2)
    print("SYNTHETIC: both RFC v7 encodings PASS")

    fits = []
    for label, mixed in (("RFC", False), ("Windows GUID mixed", True)):
        stamp, version, variant = inspect(as_network(source, mixed))
        fits.append((stamp, version, variant) == (expected, 7, 2))
        print(f"{label}: expected_time={expected.to_bytes(6, 'big').hex().upper()} "
              f"observed_time={stamp.to_bytes(6, 'big').hex().upper()} "
              f"version={version}, variant={variant:02b}, match={fits[-1]}")
    assert not any(fits)
    print("SOURCE-ONLY STOP: intact 18:01 late row fails both exact UUIDv7 views.")
    print("No selected K04 payload, mask, nonce, acceptance, or K08 candidate parsed.")


if __name__ == "__main__":
    main()
