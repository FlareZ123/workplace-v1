"""Derive a selected K04 coupon from a recovered MT19937 scalar seed.

Requires 128/128 original regular spool payload matches and four intact
held-out tail matches before trying predicted selected coupon bytes against
the unchanged source K04 acceptance commitment. Read-only, standard library.
"""
import argparse
import hashlib
import json
import random
import re
import struct
import zipfile
from pathlib import Path

SOURCE_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
SELECTED_ROW = 129


def source(root):
    def read(path):
        if root.is_file():
            with zipfile.ZipFile(root) as z:
                return z.read(path)
        return (root / path).read_bytes()

    raw = read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256
    payloads = [
        bytes.fromhex(x)
        for x in re.findall(rb"PAYLOAD=([0-9A-F]{32})", raw)
    ]
    assert len(payloads) == 133
    mask = bytes.fromhex(
        json.loads(read("evidence/recovery-routing.json"))["K04"]["masked_component"]
    )
    target = json.loads(read("acceptance.json"))["slot_sha256"]["K04"]
    return payloads, mask, target


def fit(seed, payloads, mask, target, outputs=15000):
    rng = random.Random(seed)
    words = [rng.getrandbits(32) for _ in range(outputs)]
    inverse = {tuple(words[i:i+4]): i for i in range(outputs-3)}
    observed = [tuple(struct.unpack("<4I", p)) for p in payloads]
    offsets = [inverse.get(x) for x in observed]
    intact = sum(i is not None for i in offsets[:128])
    print("seed", repr(seed), "regular_matched", intact, "of_128")
    if intact != 128:
        return None

    assert all(offsets[i] < offsets[i+1] for i in range(127))
    print("regular_start_indices", offsets[:8], "last", offsets[127])
    print("tail_record_indices", offsets[128:])
    other_tail = (128, 130, 131, 132)
    if any(offsets[i] is None for i in other_tail):
        return None
    assert offsets[128] < offsets[130] < offsets[131] < offsets[132]
    print("heldout_tail_matched", len(other_tail), "of_4")

    lo, hi = offsets[128]+4, offsets[130]-4
    assert lo <= hi
    matches = []
    for offset in range(lo, hi+1):
        raw_coupon = struct.pack("<4I", *words[offset:offset+4])
        candidate = bytes(a ^ b for a, b in zip(raw_coupon, mask))
        if hashlib.sha256(candidate).hexdigest() == target:
            matches.append({
                "stream_offset": offset,
                "raw_coupon": raw_coupon.hex().upper(),
                "K04": candidate.hex().upper(),
            })
    print("offsets_tested", hi-lo+1, "original_K04_matches", matches)
    return matches


def synthetic_control():
    seed = 12345
    rng = random.Random(seed)
    rows = []
    for _ in range(133):
        rng.choice(("LABEL", "STORES", "RECOVER"))
        rng.choice(("desk", "bench", "store"))
        rows.append(rng.randbytes(16))
    mask = bytes(range(16))
    correct_coupon = rows[SELECTED_ROW]
    target = hashlib.sha256(bytes(a ^ b for a, b in zip(correct_coupon, mask))).hexdigest()
    rows[SELECTED_ROW] = bytes(b ^ 0xA5 for b in correct_coupon)
    result = fit(seed, rows, mask, target)
    assert result and len(result) == 1
    assert result[0]["raw_coupon"] == correct_coupon.hex().upper()
    print("synthetic_control_PASS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("resources"))
    parser.add_argument("--seed", type=int)
    parser.add_argument("--outputs", type=int, default=15000)
    args = parser.parse_args()
    synthetic_control()
    if args.seed is not None:
        fit(args.seed, *source(args.source), outputs=args.outputs)


if __name__ == "__main__":
    main()
