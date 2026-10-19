"""K04 16-way completion of four consecutive MT outputs from two donor runs.

Positive controls use actual seeded CPython MT19937; no original source,
acceptance hash or disputed row129 is read. Applying this to real K04 requires
independently matched original donor arrays at the two ancestry windows.
"""
import hashlib
import random
import struct

MAGIC = 0x9908B0DF
BIT30_TEMPER_MASK = 0x44081102

def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9D2C5680
    x ^= (x << 15) & 0xEFC60000
    x ^= x >> 18
    return x & 0xFFFFFFFF

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
    return right(left(left(right(y, 18), 15, 0xEFC60000), 7, 0x9D2C5680), 11)

def recover_payloads(successor_low31, middle_full):
    """Sixteen potential little-endian 16-byte coupon payloads.

    Inputs: lower 31 state bits of X[p-623..p-620], and full untempered
    state words X[p-227..p-224]. Unknown predecessor high bits are the only
    remaining degrees of freedom in the MT recurrence for X[p..p+3].
    """
    assert len(successor_low31) == len(middle_full) == 4
    baseline = []
    for successor, middle in zip(successor_low31, middle_full):
        assert 0 <= successor < (1 << 31) and 0 <= middle < (1 << 32)
        state = middle ^ (successor >> 1) ^ (MAGIC if successor & 1 else 0)
        baseline.append(temper(state))
    candidates = []
    for predecessors in range(16):
        values = [value ^ (BIT30_TEMPER_MASK if (predecessors >> i) & 1 else 0)
                  for i, value in enumerate(baseline)]
        candidates.append(struct.pack("<4I", *values))
    assert len(set(candidates)) == 16
    return candidates

def main():
    assert temper(1 << 30) == BIT30_TEMPER_MASK
    for seed, offset in ((1, 625), (1234567, 900), (0xCAFEBABE, 1440)):
        r = random.Random(seed)
        state = [untemper(r.getrandbits(32)) for _ in range(offset + 4)]
        predecessor = [state[offset - 624 + i] for i in range(4)]
        successor = [state[offset - 623 + i] & 0x7FFFFFFF for i in range(4)]
        middle = [state[offset - 227 + i] for i in range(4)]
        candidates = recover_payloads(successor, middle)
        truth = struct.pack("<4I", *(temper(state[offset + i]) for i in range(4)))
        matching = [i for i, payload in enumerate(candidates)
                    if hashlib.sha256(payload).digest() == hashlib.sha256(truth).digest()]
        expected_index = sum(((p >> 31) & 1) << j for j, p in enumerate(predecessor))
        assert matching == [expected_index]
        print("PASS seed", seed, "offset", offset, "variant", expected_index, "/16")
    print("Three exact 16-way coupon completion controls PASS")

if __name__ == "__main__":
    main()
