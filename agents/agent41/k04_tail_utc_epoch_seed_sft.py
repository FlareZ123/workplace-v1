"""Read-only H-17 RECOVER-tail UTC-seed probe, with a positive producer control.

The disputed ESC-N attempt-2 is excluded before payload parsing.
This tests a narrow alternate printer epoch, not the K04 acceptance commitment.
"""
import argparse
import datetime as dt
import hashlib
import random
import re
import zipfile
from pathlib import Path

SPOOL_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
TARGET_ROW = "JOB=PS-261003-0417 ATTEMPT=2 STATE=ACK"
SPOOL_PATH = "evidence/print/spool-reconstruction.log"
START = int(dt.datetime(2026, 10, 3, 16, 0, tzinfo=dt.timezone.utc).timestamp())
STOP = int(dt.datetime(2026, 10, 3, 18, 3, tzinfo=dt.timezone.utc).timestamp())
MAX_OFFSET = 2000


def load_rows(path):
    if path.is_dir():
        spool = (path / SPOOL_PATH).read_bytes()
    else:
        with zipfile.ZipFile(path) as archive:
            spool = archive.read(SPOOL_PATH)
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA256
    rows = []
    for line in spool.decode("ascii").splitlines():
        if not line.startswith("2026-10-03T18:") or TARGET_ROW in line:
            continue
        match = re.fullmatch(
            r"(\S+) JOB=(\S+) ATTEMPT=(\d+) STATE=(\w+) CLASS=(\w+) "
            r"PAYLOAD=([0-9A-F]{32}) DEST=(\w+)",
            line,
        )
        assert match is not None, line
        rows.append((
            match.group(1),
            match.group(2),
            int(match.group(3)),
            bytes.fromhex(match.group(6)),
        ))
    assert len(rows) == 4
    assert rows[0][:3] == ("2026-10-03T18:01:00Z", "PS-261003-0417", 1)
    return rows


def word_patterns(payload):
    assert len(payload) == 16
    result = []
    for endian in ("little", "big"):
        forward = tuple(int.from_bytes(payload[i:i + 4], endian) for i in range(0, 16, 4))
        result.extend(((endian, "forward", forward), (endian, "reversed", forward[::-1])))
    return result


def matches(output, patterns, limit=MAX_OFFSET):
    hits = []
    for offset in range(limit + 1):
        for endian, direction, expected in patterns:
            if output[offset] == expected[0] and tuple(output[offset:offset + 4]) == expected:
                hits.append((offset, endian, direction))
    return hits


def run(path):
    rows = load_rows(path)
    print("Selected K04 ACK target withheld; test row:", rows[0][:3])
    patterns = word_patterns(rows[0][3])
    hits = []
    for seed in range(START, STOP + 1):
        rng = random.Random(seed)
        output = [rng.getrandbits(32) for _ in range(MAX_OFFSET + 4)]
        hits.extend((seed,) + hit for hit in matches(output, patterns))
    print("UTC-second seeds:", STOP - START + 1, "offsets:", MAX_OFFSET + 1)
    print("Full 128-bit hits across four orientation hypotheses:", len(hits), hits[:8])
    assert not hits

    fixture_seed = START + 63
    fixture_offset = 1473
    rng = random.Random(fixture_seed)
    output = [rng.getrandbits(32) for _ in range(MAX_OFFSET + 4)]
    words = output[fixture_offset:fixture_offset + 4]
    for endian in ("little", "big"):
        for direction in ("forward", "reversed"):
            ordered = words if direction == "forward" else words[::-1]
            payload = b"".join(w.to_bytes(4, endian) for w in ordered)
            assert (fixture_offset, endian, direction) in matches(output, word_patterns(payload))
    print("Four positive seeded-MT orientation and nonzero-prefix controls: PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    run(parser.parse_args().source)
