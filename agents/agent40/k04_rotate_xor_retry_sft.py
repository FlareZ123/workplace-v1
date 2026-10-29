"""SFT: source-only K04 rotate/XOR retry hypothesis, no selected-row decoding.

Run with a repository checkout (resources/ at root) or a local original ZIP:
    python k04_rotate_xor_retry_sft.py /path/to/c-energy-group-documents2026.zip

This script does not open acceptance commitments, K04 mask, or verifier.
"""
from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path

SOURCE_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MODULO = (1 << 128) - 1
TARGET_TIME = "2026-10-03T18:02:00Z"
CONTROL_TIMES = (
    "2026-10-03T17:00:00+00:00",
    "2026-10-03T18:25:00Z",
    "2026-10-03T18:01:00Z",
    "2026-10-03T18:03:00Z",
)


def read_spool(path: Path) -> bytes:
    if path.is_file():
        with zipfile.ZipFile(path) as archive:
            return archive.read("evidence/print/spool-reconstruction.log")
    return (path / "evidence" / "print" / "spool-reconstruction.log").read_bytes()


def rotate_left(value: int, count: int) -> int:
    return ((value << count) | (value >> (128 - count))) & MODULO


def transition(value: int, count: int, shift_key: int) -> int:
    return rotate_left(value, count) ^ shift_key


def parse_controls(spool_bytes: bytes) -> dict[str, int]:
    retained: dict[str, int] = {}
    for line in spool_bytes.decode("utf-8").splitlines():
        # Physical exclusion before parsing metadata or PAYLOAD of disputed target.
        if line.startswith(TARGET_TIME + " "):
            continue
        timestamp, *fields = line.split()
        if timestamp not in CONTROL_TIMES:
            continue
        attrs = dict(field.split("=", 1) for field in fields)
        if timestamp in CONTROL_TIMES[:2]:
            assert attrs["JOB"] == "PS-261003-0420"
        else:
            assert attrs["JOB"] == "PS-261003-0417"
        assert attrs["PAYLOAD"].isalnum() and len(attrs["PAYLOAD"]) == 32
        assert timestamp not in retained
        retained[timestamp] = int(attrs["PAYLOAD"], 16)
    assert set(retained) == set(CONTROL_TIMES), sorted(retained)
    return retained


def synthetic_check() -> None:
    initial = int("0714212835424956637077849198A5B2", 16)
    shift = int("5182A3C4D5E6F708192A3B4C5D6E7F80", 16)
    count = 55
    next_one = transition(initial, count, shift)
    next_two = transition(next_one, count, shift)
    inferred_shift = rotate_left(initial, count) ^ next_one
    assert inferred_shift == shift
    assert transition(transition(initial, count, inferred_shift), count, inferred_shift) == next_two
    print("Synthetic two-step positive: PASS")


def main(source: Path) -> None:
    spool = read_spool(source)
    actual_hash = hashlib.sha256(spool).hexdigest()
    assert actual_hash == SOURCE_SHA256, actual_hash
    print("Pinned original printer log: PASS")
    original = parse_controls(spool)
    earlier_0420, later_0420, earlier_0417, later_0417 = (original[t] for t in CONTROL_TIMES)
    print("Intact controls parsed: 4; disputed 18:02 row withheld before parsing")
    synthetic_check()

    best: list[tuple[int, int]] = []
    matches: list[int] = []
    for count in range(1, 128):
        shift = rotate_left(earlier_0420, count) ^ later_0420
        predicted = transition(transition(earlier_0417, count, shift), count, shift)
        differing_bits = (predicted ^ later_0417).bit_count()
        best.append((differing_bits, count))
        if predicted == later_0417:
            matches.append(count)
    print(f"Frozen 127 rotate/XOR cases: exact holdout matches {len(matches)}/127")
    print(f"Best residual Hamming distances (bits,rotation): {sorted(best)[:5]}")
    assert len(matches) == 0, "Source control matched; requires historical producer validation"
    assert sorted(best)[0] == (46, 55), sorted(best)[:5]
    print("Original intact holdout gate: FAIL for all 127 model candidates")
    print("K04 target bits authenticated: 0/128; no acceptance candidate generated")


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Provide a local ZIP or resources directory"
    main(Path(sys.argv[1]))
