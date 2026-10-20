"""SFT: read-only original AX checkpoint halfwords vs K04 conditional future-donor pairs.

Uses prior source-derived index955 future XOR equations; never reads row129
payload, mask, acceptance commitments or verifier.
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "resources/evidence"
TRANSFER_SHA = "32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf"
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def temper(word: int) -> int:
    word ^= word >> 11
    word ^= (word << 7) & 0x9D2C5680
    word ^= (word << 15) & 0xEFC60000
    return (word ^ (word >> 18)) & 0xFFFFFFFF


def undo_right(word: int, shift: int) -> int:
    result = word
    for _ in range(6):
        result = word ^ (result >> shift)
    return result & 0xFFFFFFFF


def undo_left(word: int, shift: int, mask: int) -> int:
    result = word
    for _ in range(8):
        result = word ^ ((result << shift) & mask)
    return result & 0xFFFFFFFF


def untemper(word: int) -> int:
    return undo_right(undo_left(undo_left(undo_right(word, 18), 15, 0xEFC60000), 7, 0x9D2C5680), 11)


def upper16_options(mask: int, known: int) -> set[int]:
    assert known & ~mask == 0
    unknown_bits = [1 << bit for bit in range(32) if not (mask & (1 << bit))]
    assert len(unknown_bits) <= 2
    return {
        temper(known ^ sum(((choice >> index) & 1) * bit for index, bit in enumerate(unknown_bits))) >> 16
        for choice in range(1 << len(unknown_bits))
    }


def main() -> None:
    transfer = (ROOT / "transfers/transfer-audit.jsonl").read_bytes()
    spool = (ROOT / "print/spool-reconstruction.log").read_bytes()
    assert hashlib.sha256(transfer).hexdigest() == TRANSFER_SHA
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    rows = [json.loads(line) for line in transfer.splitlines()]
    checkpoints = [r for r in rows if r["kind"] == "CHUNK"]
    assert len(checkpoints) == 64
    assert {r["transfer"] for r in checkpoints} == {"AX-7778", "AX-7781", "AX-7782", "AX-7783"}

    # Original producer positive control: four AX-7778 halfwords match upper16
    # of reconstructed MT predecessor outputs from intact spool rows34 and64.
    payloads = re.findall(rb"PAYLOAD=([A-F0-9]{32})", spool)
    assert len(payloads) == 133
    left = [untemper(x) for x in struct.unpack("<4I", bytes.fromhex(payloads[34].decode()))]
    right = [untemper(x) for x in struct.unpack("<4I", bytes.fromhex(payloads[64].decode()))]
    ax7778 = sorted((r for r in checkpoints if r["transfer"] == "AX-7778"), key=lambda r: (r["seq"], r["attempt"]))
    for index, record in enumerate(ax7778[11:15]):
        z = left[index] ^ right[index]
        low31 = ((((z ^ (0x9908B0DF if z & 0x80000000 else 0)) << 1) | (z >> 31)) & 0x7FFFFFFF)
        expected = {temper(low31) >> 16, temper(low31 | 0x80000000) >> 16}
        observed = int(record["checkpoint"][2:] + record["checkpoint"][:2], 16)
        assert observed in expected
    print("ORIGINAL_AX7778_HIGH16_POSITIVE_CONTROL PASS")

    # Source-only future-state XORs from Agent29's original-print-payload GF2 elimination.
    # The selected K04 source row129 and target digest are absent by construction.
    relations = [
        ("X1412_X1866", 0xFFFFFFFF, 0xBD2761F8),
        ("X1185_X1412", 0xBFFFFFFF, 0x359EC0C7),
        ("X1185_X1866", 0xBFFFFFFF, (0x114F2035 ^ 0x99F6810A) & 0xBFFFFFFF),
        ("X1411_X1865", 0x9FFFFFFF, 0x0CDE27B9),
    ]
    assert temper(0xBD2761F8) == 0x4692D6B0
    for name, mask, constant in relations:
        allowed = upper16_options(mask, constant)
        matches = []
        for view in ("native", "swapped"):
            values = [int(r["checkpoint"], 16) for r in checkpoints]
            if view == "swapped":
                values = [((value & 255) << 8) | (value >> 8) for value in values]
            for i, a in enumerate(values):
                for j in range(i+1, len(values)):
                    if a ^ values[j] in allowed:
                        matches.append((view, i, j))
        print(name, "source_high16_XOR_signatures", sorted(f"{v:04X}" for v in allowed), "AX_pair_hits", len(matches))
        assert not matches
    print("FOUR_FUTURE_PAIRS_ZERO_AX_HIGH16_MATCHES; ACTUAL_K04_BITS=0; NO_TARGET_HASH_READ")


if __name__ == "__main__":
    main()
