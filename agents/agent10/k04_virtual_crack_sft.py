"""Original-source K04 virtual MT two-twist crack, selected spool row129 withheld.

Run: python agents/agent10/k04_virtual_crack_sft.py original-case.zip
Needs only Python stdlib and existing agent23 source parser.
Tests true indexed quartets against *unprinted* reconstructed state words,
screening each promising source match by exact chronological feasibility.
Reads no acceptance commitments, recovery mask, nonce or selected payload.
"""
import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_inverse_peel import groups, inverse_twist, rows

ALL = 0xFFFFFFFF
LOW = 0x7FFFFFFF
HIGH = 0x80000000
KEEP = 0xBFFFFFFF
A = 0x9908B0DF

QUADS = (
    ((4, 3), (35, 0), (58, 0), (118, 1)),
    ((5, 3), (36, 0), (59, 1), (119, 3)),
    ((9, 2), (40, 0), (63, 0), (124, 0)),
)


def twist(a, b):
    y = (a & HIGH) | (b & LOW)
    return ((y >> 1) ^ (A if y & 1 else 0)) & ALL


def phi(w):
    return twist(0, w) & KEEP


def source_groups(source, words):
    """Join the 42 authentic one-twist groups via three actual 31-bit quartets."""
    clusters = groups(source, words)
    parent = {root: root for root in clusters}
    displacement = {root: 0 for root in clusters}
    owner = {r: (root, offset)
             for root, entries in clusters.items() for r, offset in entries}

    def find(x):
        if parent[x] != x:
            p = parent[x]
            root = find(p)
            displacement[x] += displacement[p]
            parent[x] = root
        return parent[x]

    def join(a, b, distance):
        ra, rb = find(a), find(b)
        if ra == rb:
            assert displacement[b] - displacement[a] == distance
        else:
            parent[rb] = ra
            displacement[rb] = displacement[a] + distance - displacement[b]

    for q in QUADS:
        w = [words[r][j] for r, j in q]
        assert ((w[3] ^ w[2]) & KEEP) == (phi(w[0]) ^ phi(w[1]))
        (ar, aj) = q[0]
        owner_a, offset_a = owner[ar]
        for (br, bj), gap in zip(q[1:], (227, 396, 850)):
            owner_b, offset_b = owner[br]
            join(owner_a, owner_b, gap + aj - bj + offset_a - offset_b)

    combined = collections.defaultdict(list)
    for row, (root, offset) in owner.items():
        combined[find(root)].append((row, offset + displacement[root]))
    assert len(combined) == 75
    return combined


def infer_state(entries, words):
    observed = {}
    for row, offset in entries:
        for j, w in enumerate(words[row]):
            p = offset + j
            assert p not in observed or observed[p] == w
            observed[p] = w
    if not observed:
        return {}, {}
    states = {p: (ALL, w) for p, w in observed.items()}

    def put(p, mask, value):
        prev_mask, prev_value = states.get(p, (0, 0))
        assert not ((prev_value ^ value) & prev_mask & mask)
        new = (prev_mask | mask, prev_value | (value & mask))
        changed = new != (prev_mask, prev_value)
        states[p] = new
        return changed

    for _ in range(40):
        changed = 0
        for p in range(min(observed) - 624, max(observed) + 1):
            am, av = states.get(p, (0, 0))
            bm, bv = states.get(p + 1, (0, 0))
            cm, cv = states.get(p + 397, (0, 0))
            dm, dv = states.get(p + 624, (0, 0))
            if cm == dm == ALL:
                t = inverse_twist(cv ^ dv)
                changed += put(p, HIGH, t & HIGH)
                changed += put(p + 1, LOW, t & LOW)
            if (am & HIGH) and (bm & LOW) == LOW:
                value = twist(av, bv)
                if cm == ALL:
                    changed += put(p + 624, ALL, cv ^ value)
                if dm == ALL:
                    changed += put(p + 397, ALL, dv ^ value)
        if not changed:
            break
    else:
        raise AssertionError("state inference did not converge")
    return observed, states


