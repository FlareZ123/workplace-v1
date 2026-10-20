"""Read-only job-reuse seed test. No selected K04 payload or hash is used."""
import hashlib
import random
import re
import sys
from pathlib import Path

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
LIMIT = 32772


def seed_forms(raw):
    return (
        ("int-big", int.from_bytes(raw, "big")),
        ("int-little", int.from_bytes(raw, "little")),
        ("raw-bytes", raw),
        ("hex-ascii", raw.hex().upper()),
    )


def matches(seed, expected):
    rng = random.Random(seed)
    outputs = [rng.getrandbits(32) for _ in range(LIMIT)]
    little = tuple(int.from_bytes(expected[i:i+4], "little") for i in range(0, 16, 4))
    big = tuple(int.from_bytes(expected[i:i+4], "big") for i in range(0, 16, 4))
    found = []
    for i in range(LIMIT - 3):
        four = tuple(outputs[i:i+4])
        if four == little:
            found.append((i, "little"))
        if four == big:
            found.append((i, "big"))
    return found


def run(path):
    content = Path(path).read_bytes()
    assert hashlib.sha256(content).hexdigest() == SPOOL_SHA
    # Omit the disputed ESC-N attempt2 ACK before any parsing.
    lines = [line for line in content.splitlines()
             if b"2026-10-03T18:02:00Z JOB=PS-261003-0417" not in line]
    records = {}
    for line in lines:
        if b"JOB=PS-261003-0417" not in line and b"JOB=PS-261003-0420" not in line:
            continue
        f = dict(re.findall(rb"([A-Z]+)=([^ ]+)", line))
        key = (f[b"JOB"].decode(), f[b"ATTEMPT"].decode(), f[b"STATE"].decode())
        records[key] = bytes.fromhex(f[b"PAYLOAD"].decode())

    pairs = (
        ("0420 ACK1/ACK2",
         records["PS-261003-0420", "1", "ACK"],
         records["PS-261003-0420", "2", "ACK"]),
        ("0417 requested1/requested3",
         records["PS-261003-0417", "1", "REQUESTED"],
         records["PS-261003-0417", "3", "REQUESTED"]),
    )

    # Test the actual generator/word orientation path at a withheld offset.
    control = bytes(range(16))
    for name, seed in seed_forms(control):
        rng = random.Random(seed)
        words = [rng.getrandbits(32) for _ in range(41)]
        positive = b"".join(x.to_bytes(4, "little") for x in words[37:41])
        assert (37, "little") in matches(seed, positive), name
    print("Synthetic source-independent controls 4/4 PASS")

    for label, earlier, later in pairs:
        print("Pair:", label)
        for name, seed in seed_forms(earlier):
            found = matches(seed, later)
            print(" ", name, "matches=", len(found))
            assert found == []
        checks = (
            hashlib.sha256(earlier).digest()[:16],
            hashlib.sha256(earlier.hex().upper().encode()).digest()[:16],
            hashlib.md5(earlier).digest(),
        )
        assert all(x != later for x in checks)
        print(" ", "SHA256(raw), SHA256(hex), MD5(raw): 0/3")
    print("No witnessed job-replay model; actual K04 bits gained: 0")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) == 2 else
        Path(__file__).resolve().parents[2] / "resources/evidence/print/spool-reconstruction.log")
