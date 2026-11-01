"""Exact conditional K04 native-output donor-bit relations (read-only SFT).

Usage: python agents/agent26/k04_native_donor_direct_bit_sft.py case.zip
Never reads disputed spool row129, the K04 commitment or the copied ACK.
"""
import random
import sys
import zipfile
from itertools import combinations

MASK = 0xFFFFFFFF
EARLY = {0: (1, 4, 22), 4: (1, 5, 19), 22: (1, 19, 23)}


def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9D2C5680
    x ^= (x << 15) & 0xEFC60000
    x ^= x >> 18
    return x & MASK


def undo_right(x, shift):
    y = x
    for _ in range(6):
        y = x ^ (y >> shift)
    return y & MASK


def undo_left(x, shift, mask):
    y = x
    for _ in range(6):
        y = x ^ ((y << shift) & mask)
    return y & MASK


def untemper(x):
    x = undo_right(x, 18)
    x = undo_left(x, 15, 0xEFC60000)
    x = undo_left(x, 7, 0x9D2C5680)
    return undo_right(x, 11)


def twist(a, b):
    x = ((a & 0x80000000) | (b & 0x7FFFFFFF)) >> 1
    return x ^ (0x9908B0DF if b & 1 else 0)


def bit(x, j):
    return (x >> j) & 1


def coupon_bit(j, early, middle):
    v = bit(middle, j)
    for k in EARLY[j]:
        v ^= bit(early, k)
    return v


def main(filename):
    assert all(temper(untemper(1 << j)) == 1 << j for j in range(32))
    # Complete GF(2) certificate, since twist+temper is linear in three words.
    triples = [(0, 0, 0)]
    for k in range(3):
        for j in range(32):
            words = [0, 0, 0]
            words[k] = 1 << j
            triples.append(tuple(words))
    for a, b, c in triples:
        target = temper(c ^ twist(a, b))
        for j in EARLY:
            assert bit(target, j) == coupon_bit(j, temper(b), temper(c))
    assert len(triples) == 97
    print("97 / 97 complete basis witnesses PASS")

    # Enumerate the 32 direct selected output-bit dependencies on the
    # first latent 32-bit printed output, with the other donor bit at j.
    support = {}
    for j in range(32):
        support[j] = tuple(k for k in range(32)
                           if bit(temper(twist(0, untemper(1 << k))), j))
    min_single = min(1 + len(v) for v in support.values())
    winners = [(j, v) for j, v in support.items() if len(v) + 1 == min_single]
    assert min_single == 4 and winners == list(EARLY.items())
    print("Minimum donor bits for one direct selected bit: 4", winners)
    for width, expected in ((2, 6), (3, 9)):
        cost, indices = min((width + len(set().union(
            *(set(support[j]) for j in indices))), indices)
            for indices in combinations(range(32), width))
        assert cost == expected, (cost, indices)
        print("Minimum donor bits for", width, "direct selected bits:", cost, indices)

    # Source only: row43 is an intact 10:35 label. Never read row129.
    with zipfile.ZipFile(filename) as z:
        rows = z.read("evidence/print/spool-reconstruction.log").decode().splitlines()
    row43 = next(line for line in rows if "JOB=PS-261003-0343 " in line)
    payload = row43.split("PAYLOAD=")[1].split()[0]
    assert untemper(int.from_bytes(bytes.fromhex(payload)[12:16], "little")) == 0x59E4D0B9
    print("Original row43.word3 state witness verified")

    count = 0
    for seed in (0, 17, 20261003, 314159, 0xC0FFEE):
        rng = random.Random(seed)
        native = [rng.getrandbits(32) for _ in range(960)]
        for p in range(950, 956):
            for j in EARLY:
                assert bit(native[p], j) == coupon_bit(
                    j, native[p-623], native[p-227])
            count += 1
    print(count, "/", count, "genuine seeded MT chronology controls PASS")
    print("Hypothetical donor observations only; K04 remains unknown")


if __name__ == "__main__":
    main(sys.argv[1])
