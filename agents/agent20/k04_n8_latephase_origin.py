"""Bounded source-only 256-bit CPython MT seed reconstruction in the
recorder-origin-conditioned late-first-cycle printer window.

Run: python agents/agent20/k04_n8_latephase_origin.py original-case.zip
Reads only SHA-pinned unselected printer rows; no K04/K08 masks or digests.
Source bounds are conditional on the historical common-MT and recorder origin.
"""
import collections
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent8"))
from k04_seed_stitch import (
    bridge, compatible, extract_pairs, fragments, pair_group,
    rows, temper, untemper,
)

WORD = 0xFFFFFFFF
LENGTHS = {3: 5, 10: 4, 11: 3, 13: 5, 14: 4}


def synthetic_control():
    seed = sum(((0xA1058C11 + 0x13579B1 * i) & WORD) << (32*i)
               for i in range(8))
    rng = random.Random(seed)
    state = [untemper(rng.getrandbits(32)) for _ in range(624)]
    phases = {3: 321, 10: 357, 11: 363, 13: 382, 14: 392}
    samples = {
        row: [(state[p+j], state[p+j+227])
              for j in range(LENGTHS[row])]
        for row, p in phases.items()
    }
    keys = {}
    for row in (3, 10, 13, 14):
        keys = compatible(keys, fragments(samples[row], phases[row], 8))
        assert keys is not None
    original = {i: (seed >> (32*i)) & WORD for i in range(8)}
    assert all(keys[i] == original[i] for i in keys)
    first = bridge(keys, phases[10], phases[11],
                   samples[10], samples[11], 8)
    second = bridge(keys, phases[13], phases[14],
                    samples[13], samples[14], 8)
    assert first is not None and second is not None
    for candidate in (first, second):
        assert candidate == original
    print("real_CPython_256bit_synthetic_control PASS")


def scan(original_zip):
    # The recorder/source common-stream origin premise places printer row0
    # at >=307 and printer row3 >=15 outputs later. Its row3 predecessor
    # pair therefore starts at absolute p_a >=321. First cycle and row14's
    # four pairs imply p_d <=393; printer pair bounds imply p_a <=333.
    a, c, b, d = extract_pairs(original_zip)
    eleven = pair_group(original_zip, 11, 3)
    observed_holdout = temper(rows(original_zip)[34][3])
    stats = collections.Counter()
    placements = []
    for pa in range(321, 334):
        ka = fragments(a, pa, 8)
        for pb in range(pa+59, min(pa+114, 393)):
            ab = compatible(ka, fragments(b, pb, 8))
            if ab is None:
                continue
            for pc in range(max(pa+36, pb-77), min(pa+91, pb-22, 394)):
                abc = compatible(ab, fragments(c, pc, 8))
                if abc is None:
                    continue
                for pd in range(pb+8, min(pb+63, 394)):
                    keys = compatible(abc, fragments(d, pd, 8))
                    if keys is None:
                        continue
                    stats["phase_compatible"] += 1
                    placements.append((pa, pc, pb, pd))
                    completions = [keys]
                    if pd-pb <= 18:
                        filled = bridge(keys, pb, pd, b, d, 8)
                        if filled is not None:
                            stats["bridge_13_14"] += 1
                            completions.append(filled)
                    for p11 in range(pc+4, min(pc+19, pb-6)):
                        filled = bridge(keys, pc, p11, c, eleven, 8)
                        if filled is None:
                            continue
                        stats["bridge_10_11"] += 1
                        completions.append(filled)
                        if pd-pb <= 18:
                            combined = bridge(filled, pb, pd, b, d, 8)
                            if combined is not None:
                                stats["dual_bridge"] += 1
                                completions.append(combined)
                    for candidate in completions:
                        if len(candidate) != 8:
                            continue
                        stats["full_keys"] += 1
                        seed = sum(candidate[i] << (32*i) for i in range(8))
                        rng = random.Random(seed)
                        predicted = None
                        for _ in range(pa+233):
                            predicted = rng.getrandbits(32)
                        if predicted == observed_holdout:
                            stats["source_holdout_PASS"] += 1
                            print("SOURCE_HOLDOUT_MATCH", pa, pc, pb, pd,
                                  hex(seed))
    print("source_only_selected_row129_withheld True")
    print("source_phase_placements", placements)
    print("observed_row34_word3", f"{observed_holdout:08X}")
    print("source_scan_counts", dict(stats))
    assert placements == [(321, 357, 382, 392),
                          (322, 358, 383, 393)]
    assert stats["full_keys"] == 16
    assert stats["source_holdout_PASS"] == 0
    print("conditional_n8_late_origin_NO_MATCH")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_n8_latephase_origin.py original-case.zip")
    synthetic_control()
    scan(Path(sys.argv[1]))
