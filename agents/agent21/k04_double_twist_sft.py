"""Source-only K04 two-step MT recurrence and hidden DEST recovery (Agent 21).

Run: python agents/agent21/k04_double_twist_sft.py original-case.zip
No selected row129, K04/K08 commitments, route mask, or facility equipment used.
"""
import collections
import hashlib
import random
import re
import struct
import sys
import zipfile

SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
LOW = 0x7fffffff
MAG = 0x9908b0df
MASK = 0xbfffffff  # everything except the unknown predecessor MSB at bit 30


def untemper(y):
    x = y
    for shift, mask in ((18, None), (15, 0xefc60000), (7, 0x9d2c5680), (11, None)):
        for _ in range(6):
            x = y ^ (x >> shift if mask is None else ((x << shift) & mask))
        y = x
    return x & 0xffffffff


def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9d2c5680
    x ^= (x << 15) & 0xefc60000
    return (x ^ (x >> 18)) & 0xffffffff


def half(x):
    return ((x & LOW) >> 1) ^ (MAG if x & 1 else 0)


def sig(x, y):
    return (half(x) ^ half(y)) & MASK


def hidden_low31(middle, fourth, future):
    v = (fourth ^ future) ^ half(middle)
    odd = v >> 31
    return ((((v ^ (MAG if odd else 0)) & 0x3fffffff) << 1) | odd) & LOW


def read(path):
    with zipfile.ZipFile(path) as z:
        raw = z.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw).hexdigest() == SHA
    lines = [x for x in raw.decode("ascii").splitlines() if x.startswith("2026-")]
    assert len(lines) == 133
    words = [
        [untemper(w) for w in struct.unpack("<4I", bytes.fromhex(
            re.search(r"PAYLOAD=([A-F0-9]{32})", line).group(1)))]
        for line in lines
    ]
    words[129] = []  # selected ESC-N ACK2 withheld
    return lines, words


def search(words):
    items = [(r, j, x) for r, w in enumerate(words) for j, x in enumerate(w)]
    left = collections.defaultdict(list)
    for a, (r, j, u) in enumerate(items):
        for s, k, v in items[a + 1:]:
            if r < s:
                left[sig(u, v)].append(((r, j), (s, k)))
    hits = []
    for a, (r, j, u) in enumerate(items):
        for s, k, v in items[a + 1:]:
            if r < s:
                for first, second in left.get((u ^ v) & MASK, ()):
                    if second[0] < r:
                        hits.append((first, second, (r, j), (s, k)))
    return hits


def main(path):
    rng = random.Random(11445)
    x = [untemper(rng.getrandbits(32)) for _ in range(2500)]
    for t in range(15, 1350):
        a, b, c, d = (x[t + offset] for offset in (0, 227, 396, 850))
        assert ((c ^ d) & MASK) == sig(a, b)
        assert hidden_low31(b, c, d) == (a & LOW)
        assert untemper(temper(a)) == a
    print("synthetic two-step and inverse controls: 1335 PASS")
    lines, words = read(path)
    hits = search(words)
    assert len(hits) == 15, len(hits)
    a = ((9, 2), (40, 0), (63, 0), (124, 0))
    b = ((9, 3), (40, 1), (63, 1), (124, 1))
    assert a in hits and b in hits
    for q in (a, b):
        u, v, w, z = (words[row][col] for row, col in q)
        assert sig(u, v) == ((w ^ z) & MASK)
        print("original quartet", q, *(f"{n:08X}" for n in (u, v, w, z)))
    assert "DEST=store" in lines[9] and "CLASS=STORES" in lines[10]
    recovered = []
    for j, codes in ((2, (1, 3)), (3, (2, 0))):
        lo = hidden_low31(words[40][j], words[63][j], words[124][j])
        candidates = [(lo | (top << 31), temper(lo | (top << 31)) >> 30)
                      for top in (0, 1)]
        assert tuple(code for _, code in candidates) == codes
        recovered.append(candidates[1][0])
        print("row9 hidden word", j + 2, "low31", f"{lo:08X}", "code alternatives", candidates)
    assert [temper(w) >> 30 for w in recovered] == [3, 0]
    print("conditional reconstructed row9 states", *(f"{w:08X}" for w in recovered))
    print("row9 DEST sample: reject 3 then accept store 0")
    print("K04 selected coupon bits: 0; K08 exact recovered words: 0")


if __name__ == "__main__":
    main(sys.argv[1])
