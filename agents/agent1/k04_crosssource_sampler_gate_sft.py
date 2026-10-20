"""SFT: source-indexed CLASS contradiction in all six cross-source K04 index fixtures.

Use: python agents/agent1/k04_crosssource_sampler_gate_sft.py path/to/original.zip

Read-only: original spool SHA-pinned, row129 excluded from projector,
no recovery mask, acceptance commitment, nonce, or HMAC consulted.
The model assumes an accepted ordinary CLASS 3-bit selector directly
precedes each four-word printer payload.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import struct
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from k04_source_dest_parity_projection import original_rows, synthetic, untemper, temper
from k04_hidden_selector_nogood_pruner import selector_nogoods

SOURCE_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
A = 0x9908B0DF
EXPECTED_FAILS = {950: 5, 951: 6, 952: 10, 953: 12, 954: 5, 955: 10}


def twist(x: int, y: int) -> int:
    z = (x & 0x80000000) | (y & 0x7FFFFFFF)
    return ((z >> 1) ^ (A if z & 1 else 0)) & 0xFFFFFFFF


def source_witness(zip_path: Path, starts: list[int]) -> tuple[int, int, int, int]:
    """Use two intact original payloads to predict row84's hidden CLASS."""
    with zipfile.ZipFile(zip_path) as z:
        raw = z.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256
    lines = [line for line in raw.decode().splitlines()
             if line.startswith("2026-")]
    assert len(lines) == 133
    assert "CLASS=LABEL" in lines[84]

    def words(row: int) -> tuple[int, int, int, int]:
        payload = re.search(r"PAYLOAD=([A-F0-9]{32})", lines[row]).group(1)
        return tuple(untemper(x) for x in struct.unpack("<4I", bytes.fromhex(payload)))

    first, middle = words(1), words(54)
    t1, t54, t84 = starts[1], starts[54], starts[84]
    matches = [
        (i, j)
        for i in range(3)
        for j in range(4)
        if t1 + i + 397 == t54 + j
        and t1 + i + 624 == t84 - 1
    ]
    assert len(matches) == 1, matches
    i, j = matches[0]
    prediction = middle[j] ^ twist(first[i], first[i + 1])
    visible = temper(prediction)
    assert visible >> 29 == 3, "Expected rejected CLASS code"
    return i, j, prediction, visible


def main(zip_path: Path) -> None:
    # Positive controls: MT temper/untemper and true consecutive 624-word recurrence.
    rng = random.Random(433)
    stream = [untemper(rng.getrandbits(32)) for _ in range(660)]
    for t in (0, 7, 21, 33):
        assert stream[t + 624] == stream[t + 397] ^ twist(stream[t], stream[t + 1])
    for v in (0, 1, 0x12345678, 0xFFFFFFFF, 0x9F24BDC1):
        assert temper(untemper(v)) == v
    controls = synthetic(433)
    assert selector_nogoods(*controls[:4])["contradiction_count"] == 0
    print("SYNTHETIC_CONTROLS PASS", flush=True)

    fixture = json.loads((HERE.parent / "agent5" / "k04_crosssource_six_vectors.json")
                         .read_text(encoding="utf-8"))
    assert fixture["source_spool_sha256"] == SOURCE_SHA256
    rows, classes, dests = original_rows(str(zip_path))
    assert rows[129] == [] and classes[84] == 0
    for index, expected_fails in EXPECTED_FAILS.items():
        starts = fixture["row_starts"][str(index)]
        assert len(starts) == 133 and starts[0] == 0 and starts[129] == index
        i, j, state, visible = source_witness(zip_path, starts)
        expected = 0x766C3AD1 if index == 954 else 0x65FDAF9F
        assert visible == expected
        result = selector_nogoods(rows, starts, classes, dests)
        assert result["contradiction_count"] == expected_fails
        assert any(
            c["target_field"] == "CLASS" and c["target_row"] == 84
            and c["producer"] == "forward" and c["predicted_codes"] == [3]
            for c in result["source_nogoods"]
        )
        print(
            f"index={index} row1_word={i} row54_word={j} "
            f"predicted_CLASS={visible:08X} code=3 original_LABEL_code=0 "
            f"checked={result['checked_hidden_selectors']} "
            f"contradictions={result['contradiction_count']} PASS", flush=True
        )
    print("PASS all six conditional common-MT two-sampler geometries rejected")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(Path(sys.argv[1]))
