"""K04: source-window first-cycle census under the CRC-valid TRP2 shared-origin hypothesis.

python agents/agent3/k04_origin_window_census.py original-case.zip

Withholds printer row129 and all REC8 commitments, masked coupon and desk nonce.
Results are conditional MT-output-index statements, not historical clock order.
"""
import hashlib
import random
import struct
import sys
import zlib
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "agent46"), str(ROOT / "agent31"),
                str(ROOT / "agent23")]
from k04_cross_carrier_seed_windows import indexed_groups
from k04_mt_recursive_peel import close_group
from k04_mt_inverse_peel import inverse_twist
from k04_mt_rowstart import untemper

FULL = 0xFFFFFFFF
LOW31 = 0x7FFFFFFF
TRP = "evidence/recorder/trip-recorder.raw"


def shortest(start, edges):
    distance = [10**8] * 133
    distance[start] = 0
    for _ in range(133):
        changed = False
        for left, right, limit in edges:
            if distance[left] + limit < distance[right]:
                distance[right] = distance[left] + limit
                changed = True
        if not changed:
            break
    assert not changed, "negative cycle in row-order constraints"
    return distance


def synthetic_boundary():
    rng = random.Random(0x1234ABCDEF987654)
    initialized_623 = rng.getstate()[1][623]
    outputs = [untemper(rng.getrandbits(32)) for _ in range(625)]
    pairs = [(outputs[p], outputs[p + 227]) for p in (395, 396, 397)]
    mixed = [inverse_twist(a ^ b) for a, b in pairs]
    assert ((mixed[0] & LOW31) | (mixed[1] & 0x80000000)) == initialized_623
    assert ((mixed[1] & LOW31) | (mixed[2] & 0x80000000)) == outputs[0]
    assert (mixed[2] & LOW31) == (outputs[1] & LOW31)
    print("SYNTHETIC_CYCLE_BOUNDARY_PASS", True)


def main(path):
    synthetic_boundary()
    values, clusters = indexed_groups(path, True)
    assert len(values) == 133 and not values[129]
    with ZipFile(path) as z:
        recorder = z.read(TRP)
    assert recorder[:8] == b"TRP2DUMP"
    assert struct.unpack_from("<I", recorder, 12)[0] == 88
    record = recorder[16 + 26 * 24:16 + 27 * 24]
    assert zlib.crc32(record[:20]) == struct.unpack_from("<I", record, 20)[0]
    recorder_word = untemper(struct.unpack_from("<I", record, 12)[0])
    assert recorder_word == 0xBBC259FD

    # Union-Find source witness equalities already checked by indexed_groups().
    # Reverse pairwise edges give exact same-stream row start offsets.
    # Four output words per row supply a nonnegative chronological draw floor.
    edges = [(r + 1, r, -4) for r in range(132)]
    for entries in clusters.values():
        anchor, anchor_offset = entries[0]
        for r, offset in entries[1:]:
            d = offset - anchor_offset
            edges.extend(((anchor, r, d), (r, anchor, -d)))

    # Original CRC-valid TRP2 record26 matches the low31 MT ancestor of
    # printer row7 word3 -> row38 word0. That ancestor's predecessor occurs
    # at s7-394, requiring s7>=394 for any zero-origin common RNG stream.
    row7_group = next(g for g in clusters.values()
                      if any(r == 7 for r, _ in g))
    state, _ = close_group(row7_group, values)
    start = dict(row7_group)[7] + 1
    pairs = []
    for j in range(3):
        a, b = state[start + j], state[start + j + 227]
        assert a[0] == FULL and b[0] == FULL
        pairs.append((a[1], b[1]))
    mixed = [inverse_twist(a ^ b) for a, b in pairs]
    assert (mixed[2] & LOW31) == (recorder_word & LOW31)

    windows = []
    for entries in clusters.values():
        state, _ = close_group(entries, values)
        full = {p for p, (mask, _) in state.items() if mask == FULL}
        overlap = {p for p in full if p + 227 in full}
        representative, relative = entries[0]
        # s(r) >= 394 - shortest(r,7), using the original 42 witness
        # equalities + three recorder/RC17 bridges and four-output floors.
        min_row_phase = 394 - shortest(representative, edges)[7]
        for start in sorted(overlap):
            if start - 1 in overlap:
                continue
            length = 1
            while start + length in overlap:
                length += 1
            if length < 2:
                continue
            min_phase = min_row_phase + start - relative
            last_full_first_cycle = 623 - 227 - (length - 1)
            windows.append((min(r for r, _ in entries), length,
                            min_phase, last_full_first_cycle))
    assert len(windows) == 35, len(windows)
    viable = [w for w in windows if w[2] <= w[3]]
    assert len(viable) == 1 and viable[0][:2] == (3, 5), viable
    assert viable[0][2:] == (321, 392), viable

    print("TRP2_record26_crc_valid", True)
    print("TRP2_record26_untempered", f"{recorder_word:08X}")
    print("conditional_absolute_row7_floor", 394)
    print("source_227_pair_windows_ge2", len(windows))
    print("fully_first_cycle_possible_windows", viable)
    print("fully_first_cycle_excluded_windows", len(windows) - len(viable))
    print("row7_three_pair_window_absolute_phase_floor", 395)
    print("row7_three_pair_window_full_first_cycle_phase_ceiling", 394)

    # Boundary s7=394 is possible only as a phase *hypothesis*; the
    # existence of a source-conforming common generator is not proven.
    # At this exact phase, row7 pairs start at 395, and their inverse-twist
    # components recover last seeded state word S[623] and first output X[0].
    initialized_623 = (mixed[0] & LOW31) | (mixed[1] & 0x80000000)
    first_output = (mixed[1] & LOW31) | (mixed[2] & 0x80000000)
    assert initialized_623 == 0x2F9F1C79
    assert first_output == 0x4373C70C
    print("if_s7_equals_394_seeded_state_623", f"{initialized_623:08X}")
    print("if_s7_equals_394_first_output_X0", f"{first_output:08X}")
    print("if_s7_equals_394_second_output_X1", f"{recorder_word:08X}")
    print("selected_row129_withheld", True)
    print("K04_K08_UNRESOLVED", True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python agents/agent3/k04_origin_window_census.py case.zip")
    main(Path(sys.argv[1]))
