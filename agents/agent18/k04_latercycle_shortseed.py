"""Independent later-cycle CPython integer seed test using two AX-7778 state windows.

The six source-derived words are from:
results/h17-k04-AX7778-cross-cycle-seed-window.md (Agent 9).
They are conditional on the shared MT stream, recorder prefix and first-cycle
row34-state interpretation, with absolute row34 phase p=535..621.

No row129 bytes, REC8 commitments, K04 mask, or K08 phrase are read.
Run: python agents/agent18/k04_latercycle_shortseed.py
"""
import random

MASK = 0xFFFFFFFF
INITIAL = [19650218]
for index in range(1, 624):
    previous = INITIAL[-1]
    INITIAL.append(
        (1812433253 * (previous ^ (previous >> 30)) + index) & MASK
    )


def seed_word(a, b, c, index):
    prior = ((b + index - 1) ^ ((a ^ (a >> 30)) * 1566083941)) & MASK
    current = ((c + index) ^ ((b ^ (b >> 30)) * 1566083941)) & MASK
    return (
        current
        - (INITIAL[index] ^ ((prior ^ (prior >> 30)) * 1664525))
    ) & MASK


def recover_key(source_quartet, phase, word_count):
    recovered = {}
    for offset in (2, 3):
        state_index = phase - 1 + offset
        key_index = (state_index - 1) % word_count
        key_word = (
            seed_word(
                *source_quartet[offset - 2 : offset + 1],
                state_index,
            )
            - key_index
        ) & MASK
        if key_index in recovered and recovered[key_index] != key_word:
            return None
        recovered[key_index] = key_word
    if len(recovered) != word_count:
        return None
    return sum(recovered[index] << (32 * index) for index in range(word_count))


def initial_state(seed):
    return random.Random(seed).getstate()[1][:624]


def main():
    controls = 0
    for phase in (535, 555, 584, 605, 621):
        for word_count, seed in (
            (1, 0xA12F6B35),
            (2, 0xBB103344A12F6B35),
        ):
            state = initial_state(seed)
            assert recover_key(
                state[phase - 1 : phase + 3], phase, word_count
            ) == seed
            controls += 1
    assert controls == 10
    print("synthetic_controls_PASS", controls)

    early = (0x0A9DE247, 0xFBBBB07E)  # S[p-168:p-166]
    late = (0x6CE0E225, 0xF4E8FCB2, 0xC517EB25, 0x7D3AAF35)
    for word_count in (1, 2):
        compatible_quartets = 0
        heldout_matches = 0
        for phase in range(535, 622):
            seed = recover_key(late, phase, word_count)
            if seed is None:
                continue
            state = initial_state(seed)
            if tuple(state[phase - 1 : phase + 3]) != late:
                continue
            compatible_quartets += 1
            if tuple(state[phase - 168 : phase - 166]) == early:
                heldout_matches += 1
        print(
            "seed_words", word_count,
            "phases", 87,
            "quartet_matches", compatible_quartets,
            "heldout_matches", heldout_matches,
        )
        assert (compatible_quartets, heldout_matches) == (0, 0)
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    main()