def main(source):
    words = rows(source)
    assert len(words) == 133 and not words[129]
    clusters = source_groups(source, words)
    row_info = {row: (root, offset)
                for root, entries in clusters.items() for row, offset in entries}
    obs = []
    full_virtual = low_virtual = high_virtual = 0

    for root, entries in clusters.items():
        observed, states = infer_state(entries, words)
        if not observed:
            continue
        for pos, (mask, value) in states.items():
            if mask == HIGH:
                high_virtual += 1
                continue
            assert mask in (ALL, LOW)
            nearest = min(observed, key=lambda p: abs(p - pos))
            nearest_row = next(row for row, offset in entries
                              if any(offset + j == nearest for j in range(len(words[row]))))
            kind = "source" if pos in observed else ("full" if mask == ALL else "low31")
            if kind == "full":
                full_virtual += 1
            if kind == "low31":
                low_virtual += 1
            obs.append((root, pos, mask, value, nearest_row, kind))

    assert (full_virtual, low_virtual, high_virtual) == (81, 15, 30)
    assert len(obs) == 624

    # Graph constraints: row starts already indexed within each authentic source
    # group. The sole physical floor is four words per row, not metadata claims.
    edges = []
    for entries in clusters.values():
        r0, off0 = entries[0]
        for r, off in entries[1:]:
            gap = off - off0
            edges.extend(((r0, r, gap), (r, r0, -gap)))
    edges.extend((r + 1, r, -4) for r in range(132))

    def feasible(extra):
        distances = [0] * 133
        for _ in range(133):
            changed = False
            for a, b, gap in (*edges, *extra):
                if distances[b] > distances[a] + gap:
                    distances[b] = distances[a] + gap
                    changed = True
            if not changed:
                return True
        return False

    assert feasible(())

    def relation(a, b, gap):
        _, pa, _, _, ra, _ = a
        _, pb, _, _, rb, _ = b
        distance = gap + pa - row_info[ra][1] - pb + row_info[rb][1]
        return ((ra, rb, distance), (rb, ra, -distance))

    left = collections.defaultdict(list)
    count_left = 0
    for i, a in enumerate(obs):
        for j, b in enumerate(obs):
            if i == j or (a[0] == b[0] and b[1] - a[1] != 227):
                continue
            left[phi(a[3]) ^ phi(b[3])].append((i, j))
            count_left += 1

    count_right = matches = accepted = 0
    for i, c in enumerate(obs):
        if c[2] != ALL:
            continue
        for j, d in enumerate(obs):
            if i == j or d[2] != ALL:
                continue
            if c[0] == d[0] and d[1] - c[1] != 454:
                continue
            count_right += 1
            for ia, ib in left.get((c[3] ^ d[3]) & KEEP, ()):
                a, b = obs[ia], obs[ib]
                if len({(v[0], v[1]) for v in (a, b, c, d)}) != 4:
                    continue
                matches += 1
                if len({v[0] for v in (a, b, c, d)}) == 1:
                    continue
                constraints = (
                    *relation(a, b, 227),
                    *relation(a, c, 396),
                    *relation(a, d, 850),
                )
                if feasible(constraints):
                    accepted += 1
                    print("NEW_COHERENT_QUARTET", (a, b, c, d))

    assert count_left == 378988, count_left
    assert count_right == 361115, count_right
    assert matches == 70, matches
    assert accepted == 0, accepted
    print("ORIGINAL_SOURCE_42_WITNESSES 25+17")
    print("ORIGINAL_TWO_TWIST_ANCHORS", len(QUADS))
    print("SOURCE_WORDS 528 VIRTUAL_FULL", full_virtual, "LOW31", low_virtual,
          "HIGH_ONLY", high_virtual)
    print("A_B_PAIRS", count_left, "C_D_PAIRS", count_right)
    print("31_BIT_MATCHES", matches, "NEW_CHRONOLOGICALLY_FEASIBLE_LINKS", accepted)
    print("K04 coupon and K08 exact caption UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Pass the unchanged original H-17 case ZIP.")
    main(Path(sys.argv[1]))
