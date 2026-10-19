"""H-17 K04: four-candidate five-word CPython numeric-seed recovery.

Reads only original SHA256-pinned intact spool via adjacent
k04_seven_residue_gate.py. Original selected ACK row129, masks,
acceptance commitments, K08 nonce and unchanged REC8 verifier are unread.

Usage: python agents/agent26/k04_n5_two_window_seed.py ORIGINAL_CASE_ZIP
"""
import itertools
import random
import sys

import k04_seven_residue_gate as core

MASK = core.M
TOP = 0x80000000


def four_seeds(early, late, phase):
    """Recover 158 of 160 key bits from two source-aligned seed-state windows."""
    (early_full, early_low31), (late_full, late_low31) = early, late
    observations = (
        (phase - 166, early_full[0], early_full[1], early_low31, False),
        (phase, late_full[0], late_full[1], late_full[2], True),
        (phase + 1, late_full[1], late_full[2], late_full[3], True),
        (phase + 2, late_full[2], late_full[3], late_full[4], True),
        (phase + 3, late_full[3], late_full[4], late_low31, False),
    )
    slots = [None] * 5
    for index, a, b, c, full in observations:
        assert 2 <= index <= 623
        residue = (index - 1) % 5
        assert slots[residue] is None, (phase, residue)
        term = core.seed_term(a, b, c, index)
        value = (term - residue) & MASK
        if full:
            slots[residue] = [value]
        else:
            value &= 0x7FFFFFFF
            slots[residue] = [value, value | TOP]
    assert all(item is not None for item in slots)
    return [
        sum(word << (32 * j) for j, word in enumerate(words))
        for words in itertools.product(*slots)
        if words[4] != 0
    ]


def synthetic_controls():
    passes = 0
    for phase in (396, 445, 535, 562, 563, 564, 565, 566, 567, 568, 600, 620):
        for trial in range(10):
            seed = sum(
                ((0x9A12376B + trial * 0x517 + j * 0x91E3F) & MASK) << (32 * j)
                for j in range(5)
            )
            rng = random.Random(seed)
            words = [
                core.untemper(rng.getrandbits(32))
                for _ in range(phase + 684)
            ]
            rows = {
                row: words[phase + offset:phase + offset + 4]
                for row, offset in core.POSITIONS.items()
            }
            early, late, _ = core.infer(rows)
            candidates = four_seeds(early, late, phase)
            assert len(candidates) == 4
            assert seed in candidates, (phase, trial)
            matches = [
                candidate for candidate in candidates
                if random.Random(candidate).getstate()[1][phase - 2:phase + 3]
                == tuple(late[0])
            ]
            assert matches == [seed], (phase, trial)
            passes += 1
    print('SYNTHETIC_POSITIVES_PASS', passes)


def original_source(zip_path):
    early, late, _ = core.infer(core.read_rows(zip_path))
    assert early[0] == [0x0A9DE247, 0xFBBBB07E]
    assert early[1] == 0x2A07F662
    assert late[0] == [
        0xB30BF870, 0x6CE0E225, 0xF4E8FCB2, 0xC517EB25, 0x7D3AAF35
    ]
    assert late[1] == 0x31FD69FC

    total = 0
    survivors = []
    for phase in range(396, 621):
        candidates = four_seeds(early, late, phase)
        assert len(candidates) == 4, phase
        total += len(candidates)
        matches = [
            candidate for candidate in candidates
            if list(random.Random(candidate).getstate()[1][:624])[phase - 2:phase + 3]
            == late[0]
        ]
        if phase in (564, 566):
            print('RESIDUAL_BOUNDARY_PHASE', phase,
                  'four_candidates', len(candidates), 'state_matches', len(matches))
        for seed in matches:
            survivors.append((phase, seed))
    assert not survivors, survivors
    assert total == 900
    print('ORIGINAL_FIRSTCYCLE_PHASES_EXCLUDED', 225, 'CANDIDATE_SEEDS_EXCLUDED', total)
    print('SOURCE_SHA256', core.SOURCE_SHA)
    print('ORIGINAL_SELECTED_ROW129_AND_ACCEPTANCE_UNREAD', True)
    print('K04_AND_K08_NOT_RECOVERED')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python k04_n5_two_window_seed.py original-case.zip')
    synthetic_controls()
    original_source(sys.argv[1])
