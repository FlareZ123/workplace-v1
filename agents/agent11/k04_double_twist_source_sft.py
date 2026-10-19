"""Original K04 four-word double-twist witnesses and whole-spool target projection.

Usage: python agents/agent11/k04_double_twist_source_sft.py PATH_TO_ORIGINAL_ZIP
Source-only: selected spool row129, routing mask, commitments and REC8 checker unused.
SciPy is required by the existing Agent37 source-reader dependency.
"""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agents" / "agent33"))
sys.path.insert(0, str(ROOT / "agents" / "agent37"))
from k04_global_inverse_chronology_sft import source, twist
from k04_global_target_projection import source_rows, solve_target, untemper

MASK = 0xBFFFFFFF


def double_twist_matches(rows):
    words = [(r, j, value) for r, group in enumerate(rows) for j, value in enumerate(group)]
    earlier = defaultdict(list)
    for pos, (r, j, x) in enumerate(words):
        for rb, jb, y in words[pos + 1:]:
            if r < rb:
                earlier[(twist(0, x) ^ twist(0, y)) & MASK].append((r, j, rb, jb))
    matches = []
    for pos, (rc, jc, z) in enumerate(words):
        for rd, jd, w in words[pos + 1:]:
            if rc >= rd:
                continue
            for ra, ja, rb, jb in earlier[(z ^ w) & MASK]:
                if rb < rc:
                    matches.append((ra, ja, rb, jb, rc, jc, rd, jd))
    return sorted(matches)


def equality_graph_size(edges):
    parent = list(range(133))
    offset = [0] * 133

    def root(x):
        if parent[x] != x:
            y = parent[x]
            parent[x] = root(y)
            offset[x] += offset[y]
        return parent[x]

    for a, b, difference in edges:
        ra, rb = root(a), root(b)
        if ra == rb:
            assert offset[b] - offset[a] == difference
        else:
            parent[rb] = ra
            offset[rb] = offset[a] + difference - offset[b]
    return len({root(r) for r in range(133)})


def main(original_zip):
    rows, within, boundary = source(str(original_zip))
    assert (len(within), len(boundary)) == (25, 17)
    old_edges = []
    for (a, i), (b, j), (c, k) in within:
        old_edges.extend(((a, b, 397 + i - j), (a, c, 624 + i - k)))
    for a, bit, (b, j), (c, k) in boundary:
        old_edges.extend(((a, b, 396 - j), (a, c, 623 - k)))
    assert equality_graph_size(old_edges) == 84

    matches = double_twist_matches(rows)
    assert len(matches) == 15
    for required in (
        (4, 3, 35, 0, 58, 0, 118, 1),
        (5, 3, 36, 0, 59, 1, 119, 3),
        (9, 2, 40, 0, 63, 0, 124, 0),
        (9, 3, 40, 1, 63, 1, 124, 1),
    ):
        assert required in matches

    edges = list(old_edges)
    for a, i, b, j, c, k, d, ell in matches:
        edges.extend(((a, b, 227 + i - j),
                      (a, c, 396 + i - k),
                      (a, d, 850 + i - ell)))
    assert equality_graph_size(edges) == 75

    generator = random.Random(102938)
    source_state = [untemper(generator.getrandbits(32)) for _ in range(1200)]
    for t in range(300):
        parity = (source_state[t + 851] ^ source_state[t + 397]
                  ^ twist(0, source_state[t + 1])
                  ^ twist(0, source_state[t + 228]))
        assert parity & MASK == 0

    indexed = json.loads((ROOT / "results" / "h17-k04-source-consistent-index955.json").read_text(encoding="utf-8"))
    starts = indexed["row_starts"]
    compact = json.dumps(starts, separators=(",", ":")).encode("ascii")
    assert len(starts) == 133
    assert hashlib.sha256(compact).hexdigest() == "1635d1a4e4e9d8e5b33c11464061f16323de0e284bed8ba6ce2195de04701edf"
    result = solve_target(source_rows(original_zip), starts)
    assert result["source_rank"] == 15305
    assert result["target_rank_after_source"] == 128
    assert result["fixed_tempered_target_bits"] == 0
    print("PASS: 300 synthetic double-twist identities, 15 original four-word matches,")
    print("original equality groups 84 to 75; full original state equations consistent.")
    print("K04 selected output: 128/128 bits still undetermined; zero coupon bits recovered.")
    print("No original REC8 commitment or disputed spool row129 was consulted.")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
