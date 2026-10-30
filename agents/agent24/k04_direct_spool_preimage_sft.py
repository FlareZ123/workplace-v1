"""H-17 K04 printer-only MT19937 direct-antecedent SFT.

Read-only original-archive test. It generates every one-step full-word MT
prediction with two intact ordinary printer sources and compares the frozen
prediction set to intact late controls and the disputed selected record.
These comparisons do not authenticate the selected original medium or mask.
"""
from __future__ import annotations

import argparse
import hashlib
import random
import re
import struct
import zipfile
from collections import defaultdict
from pathlib import Path

SPOOL_PATH = "evidence/print/spool-reconstruction.log"
SPOOL_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MASK32 = 0xFFFFFFFF
MAGIC = 0x9908B0DF


def undo_right(value: int, shift: int) -> int:
    result = value
    for _ in range(6):
        result = value ^ (result >> shift)
    return result & MASK32


def undo_left(value: int, shift: int, mask: int) -> int:
    result = value
    for _ in range(7):
        result = value ^ ((result << shift) & mask)
    return result & MASK32


def untemper(value: int) -> int:
    value = undo_right(value, 18)
    value = undo_left(value, 15, 0xEFC60000)
    value = undo_left(value, 7, 0x9D2C5680)
    return undo_right(value, 11)


def temper(value: int) -> int:
    value ^= value >> 11
    value ^= (value << 7) & 0x9D2C5680
    value ^= (value << 15) & 0xEFC60000
    value ^= value >> 18
    return value & MASK32


def predict(a: int, successor: int, middle: int) -> int:
    mixed = (a & 0x80000000) | (successor & 0x7FFFFFFF)
    return (middle ^ (mixed >> 1) ^ (MAGIC if successor & 1 else 0)) & MASK32


def read_spool(archive: Path) -> list[tuple[int, int, int, int]]:
    with zipfile.ZipFile(archive) as source:
        blob = source.read(SPOOL_PATH)
    digest = hashlib.sha256(blob).hexdigest()
    assert digest == SPOOL_SHA256, f"Unexpected spool digest: {digest}"
    output = []
    for line in blob.decode("ascii").splitlines():
        match = re.search(r"\bPAYLOAD=([A-F0-9]{32})\b", line)
        if match:
            serialized = struct.unpack("<4I", bytes.fromhex(match.group(1)))
            output.append(tuple(untemper(word) for word in serialized))
    assert len(output) == 133, len(output)
    assert all(
        temper(word) == raw
        for words, line in zip(output, [
            struct.unpack("<4I", bytes.fromhex(match.group(1)))
            for line in blob.decode("ascii").splitlines()
            if (match := re.search(r"\bPAYLOAD=([A-F0-9]{32})\b", line))
        ])
        for word, raw in zip(words, line)
    )
    return output


def source_predictions(
    words: list[tuple[int, int, int, int]],
) -> dict[int, list[tuple[int, int, int, int]]]:
    """Use only original rows 0..127: A[k], A[k+1] and later B[k+397]."""
    predictions: dict[int, list[tuple[int, int, int, int]]] = defaultdict(list)
    for a_row in range(128):
        for a_word in range(3):
            a, b = words[a_row][a_word:a_word + 2]
            for middle_row in range(a_row + 1, 128):
                for middle_word in range(4):
                    value = predict(a, b, words[middle_row][middle_word])
                    predictions[value].append((a_row, a_word, middle_row, middle_word))
    return predictions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True, help="Original 43-member case ZIP")
    args = parser.parse_args()

    synthetic = random.Random(314159)
    synthetic_state = [untemper(synthetic.getrandbits(32)) for _ in range(2000)]
    for index in (0, 45, 199, 600, 1100):
        assert predict(
            synthetic_state[index],
            synthetic_state[index + 1],
            synthetic_state[index + 397],
        ) == synthetic_state[index + 624]
    print("SYNTHETIC_MT_CONTROLS_PASS 5")

    words = read_spool(args.archive)
    candidates = source_predictions(words)
    count = sum(map(len, candidates.values()))
    assert count == 97536
    print("ORIGINAL_SOURCE_SHA256", SPOOL_SHA256)
    print("ORIGINAL_SOURCE_ROWS 128 (ordinary only); held-out late rows 128..132")
    print("PREDICTION_ASSIGNMENTS", count, "UNIQUE_WORD_VALUES", len(candidates))

    controls = [(131, 0, (44, 0, 97, 3)), (132, 3, (45, 0, 98, 3))]
    for target_row, target_word, expected in controls:
        hits = candidates.get(words[target_row][target_word], [])
        assert hits == [expected], (target_row, target_word, hits)
        print("ORIGINAL_BLIND_LATE_CONTROL_PASS", target_row, target_word, expected)

    for selected_word, original_value in enumerate(words[129]):
        hits = candidates.get(original_value, [])
        print("DISPUTED_ACK_18_02_WORD_MATCHES", selected_word, len(hits))
        assert not hits, (selected_word, hits)
    print("SCOPE_NO_MATCH original three-ordinary-word full-word antecedents")
    print("H17_SELECTED_K04_AUTHENTICATED_BITS_GAINED 0/128")
    print("H17_FINAL_K08_ATTESTED_WORDS_GAINED 0")


if __name__ == "__main__":
    main()
