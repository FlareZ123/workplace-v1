"""Source-only K04 scalar MT19937 seeding gate.

Run from the repository: python agents/agent22/k04_scalar_mt_seed_gate.py CASE.zip
Uses Agent1's source-pinned five-pair extractor and no selected row129,
route mask, verifier, commitment, nonce or K08 candidate.
"""
import hashlib
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent1"))
from k04_python_seed_fragments import extract_pairs, initial_words

MASK = 0xFFFFFFFF
MULTIPLIER = 1812433253
SPOOL_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def scalar_seed_state(seed):
    state = [seed & MASK]
    for i in range(1, 624):
        predecessor = state[-1]
        state.append((MULTIPLIER * (predecessor ^ (predecessor >> 30)) + i) & MASK)
    return state


def first_twist(initial):
    state = initial.copy()
    for i in range(624):
        y = (state[i] & 0x80000000) | (state[(i + 1) % 624] & 0x7FFFFFFF)
        state[i] = (state[(i + 397) % 624] ^ (y >> 1) ^
                    (0x9908B0DF if y & 1 else 0)) & MASK
    return state


def implied_seed_indices(initialized_words):
    return [
        (next_word -
         MULTIPLIER * (previous ^ (previous >> 30))) & MASK
        for previous, next_word in zip(initialized_words, initialized_words[1:])
    ]


def synthetic_controls():
    count = 0
    for seed in [0, 5489, 0xDEADBEEF, 0xFFFFFFFF]:
        initialized = scalar_seed_state(seed)
        outputs = first_twist(initialized)
        for t in [0, 38, 227, 392]:
            samples = [(outputs[t + j], outputs[t + j + 227])
                       for j in range(5)]
            reconstruction = initial_words(samples)
            assert reconstruction == initialized[t + 228:t + 232]
            assert implied_seed_indices(reconstruction) == [t + 229, t + 230, t + 231]
            count += 1
    print("scalar_seed_synthetic_PASS", count)


def main(archive):
    synthetic_controls()
    with zipfile.ZipFile(archive) as source:
        actual = hashlib.sha256(
            source.read("evidence/print/spool-reconstruction.log")).hexdigest()
        assert actual == SPOOL_SHA256, "Original printer-source SHA mismatch"
    group3, _, _, _ = extract_pairs(Path(archive))
    assert len(group3) == 5
    initialized = initial_words(group3)
    assert initialized == [
        0x6CE0E225, 0xF4E8FCB2, 0xC517EB25, 0x7D3AAF35
    ]
    implied = implied_seed_indices(initialized)
    assert implied == [1211007102, 3776610384, 2011796279]
    assert all(index > 623 for index in implied)
    print("source_initial_state_words", " ".join(f"{word:08X}" for word in initialized))
    print("scalar_seed_implied_indices", implied)
    print("single_scalar_init_genrand_32bit_first_twist_NO_MATCH")
    print("later_twists_and_seed_sequence_UNTESTED")
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python agents/agent22/k04_scalar_mt_seed_gate.py original-case.zip")
    main(sys.argv[1])
