"""Agent41: reconstruct an H-17 K04 16-byte coupon from two source-indexed
four-word MT19937 low31 ancestor runs plus the intact row43 word3.

Conditional source model d=11,p=627. Original selected row129 is never read.
Synthetic SFT enumerates 2^7=128 coupon hypotheses with an unchanged SHA256.
"""
from hashlib import sha256
from random import Random

MATRIX = 0x9908B0DF


def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9D2C5680
    x ^= (x << 15) & 0xEFC60000
    return (x ^ (x >> 18)) & 0xFFFFFFFF


def untemper(y):
    x = y ^ (y >> 18)
    x ^= (x << 15) & 0xEFC60000
    z = x
    for _ in range(5):
        z = x ^ ((z << 7) & 0x9D2C5680)
    x = z
    for _ in range(3):
        z = x ^ (z >> 11)
    return z & 0xFFFFFFFF


def twist(a, b):
    x = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return (x >> 1) ^ (MATRIX if b & 1 else 0)


def recover(x3, early_low31, late_low31, mask, expected_sha256):
    """Enumerate the seven relevant missing state high bits.

    early_low31: X[4], X[5], X[6], X[7], each masked by 0x7fffffff.
    late_low31: X[400], X[401], X[402], X[403] similarly.
    x3: original full untempered printer row43 final payload word.
    Each hit is (16-byte uppercase coupon hex, 7-bit high-state assignment).
    """
    assert len(early_low31) == len(late_low31) == 4
    assert all(0 <= v <= 0x7FFFFFFF for v in early_low31 + late_low31)
    assert len(mask) == 16 and len(expected_sha256) == 32
    matches = []
    for bits in range(128):
        ea = [v | (((bits >> i) & 1) << 31)
              for i, v in enumerate(early_low31[:3])]
        ea.append(early_low31[3])  # Top bit X[7] irrelevant to target.
        lb = [v | (((bits >> (i+3)) & 1) << 31)
              for i, v in enumerate(late_low31)]
        values = [lb[j] ^ twist(x3 if j == 0 else ea[j-1], ea[j])
                  for j in range(4)]
        payload = b"".join(temper(x).to_bytes(4, "little") for x in values)
        coupon = bytes(a ^ b for a, b in zip(payload, mask))
        if sha256(coupon).digest() == expected_sha256:
            matches.append((coupon.hex().upper(), bits))
    return matches


def main():
    rng = Random(20261019)
    words = [untemper(rng.getrandbits(32)) for _ in range(635)]
    original_payload = b"".join(temper(w).to_bytes(4, "little")
                                for w in words[627:631])
    mask = bytes.fromhex("8556C8CB6140A7F9A5123AC7571BEE1C")
    expected_coupon = bytes(a ^ b for a, b in zip(original_payload, mask))
    expected = sha256(expected_coupon).digest()
    early = [x & 0x7FFFFFFF for x in words[4:8]]
    late = [x & 0x7FFFFFFF for x in words[400:404]]
    hits = recover(words[3], early, late, mask, expected)
    assert len(hits) == 1 and hits[0][0] == expected_coupon.hex().upper()
    true_bits = sum(((words[4+i] >> 31) & 1) << i for i in range(3))
    true_bits |= sum(((words[400+i] >> 31) & 1) << (i+3)
                     for i in range(4))
    assert hits[0][1] == true_bits
    assert recover(words[3], early, late, mask, bytes(32)) == []
    print("PASS: exact 128-branch K04 completion from eight low31 states")
    print("PASS: synthetic true masked 16-byte coupon recovered by original SHA256 method")
    print("PASS: seven missing high bits enumerated, X[7] top bit unnecessary")
    print("Original selected row129 never used; no original K04 acceptance claimed")


if __name__ == "__main__":
    main()
