"""Sparse inverse for std::seed_seq with 1..4 32-bit inputs and n=624.

Source-independent construction and controls. An H-17 K04 claim still needs
independently indexed initialized-register words, historical producer/epoch
and output ordering, original selected print integrity, and mask integrity.
No original selected coupon, mask, SHA or final caption is read here.
"""
import random

N, P, Q = 624, 306, 317
MASK, INIT = 0xFFFFFFFF, 0x8B8B8B8B
MUL1, MUL2 = 1664525, 1566083941
INV1, INV2 = pow(MUL1, -1, 1 << 32), pow(MUL2, -1, 1 << 32)


def twist(x: int) -> int:
    return x ^ (x >> 27)


def generate(seeds: list[int]) -> list[int]:
    """Reference standard std::seed_seq::generate for 624 uint32 values."""
    s = len(seeds)
    assert 0 <= s <= 4
    a = [INIT] * N
    for k in range(N):
        r1 = MUL1 * twist(a[k] ^ a[(k + P) % N] ^ a[(k - 1) % N]) & MASK
        increment = s if k == 0 else k + seeds[k - 1] if k <= s else k
        r2 = (r1 + increment) & MASK
        a[(k + P) % N] = (a[(k + P) % N] + r1) & MASK
        a[(k + Q) % N] = (a[(k + Q) % N] + r2) & MASK
        a[k] = r2
    for k in range(N, 2 * N):
        j = k % N
        r3 = MUL2 * twist((a[j] + a[(j + P) % N] + a[(j - 1) % N]) & MASK) & MASK
        r4 = (r3 - j) & MASK
        a[(j + P) % N] ^= r3
        a[(j + Q) % N] ^= r4
        a[j] = r4
    return a


def required_indexes(s: int) -> list[int]:
    """Conservative dependency-closure sufficient positions, not minimal."""
    assert 1 <= s <= 4
    a = [1 << i for i in range(N)]
    for k in range(2 * N - 1, N - 1, -1):
        j = k % N
        r4 = a[j]
        a[(j + P) % N] |= r4
        a[(j + Q) % N] |= r4
        a[j] = r4 | a[(j + P) % N] | a[(j - 1) % N]
    deps = 0
    for k in range(N - 1, -1, -1):
        j = k % N
        r2 = a[j]
        r1 = r2 if k > s else a[(j + P) % N]
        if 0 < k <= s:
            deps |= r2 | r1
        a[(j + P) % N] |= r1
        a[(j + Q) % N] |= r2
        a[j] = r1 | a[(j + P) % N] | a[(j - 1) % N]
    return [i for i in range(N) if (deps >> i) & 1]


def add(a: int | None, b: int | None) -> int | None:
    return (a + b) & MASK if a is not None and b is not None else None


def sub(a: int | None, b: int | None) -> int | None:
    return (a - b) & MASK if a is not None and b is not None else None


def xor(a: int | None, b: int | None) -> int | None:
    return a ^ b if a is not None and b is not None else None


def undo_multiply(v: int | None, inv: int) -> int | None:
    return twist(v * inv & MASK) if v is not None else None


def recover(indexed: dict[int, int], s: int) -> list[int]:
    """Reverse both passes, allowing unknown state locations to be None."""
    a = [indexed.get(i) for i in range(N)]
    for k in range(2 * N - 1, N - 1, -1):
        j = k % N
        r4 = a[j]
        r3 = add(r4, j)
        a[(j + P) % N] = xor(a[(j + P) % N], r3)
        a[(j + Q) % N] = xor(a[(j + Q) % N], r4)
        a[j] = sub(sub(undo_multiply(r3, INV2), a[(j + P) % N]), a[(j - 1) % N])
    seeds: list[int | None] = [None] * s
    for k in range(N - 1, -1, -1):
        j = k % N
        r2 = a[j]
        r1 = sub(r2, j) if k > s else sub(a[(j + P) % N], INIT)
        if 0 < k <= s:
            seeds[k - 1] = sub(sub(r2, r1), j)
        a[(j + P) % N] = sub(a[(j + P) % N], r1)
        a[(j + Q) % N] = sub(a[(j + Q) % N], r2)
        a[j] = xor(xor(undo_multiply(r1, INV1), a[(j + P) % N]), a[(j - 1) % N])
    assert all(v is not None for v in seeds), "required indexed words missing"
    result = [int(v) for v in seeds]
    expected = generate(result)
    assert all(expected[i] == value for i, value in indexed.items())
    return result


def main() -> None:
    # Values taken from an independently compiled native C++17 std::seed_seq
    # executable with std::seed_seq::generate(array<uint32_t,624>).
    positions = (0, 1, 2, 3, 306, 317, 620, 621, 622, 623)
    golden = {
        (): (3499785500, 420997768, 1623516017, 553436518, 1177540569, 2873670211, 3339742712, 2040762813, 3516187490, 305717291),
        (1,): (464373425, 340098840, 3915870620, 1610178057, 737860653, 4096341009, 3682477225, 1454274101, 1418955045, 2284808618),
        (1, 2, 3, 4): (1894167914, 1272781218, 3735951414, 3882291241, 3116778833, 639307984, 2554835853, 4138801388, 3137129736, 1782067786),
    }
    for seeds, expected in golden.items():
        out = generate(list(seeds))
        assert tuple(out[i] for i in positions) == expected
    print("NATIVE_CPP_SEEDSEQ_GOLDEN_PASS", len(golden))

    rng = random.Random(0xA1717)
    for s in range(1, 5):
        indexes = required_indexes(s)
        for case in range(16):
            original = [rng.getrandbits(32) for _ in range(s)]
            output = generate(original)
            subset = {i: output[i] for i in indexes}
            assert recover(subset, s) == original, (s, case)
        print("SPARSE_INVERSE_PASS", "input_words", s, "needed_output_words", len(indexes),
              "trials", 16, "indexes", ",".join(map(str, indexes)))
    print("H17_AUTHENTICATED_TARGET_BITS_RECOVERED 0/128")


if __name__ == "__main__":
    main()
