"""Read-only H-17 named-insured CPython seed hypothesis, source-only controls.

Prerequisite: newly unlocked company name on BX25/08 page 1 (Agent 45).
Usage: python agents/agent45/k04_noyes_name_seed_sft.py ORIGINAL_SPOOL_LOG

This is a bounded, unsupported seed family, not proof of physical printer
generation. Withhold disputed spool row129 and all K04/K08 acceptance data.
"""
import hashlib
import random
import re
import struct
import sys
import zlib
from pathlib import Path

SPOOL_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
COUNT = 65536
ORIGINAL_NAMES = (
    "Noyes Energy Group", "NOYES ENERGY GROUP", "noyes energy group",
    "Noyes", "NOYES", "noyes",
    "Noyes-Energy-Group", "noyes-energy-group", "NoyesEnergyGroup",
    "noyes-energy-group.pages.dev", "https://noyes-energy-group.pages.dev/",
    "Noyes Energy Group H-17", "Noyes Energy Group H17",
    "H-17 Noyes Energy Group", "H17-Noyes-Energy-Group",
    "Noyes Energy Group | H-17 Atlantic facility",
    "Noyes Energy Group - H-17 Atlantic facility",
    "8131",
)


def seeds():
    for name in ORIGINAL_NAMES:
        utf8 = name.encode("utf-8")
        yield name, "string", name
        yield name, "bytes", utf8
        yield name, "int_big", int.from_bytes(utf8, "big")
        yield name, "crc32", zlib.crc32(utf8)
        yield name, "sha256_32", int.from_bytes(hashlib.sha256(utf8).digest()[:4], "big")


def originals(source: Path):
    spool = source.read_bytes()
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA256
    payloads = [
        bytes.fromhex(value.decode("ascii"))
        for value in re.findall(rb"PAYLOAD=([A-F0-9]{32})", spool)
    ]
    assert len(payloads) == 133
    pairs = {}
    for row, payload in enumerate(payloads):
        if row == 129:
            continue
        for endian in "<>":
            words = struct.unpack(endian + "4I", payload)
            for offset in range(3):
                pairs[(words[offset], words[offset + 1])] = (row, offset, endian)
    assert len(pairs) == 792
    return pairs


def scan(seed, pairs, count=COUNT):
    rng = random.Random(seed)
    previous = rng.getrandbits(32)
    found = []
    for index in range(count):
        current = rng.getrandbits(32)
        if (previous, current) in pairs:
            found.append((index, pairs[(previous, current)]))
        previous = current
    return found


def main(source: Path):
    pairs = originals(source)
    hits = [
        (name, kind, outcome)
        for name, kind, seed in seeds()
        for outcome in scan(seed, pairs)
    ]
    assert len(list(seeds())) == 90
    assert not hits, hits
    synthetic_rng = random.Random("Noyes Energy Group")
    for _ in range(195):
        synthetic_rng.getrandbits(32)
    expected = (synthetic_rng.getrandbits(32), synthetic_rng.getrandbits(32))
    assert scan("Noyes Energy Group", {expected: ("synthetic", 195, "<")}) == [
        (195, ("synthetic", 195, "<"))
    ]
    print("PRODUCER_HYPOTHESES", 90, "SOURCE_PAIRS", len(pairs),
          "CHECKED_OFFSETS", COUNT, "FULL_TWO_WORD_MATCHES", len(hits))
    print("SYNTHETIC_MATCH_AT_195 PASS; SELECTED_ROW_129_NOT_READ")
    print("NO_K04_COUPON_BITS_DETERMINED")


if __name__ == "__main__":
    assert len(sys.argv) == 2
    main(Path(sys.argv[1]))
