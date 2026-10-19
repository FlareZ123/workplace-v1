"""Synthetic two-sampler target-rank probe near the original conditional index window.

Always synthetic: model rules are inferred, not authenticated historical code.
No original acceptance material or original selected row129 is used.
"""

import random
from k04_global_target_projection import solve_target, temper, untemper

CASES = {
    433: (946, 33, 90),
    958: (949, 65, 58),
    2267: (950, 128, 0),
    2311: (955, 128, 0),
    3142: (954, 64, 64),
    6785: (953, 128, 0),
    8113: (954, 65, 58),
    8122: (952, 65, 58),
}


def simulate(seed):
    rng = random.Random(seed)
    used = 0

    def draw(bits):
        nonlocal used
        used += 1
        return rng.getrandbits(bits)

    starts = []
    rows = []
    for r in range(133):
        if 1 <= r <= 127:
            while draw(3) > 2:
                pass
        starts.append(used)
        rows.append([untemper(draw(32)) for _ in range(4)])
        if r <= 127:
            while draw(2) > 2:
                pass
    return starts, rows


def main():
    for seed, (expected_pos, expected_rank, expected_fixed) in CASES.items():
        starts, rows = simulate(seed)
        withheld = [temper(x) for x in rows[129]]
        rows[129] = []
        result = solve_target(rows, starts)
        assert starts[129] == expected_pos
        assert result["target_rank_after_source"] == expected_rank
        assert result["fixed_tempered_target_bits"] == expected_fixed
        for item in result["selected_words"]:
            mask = int(item["known_bit_mask"], 16)
            predicted = int(item["known_bit_value"], 16)
            assert withheld[item["word"]] & mask == predicted
        print("Synthetic two-selector PASS", "seed", seed, "target_index", starts[129],
              "target_rank", expected_rank, "fixed_bits", expected_fixed)


if __name__ == "__main__":
    main()
