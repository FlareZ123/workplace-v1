"""Source-only K04 target-leverage atlas. Agent41, 19 October 2026.

Run from a repository checkout. Python 3 stdlib; selected printer row129,
K04 mask, acceptance hashes and verifier are never consumed as evidence.
"""
from collections import Counter
from hashlib import sha256
from pathlib import Path

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
G43 = {12: -229, 43: 0, 66: 167, 96: 393, 128: 623}
G44 = {13: -227, 44: 0, 67: 168, 97: 394, 130: 620, 131: 624}
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


def add(basis, v):
    while v:
        k = v.bit_length() - 1
        w = basis.get(k)
        if w is None:
            basis[k] = v
            return
        v ^= w


def symbol_stream(last=929):
    # Relative index -229 is origin; 624 words are independent GF(2) variables.
    a = [[1 << (32*i+j) for j in range(32)] for i in range(624)]
    for i in range(624, last+1):
        old, nxt, middle = a[i-624], a[i-623], a[i-227]
        mixed = [nxt[j+1] for j in range(30)] + [old[31], 0]
        a.append([middle[j] ^ mixed[j] ^ (nxt[0] if (MATRIX >> j) & 1 else 0)
                  for j in range(32)])
    return a


def base_for_shift(symbols, d):
    b = {}
    for pos in G43.values():
        for j in range(4):
            for v in symbols[pos+229+j]:
                add(b, v)
    for pos in G44.values():
        for j in range(4):
            for v in symbols[pos+d+229+j]:
                add(b, v)
    return b


def gain(base, target, vectors):
    a, b = base.copy(), target.copy()
    for v in vectors:
        add(a, v)
        add(b, v)
    return (len(a)-len(base)) - (len(b)-len(target))


def tempered_vectors(x):
    return [sum_xor(x[k] for k in range(32) if (temper(1 << k) >> j) & 1)
            for j in range(32)]


def sum_xor(vectors):
    result = 0
    for value in vectors:
        result ^= value
    return result


def window(symbols, t, n=4, kind="full"):
    out = []
    for i in range(n):
        x = symbols[t+229+i]
        if kind == "low31":
            x = x[:31]
        elif kind == "high16":
            x = tempered_vectors(x)[16:]
        elif kind == "top3":
            x = tempered_vectors(x)[29:]
        out.extend(x)
    return out


def main():
    source = Path(__file__).resolve().parents[2] / "resources/evidence/print/spool-reconstruction.log"
    raw = source.read_bytes()
    assert sha256(raw).hexdigest() == SPOOL_SHA
    rows = [r for r in raw.decode("ascii").splitlines() if "PAYLOAD=" in r]
    assert len(rows) == 133
    rows[129] = "[WITHHELD]"
    assert 129 not in G43 and 129 not in G44
    assert all(temper(untemper(x)) == x for x in (0, 1, 0xABCDEF01, 0xFFFFFFFF))

    S = symbol_stream()
    # Independent synthetic CPython recurrence control for the symbolic model.
    from random import Random
    rng = Random(1729)
    words = [untemper(rng.getrandbits(32)) for _ in range(930)]
    initial = sum(1 << i for i in range(624*32)
                  if (words[i//32] >> (i%32)) & 1)
    for t in (624, 627, 801, 929):
        value = sum((1 << j) for j in range(32)
                    if (S[t][j] & initial).bit_count() & 1)
        assert value == words[t], (t, value, words[t])

    hits = Counter()
    nplacements = 0
    for d in range(11, 66):
        base = base_for_shift(S, d)
        assert len(base) == 1123
        for p in range(627, d+617):
            nplacements += 1
            with_target = base.copy()
            for v in window(S, p, 4):
                add(with_target, v)
            assert len(with_target)-len(base) == 128
            for t in range(-229, 701):
                if p <= t <= p+3:
                    continue
                g = gain(base, with_target, S[t+229])
                if g:
                    hits[(p, t, g)] += 1

    assert nplacements == 1540
    assert hits == {(627, 400, 1): 55}, hits
    base = base_for_shift(S, 11)
    with_target = base.copy()
    for v in window(S, 627, 4):
        add(with_target, v)
    def g(a, b):
        return gain(base, with_target, window(S, 4, 4, a) + window(S, 400, 4, b))
    assert gain(base, with_target, window(S, 4)) == 0
    assert gain(base, with_target, window(S, 400)) == 1
    assert (g("full", "full"), g("low31", "low31"),
            g("high16", "high16"), g("top3", "top3")) == (128, 121, 1, 0)
    assert gain(base, with_target, window(S, 400, 1, "high16")) == 0

    print("PASS: synthetic recurrence; 1540 source placements; source rank 1123; K04 target rank 128")
    print("Off-target full-word positive probes (p,t,gain):", dict(hits))
    print("At d=11,p=627: windows t4..7 and t400..403 jointly: full=128, low31=121, high16=1, top3=0")
    print("Original K04/K08 acceptance commitments, K04 mask and row129 payload withheld")


if __name__ == "__main__":
    main()
