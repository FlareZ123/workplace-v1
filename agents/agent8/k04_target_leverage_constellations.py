"""K04 MT19937 target-leverage atlas; source-heldout, no original checks required.

Run: python k04_target_leverage_constellations.py
Model: Agent49 two original printer groups, MT19937 recurrence, and target
row129 at positions p=627..d+616 for group shift d=11..65.
"""
from collections import Counter, defaultdict
from random import Random

BASE, END, MAGIC = -229, 1700, 0x9908B0DF

def add(basis, vector):
    while vector:
        pivot = vector.bit_length() - 1
        previous = basis.get(pivot)
        if previous is None:
            basis[pivot] = vector
            return
        vector ^= previous

def expressions():
    words = [[1 << (32 * i + bit) for bit in range(32)] for i in range(624)]
    for i in range(END - BASE + 1 - 624):
        first, second, middle = words[i], words[i + 1], words[i + 397]
        words.append([
            middle[bit]
            ^ (first[31] if bit == 30 else second[bit + 1] if bit < 30 else 0)
            ^ (second[0] if (MAGIC >> bit) & 1 else 0)
            for bit in range(32)
        ])
    return words

def temper_bits(bits):
    a = [bits[i] ^ (bits[i + 11] if i + 11 < 32 else 0) for i in range(32)]
    b = [a[i] ^ (a[i - 7] if i >= 7 and (0x9D2C5680 >> i) & 1 else 0)
         for i in range(32)]
    c = [b[i] ^ (b[i - 15] if i >= 15 and (0xEFC60000 >> i) & 1 else 0)
         for i in range(32)]
    return [c[i] ^ (c[i + 18] if i + 18 < 32 else 0) for i in range(32)]

def source_basis(words, shift):
    starts = (-229, 0, 167, 393, 623,
              shift - 227, shift, shift + 168,
              shift + 394, shift + 620, shift + 624)
    basis = {}
    for start in starts:
        for pos in range(start, start + 4):
            for vector in words[pos - BASE]:
                add(basis, vector)
    return basis

def target_gain(words, known, known_target, observations):
    b0, b1 = known.copy(), known_target.copy()
    for pos, kind in observations:
        bits = words[pos - BASE]
        if kind == "high16":
            bits = temper_bits(bits)[16:]
        elif kind == "low31":
            bits = bits[:31]
        for vector in bits:
            add(b0, vector)
            add(b1, vector)
    return (len(b0) - len(known)) - (len(b1) - len(known_target))

def untemper(y):
    def right(value, shift):
        x = value
        for _ in range(32 // shift + 1):
            x = value ^ (x >> shift)
        return x & 0xFFFFFFFF
    def left(value, shift, mask):
        x = value
        for _ in range(32 // shift + 1):
            x = value ^ ((x << shift) & mask)
        return x & 0xFFFFFFFF
    y = right(y, 18)
    y = left(y, 15, 0xEFC60000)
    y = left(y, 7, 0x9D2C5680)
    return right(y, 11)

def controls():
    rng = Random(0xDEADBEEF123456789)
    actual = [untemper(rng.getrandbits(32)) for _ in range(1600)]
    for i in range(976):
        pair = (actual[i] & 0x80000000) | (actual[i + 1] & 0x7FFFFFFF)
        expect = actual[i + 397] ^ (pair >> 1)
        if actual[i + 1] & 1:
            expect ^= MAGIC
        assert actual[i + 624] == expect & 0xFFFFFFFF
    for value in (0, 1, 0x80000000, 0x12345678, 0xDEADBEEF):
        vectors = temper_bits([1 << i for i in range(32)])
        symbolic = sum(1 << i for i, bits in enumerate(vectors)
                       if (bits & value).bit_count() % 2)
        y = value ^ (value >> 11)
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        assert symbolic == y & 0xFFFFFFFF

def main():
    controls()
    words = expressions()
    histogram = defaultdict(Counter)
    placements = target_words = 0
    for shift in range(11, 66):
        lower, upper = 627, shift + 616
        placements_to_check = sorted({lower, (lower + upper) // 2, upper})
        known = source_basis(words, shift)
        assert len(known) == 1123
        for p in placements_to_check:
            known_target = known.copy()
            for q in range(p, p + 4):
                for vector in words[q - BASE]:
                    add(known_target, vector)
            assert len(known_target) - len(known) == 128
            placements += 1
            for q in range(p, p + 4):
                a, b, c = q - 624, q - 623, q - 227
                recipes = {
                    "three full ancestral words": [(i, "full") for i in (a, b, c)],
                    "three tempered upper halfwords": [(i, "high16") for i in (a, b, c)],
                    "three untempered low31 controls": [(i, "low31") for i in (a, b, c)],
                    "low31 successor + tempered high16 middle": [(b, "low31"), (c, "high16")],
                    "full predecessor + low31 successor + high16 middle":
                        [(a, "full"), (b, "low31"), (c, "high16")],
                    "two complete future recurrence words": [(q + 397, "full"), (q + 624, "full")],
                }
                for label, obs in recipes.items():
                    histogram[label][target_gain(words, known, known_target, obs)] += 1
                target_words += 1
    print("Synthetic seeded MT recurrence + symbolic temper controls: PASS")
    print("Placements:", placements, "target-word probes:", target_words)
    for label, counts in histogram.items():
        print(label, dict(sorted(counts.items())))
    expected = {
        "three full ancestral words": {32: 648},
        "three tempered upper halfwords": {0: 593, 1: 55},
        "three untempered low31 controls": {30: 593, 31: 55},
        "low31 successor + tempered high16 middle": {15: 593, 16: 55},
        "full predecessor + low31 successor + high16 middle": {16: 648},
        "two complete future recurrence words": {1: 162, 32: 486},
    }
    assert placements == 162 and target_words == 648
    for label, counts in expected.items():
        assert histogram[label] == Counter(counts)
    print("All target-leverage assertions: PASS")

if __name__ == "__main__":
    main()
