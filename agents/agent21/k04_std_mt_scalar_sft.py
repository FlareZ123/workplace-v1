"""H-17 SFT: source-pinned test of standard MT19937 scalar initialization.

Run from repository root: python agents/agent21/k04_std_mt_scalar_sft.py
Uses the existing independently controlled inverse-MT fixture in Agent26.
No selected K04 row, route mask, K08 or REC8 commitments are read.
"""
import hashlib
import re
import runpy
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
agent26 = runpy.run_path(str(ROOT / "agents/agent26/k04_seven_residue_gate.py"))
source = ROOT / "resources/evidence/print/spool-reconstruction.log"
spool = source.read_bytes()
assert hashlib.sha256(spool).hexdigest() == agent26["SOURCE_SHA"]
lines = [line for line in spool.decode().splitlines() if line.startswith("2026-")]
assert len(lines) == 133
positions = agent26["POSITIONS"]
rows = {}
for row in positions:
    assert row != 129
    raw = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", lines[row]).group(1))
    rows[row] = [agent26["untemper"](x) for x in struct.unpack("<4I", raw)]

early, (late, low), middle = agent26["infer"](rows)
assert late == [0xB30BF870, 0x6CE0E225, 0xF4E8FCB2, 0xC517EB25, 0x7D3AAF35]
assert low == 0x31FD69FC

MASK = 0xFFFFFFFF


def std_scalar_state(seed):
    result = [seed & MASK]
    for i in range(1, 624):
        old = result[-1]
        result.append((1812433253 * (old ^ (old >> 30)) + i) & MASK)
    return result


def indices(values):
    return [((b - 1812433253 * (a ^ (a >> 30))) & MASK)
            for a, b in zip(values, values[1:])]


def original_phase_test():
    implied = indices(late)
    possible = [p for p in range(396, 622)
                if implied == list(range(p - 1, p + 3))]
    assert not possible
    print("source_SHA256", agent26["SOURCE_SHA"])
    print("late_pre_twist_state", " ".join(f"{x:08X}" for x in late))
    print("required_seed_init_indices", implied)
    print("tested_first_cycle_absolute_phases", "396..621")
    print("source_compatible_standard_scalar_MT_phases", len(possible))


def synthetic_test():
    tested = 0
    for seed in (0, 5489, 123456789, 0xF00DBEEF):
        state = std_scalar_state(seed)
        for p in (396, 445, 562, 621):
            observed = state[p - 2:p + 3]
            assert indices(observed) == list(range(p - 1, p + 3))
            tested += 1
    print("synthetic_positive_seed_phase_checks", tested, "PASS")


if __name__ == "__main__":
    synthetic_test()
    original_phase_test()
    print("selected_row129_unread", True)
    print("REC8_target_bits_recovered", 0)
