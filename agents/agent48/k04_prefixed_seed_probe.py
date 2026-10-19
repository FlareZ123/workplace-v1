"""Source-only K04 shifted-origin first-cycle seed test.
Usage: python agents/agent48/k04_prefixed_seed_probe.py original-case.zip
Selected printer row129, recovery mask and REC8 acceptance withheld.
"""
import random
import struct
import sys
from pathlib import Path
from zipfile import ZipFile

AGENTS = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(AGENTS / "agent1"), str(AGENTS / "agent23")]
from k04_python_seed_fragments import extract_pairs, fragments, verify_seed
from k04_mt_rowstart import discover, bound_function, untemper


def synthetic_controls():
    for n, seed in ((1, 0xDEADBEEF), (2, 0xA987ED123456EF78)):
        for phase in (0, 17, 100, 300, 360, 390, 392):
            rng = random.Random(seed)
            state = [untemper(rng.getrandbits(32)) for _ in range(624)]
            pairs = [(state[phase + j], state[phase + j + 227])
                     for j in range(5)]
            assert fragments(pairs, phase, n) == {
                j: (seed >> (32 * j)) & 0xFFFFFFFF for j in range(n)}
            assert verify_seed(seed, [(phase, pairs)])
    return 14


def main(source):
    within, boundary = discover(source)
    assert (len(within), len(boundary)) == (25, 17)
    difference = bound_function(within, boundary)
    assert difference(0, 10) == (50, 104)
    assert difference(10, 13) == (24, 78)
    assert difference(10, 41) == (227, 227)

    with ZipFile(source) as archive:
        raw = archive.read("evidence/recorder/trip-recorder.raw")
    _, node, event, latch, seq, ctl, _, crc = struct.unpack_from(
        "<IHBBI4sII", raw, 16 + 28 * 24)
    assert (node, event, latch, seq) == (49, 82, 2, 992)
    assert untemper(int.from_bytes(ctl, "little")) == 0x348ADB23

    # Under a common chronological output stream, this recorder control
    # is at s41-623=s10-396, whose absolute index must be nonnegative.
    # s10-s0<=104 implies at least 292 draws before printer row0.
    assert 396 - difference(0, 10)[1] == 292
    # s13-s10>=24 places row13's initial pair at >=419, beyond
    # the last first-cycle five-pair start (392).
    assert 396 + difference(10, 13)[0] - 1 == 419 > 392

    print("synthetic_controls_pass", synthetic_controls())
    row3_pairs = extract_pairs(source)[0]
    assert row3_pairs[0] == (0x482F6361, 0xA757A2AC)
    for n in (1, 2):
        reconstructed = 0
        accepted = []
        for phase in range(393):
            fragment = fragments(row3_pairs, phase, n)
            if fragment is None or len(fragment) != n:
                continue
            reconstructed += 1
            seed = sum(fragment[i] << (32 * i) for i in range(n))
            if verify_seed(seed, [(phase, row3_pairs)]):
                accepted.append((phase, f"{seed:X}"))
        assert not accepted
        print("seed_words", n, "first_cycle_phases", 393,
              "fragment_candidates", reconstructed, "matched", accepted)
    print("common_stream_prefix_floor", 292)
    print("row13_initial_seed_inversion_first_cycle_applicable", False)
    print("row3_first_cycle_integer_seeds_32_64bits_no_match", True)
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_prefixed_seed_probe.py original-case.zip")
    main(Path(sys.argv[1]))
