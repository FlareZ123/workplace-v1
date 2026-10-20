"""H17 K04: source-only 175-state seed residue discriminator.

Uses original AX-7778 and intact printer words, excluding disputed row129,
the K04 mask/acceptance digest, K08, and original verifier.
"""
import hashlib
import json
import random
import re
import struct
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agents" / "agent26"))
import k04_seven_residue_gate as core
import k04_ax_row9_forward_bridge as bridge

LOW = 0x7FFFFFFF
LENGTHS = (1, 5, 7, 25, 35, 175)
TRANSFER_SHA = "32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf"


def key_low31(a, b, c_low, index, length):
    prior = ((b + index - 1) ^ core.mix(a, 1566083941)) & core.M
    base = core.BASE[index] ^ core.mix(prior, 1664525)
    return (((c_low + index) ^ core.mix(b, 1566083941))
            - base - ((index - 1) % length)) & LOW


def compare(early, late, phase, length):
    i1, i2 = phase - 172, phase + 3
    assert (i1 - 1) % length == (i2 - 1) % length
    a, a_low = early
    b, b_low = late
    return (key_low31(a[0], a[1], a_low, i1, length),
            key_low31(b[-2], b[-1], b_low, i2, length))


def real_source(zip_path):
    rows = core.read_rows(zip_path)
    with zipfile.ZipFile(zip_path) as z:
        spool = z.read("evidence/print/spool-reconstruction.log")
        audit = z.read("evidence/transfers/transfer-audit.jsonl")
    assert hashlib.sha256(spool).hexdigest() == core.SOURCE_SHA
    assert hashlib.sha256(audit).hexdigest() == TRANSFER_SHA
    lines = [s for s in spool.decode().splitlines() if s.startswith("2026-")]
    assert len(lines) == 133
    raw = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", lines[9]).group(1))
    row9 = [core.untemper(word) for word in struct.unpack("<4I", raw)]
    chunks = sorted(
        (obj for line in audit.decode().splitlines()
         if (obj := json.loads(line)).get("kind") == "CHUNK"
         and obj.get("transfer") == "AX-7778"),
        key=lambda obj: (int(obj["seq"]), int(obj["attempt"])))
    assert len(chunks) == 16
    checkpoints = [int.from_bytes(bytes.fromhex(x["checkpoint"]), "little")
                   for x in chunks[5:8]]
    ancestors = bridge.ax_ancestors(rows[33], rows[63], checkpoints)
    assert ancestors == [0x51DA82D0, 0x174C046A, 0x6447255B]
    early = bridge.row9_fragment(ancestors, row9)
    late = core.infer(rows)[1]
    assert early == ([0x418BDA1E, 0x2E02BC3D], 0x38EBB043)
    assert late[0][1:] == [0x6CE0E225, 0xF4E8FCB2, 0xC517EB25, 0x7D3AAF35]
    assert late[1] == 0x31FD69FC
    return early, late


def positive_controls():
    count = 0
    for length in LENGTHS:
        for phase in (402, 535, 563, 564, 590, 620):
            for trial in (0, 1):
                words = [(0xA716E19A + j * 0x9E3779B9 + trial * 0x31EA6)
                         & core.M for j in range(length)]
                seed = sum(word << (32 * j) for j, word in enumerate(words))
                state = random.Random(seed).getstate()[1][:624]
                early = (list(state[phase-174:phase-172]), state[phase-172] & LOW)
                late = (list(state[phase-2:phase+3]), state[phase+3] & LOW)
                left, right = compare(early, late, phase, length)
                assert left == right == (words[(phase-173) % length] & LOW)
                count += 1
    print("ACTUAL_CPYTHON_SEEDED_POSITIVE_CONTROLS", count, "PASS")


def main(zip_path):
    positive_controls()
    early, late = real_source(zip_path)
    print("ORIGINAL_ROW9", early, "ORIGINAL_LATE", late)
    for length in LENGTHS:
        survivors = [phase for phase in range(402, 621)
                     if (lambda pair: pair[0] == pair[1])(
                         compare(early, late, phase, length))]
        assert not survivors, (length, survivors)
        print("SEED_ARRAY_WORDS", length, "PHASES", 219, "MATCHES", len(survivors))
    print("TARGET_ROW129_AND_ACCEPTANCE_UNREAD; K04_GAIN_ZERO")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python agents/agent15/k04_row9_late_175_seed_sft.py ORIGINAL_CASE.zip")
    main(Path(sys.argv[1]))
