"""Read-only ESC-N retry xorshift128 producer crack, target excluded.

Usage: python agents/agent41/k04_tail_xorshift128_sft.py original-export.zip
This uses the intact outer attempts as a 128-bit state/output holdout.
"""
import argparse
import hashlib
import re
from pathlib import Path
from zipfile import ZipFile

SPOOL = "evidence/print/spool-reconstruction.log"
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
U32 = 0xFFFFFFFF


def step(state):
    x, y, z, w = state
    t = x ^ ((x << 11) & U32)
    next_w = (w ^ (w >> 19) ^ t ^ (t >> 8)) & U32
    return (y, z, w, next_w), next_w


def decode(payload, endian, reverse):
    words = [int.from_bytes(payload[i:i + 4], endian) for i in (0, 4, 8, 12)]
    return tuple(words[::-1] if reverse else words)


def encode(words, endian, reverse):
    ordered = words[::-1] if reverse else words
    return b"".join(word.to_bytes(4, endian) for word in ordered)


def predict(first_words):
    state = tuple(first_words)
    outputs = []
    for _ in range(8):
        state, value = step(state)
        outputs.append(value)
    return tuple(outputs)


def run(source):
    with ZipFile(source) as archive:
        spool = archive.read(SPOOL)
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    selected_lines = [line for line in spool.decode("ascii").splitlines()
                      if "JOB=PS-261003-0417" in line and "CLASS=RECOVER" in line]
    assert len(selected_lines) == 3
    assert [int(re.search(r"ATTEMPT=(\\d+)", line).group(1))
            for line in selected_lines] == [1, 2, 3]

    # Deliberately discard the 18:02 ACK line before payload extraction.
    first_line, _, last_line = selected_lines
    first = bytes.fromhex(re.search(r"PAYLOAD=([A-F0-9]{32})", first_line).group(1))
    last = bytes.fromhex(re.search(r"PAYLOAD=([A-F0-9]{32})", last_line).group(1))
    matched = []
    for endian in ("little", "big"):
        for reverse in (False, True):
            observed = decode(first, endian, reverse)
            proposed = predict(observed)
            predicted_last = encode(proposed[4:], endian, reverse)
            print("orientation", endian, "reversed", reverse,
                  "predicted_1803", predicted_last.hex().upper(),
                  "matching_words", sum(a == b for a, b in
                                        zip(proposed[4:], decode(last, endian, reverse))))
            if predicted_last == last:
                matched.append((endian, reverse, encode(proposed[:4], endian, reverse)))

            state = (0x12345678, 0x9ABCDEF0, 0x11EE22DD, 0x76543210)
            synthetic = []
            for _ in range(12):
                state, value = step(state)
                synthetic.append(value)
            serialized = encode(synthetic[:4], endian, reverse)
            assert predict(decode(serialized, endian, reverse)) == tuple(synthetic[4:])
    assert not matched
    print("Original source matches: 0; independent synthetic controls: 4/4 PASS")
    print("Selected K04 ACK bytes, mask, acceptance hash, verifier: NOT READ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("original_zip", type=Path)
    run(parser.parse_args().original_zip)
