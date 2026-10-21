"""Conditional K04 standard MT19937 direct uint32 initializer exclusion.

Source: results/h17-k04-fiveword-cpython-firstcycle-complete-exclusion.md.
The consecutive source-inferred pre-twist initialized-state words are assumed
to lie at S[p], S[p+1] with p in 396..621. This historical source alignment
is unverified. The selected coupon, mask and acceptance hashes are unused.

This excludes only direct init_genrand(uint32) initial-cycle seed states.
It does not exclude seed_seq, later cycles, or an alternate historical producer.
"""

F = 1812433253
MASK = 0xFFFFFFFF
INVERSE_F = pow(F, -1, 1 << 32)
S_P = 0xF4E8FCB2
S_P1 = 0xC517EB25


def forward(previous: int, index: int) -> int:
    return (F * (previous ^ (previous >> 30)) + index) & MASK


def backward(current: int, index: int) -> int:
    mixed = ((current - index) * INVERSE_F) & MASK
    return mixed ^ (mixed >> 30)


def main() -> None:
    seeds = (0, 1, 5489, 8131, 1791050460, 0xFFFFFFFF)
    for seed in seeds:
        states = [seed]
        for index in range(1, 624):
            states.append(forward(states[-1], index))
        for index in (1, 32, 396, 564, 621, 623):
            assert backward(states[index], index) == states[index - 1]
        assert states[-1] == forward(states[-2], 623)
        print(f"synthetic seed {seed}: PASS")

    implied_index = (S_P1 - F * (S_P ^ (S_P >> 30))) & MASK
    predicted_indices = range(397, 623)
    matches = [index for index in predicted_indices if forward(S_P, index) == S_P1]
    assert implied_index == 3776610384
    assert not matches
    print(f"original source-pair implied initializer index: {implied_index}")
    print(f"allowed first-cycle indices: {predicted_indices.start}..{predicted_indices.stop - 1}")
    print(f"original-source matches: {len(matches)} / {len(predicted_indices)}; STOP")


if __name__ == "__main__":
    main()

