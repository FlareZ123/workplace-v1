"""ACK-stage-aware MT word-placement constraints for H-17's unresolved K04.

Reads only original printer source. Selected ACK payload r129 is never decoded,
and no mask, acceptance commitment or verifier is consulted. This is a necessary
chronology certificate, not an authenticated printer model or recovered coupon.
"""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
from random import Random
import re

ROOT = Path(__file__).resolve().parents[2]
SPOOL = ROOT / "resources/evidence/print/spool-reconstruction.log"
EXPECTED_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MAX32 = (1 << 32) - 1
TARGET = 129
REQUESTED = {128, 130}


def undo_right(y: int, shift: int) -> int:
    x = y
    for _ in range(6):
        x = (y ^ (x >> shift)) & MAX32
    return x


def undo_left(y: int, shift: int, mask: int) -> int:
    x = y
    for _ in range(6):
        x = (y ^ ((x << shift) & mask)) & MAX32
    return x


def untemper(y: int) -> int:
    return undo_right(
        undo_left(undo_left(undo_right(y, 18), 15, 0xEFC60000), 7, 0x9D2C5680),
        11,
    )


def twist(a: int, b: int) -> int:
    x = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return ((x >> 1) ^ (0x9908B0DF if x & 1 else 0)) & MAX32


def parse_ack_words() -> dict[int, tuple[int, ...]]:
    raw = SPOOL.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_SHA
    lines = [line for line in raw.decode("ascii").splitlines() if " PAYLOAD=" in line]
    assert len(lines) == 133
    words = {}
    for i, line in enumerate(lines):
        is_ack = " STATE=ACK " in line
        assert is_ack == (i not in REQUESTED)
        if i in REQUESTED or i == TARGET:
            continue  # No REQUESTED payload and no selected ACK payload read.
        match = re.search(r"PAYLOAD=([0-9A-F]{32})\b", line)
        assert match is not None
        data = bytes.fromhex(match.group(1))
        chunks = [data[j:j + 4] for j in range(0, 16, 4)]
        words[i] = tuple(untemper(int.from_bytes(chunk, "little"))
                         for chunk in reversed(chunks))
    assert len(words) == 130
    return words


def source_triples(words: dict[int, tuple[int, ...]]) -> list[tuple[int, ...]]:
    by_value = defaultdict(list)
    for row, values in words.items():
        for word, value in enumerate(values):
            by_value[value].append((row, word))
    hits = []
    for a in range(128):
        for aw in range(3):
            t = twist(words[a][aw], words[a][aw + 1])
            for b in range(a + 1, 128):
                for bw, value in enumerate(words[b]):
                    for c, cw in by_value.get(t ^ value, ()):
                        if c > b:
                            hits.append((a, aw, b, bw, c, cw))
    assert len(hits) == 21
    assert sum(c < 128 for *_, c, cw in hits) == 19
    assert sum(c >= 128 for *_, c, cw in hits) == 2
    return hits



def boundary_triples(words: dict[int, tuple[int, ...]]) -> list[tuple[int, ...]]:
    """Source-only 31-bit MT recurrence when hidden X[t] precedes a row.

    X[t+624] XOR X[t+397] and twist(X[t], X[t+1]) share 31
    observable bits when X[t+1] is the row's first serialized word.
    The unknown preceding X[t].MSB only controls bit 30.
    """
    keep = 0xBFFFFFFF
    masked_values = defaultdict(list)
    for row, values in words.items():
        for word, value in enumerate(values):
            masked_values[value & keep].append((row, word))
    hits = []
    for a in range(128):
        signature = twist(0, words[a][0]) & keep
        for b in range(a + 1, 128):
            for bw, value in enumerate(words[b]):
                for c, cw in masked_values.get((signature ^ value) & keep, ()):
                    if c > b:
                        hits.append((a, b, bw, c, cw))
    assert hits == [
        (21, 74, 2, 105, 1),
        (22, 75, 2, 106, 2),
        (39, 93, 3, 123, 1),
    ]
    return hits


def boundary_edges(hits: list[tuple[int, ...]]) -> list[tuple[int, int, int]]:
    edges = []
    for a, b, bw, c, cw in hits:
        for first, last, delta in (
            (a, b, 396 - bw),
            (a, c, 623 - cw),
        ):
            edges.extend(((first, last, delta),
                          (last, first, -delta)))
    return edges


def edges_for(hits: list[tuple[int, ...]]) -> list[tuple[int, int, int]]:
    """Each (a,b,d) imposes start[b] >= start[a] + d."""
    edges = []
    for a, aw, b, bw, c, cw in hits:
        for first, last, difference in (
            (a, b, 397 + aw - bw),
            (a, c, 624 + aw - cw),
        ):
            edges.extend(((first, last, difference),
                          (last, first, -difference)))
    return edges


def lower_bound_distances(
    origin: int, nodes: list[int], edges: list[tuple[int, int, int]]
) -> dict[int, int | None]:
    """Longest-path lower bounds; reject positive cycles, all exact integers."""
    d: dict[int, int | None] = {n: None for n in nodes}
    d[origin] = 0
    for _ in range(len(nodes)):
        changed = False
        for a, b, floor in edges:
            if d[a] is not None:
                candidate = d[a] + floor
                if d[b] is None or d[b] < candidate:
                    d[b] = candidate
                    changed = True
        if not changed:
            return d
    raise ValueError("contradictory positive constraint cycle")


def gap_edges(nodes: list[int]) -> list[tuple[int, int, int]]:
    return [(a, b, 4) for a, b in zip(nodes, nodes[1:])]


def test_graph_control() -> None:
    toy = [(0, 1, 4), (1, 2, 4), (0, 2, 8), (2, 0, -8)]
    assert lower_bound_distances(0, [0, 1, 2], toy)[2] == 8
    try:
        lower_bound_distances(0, [0, 1, 2], toy + [(2, 0, -7)])
    except ValueError:
        pass
    else:
        raise AssertionError("contradictory positive cycle undetected")
    rng = Random(7123)
    samples = [untemper(rng.getrandbits(32)) for _ in range(628)]
    for word in range(3):
        assert samples[624 + word] == (
            samples[397 + word] ^ twist(samples[word], samples[word + 1])
        )


def assert_witness(
    starts: dict[int, int | None], nodes: list[int], hits: list[tuple[int, ...]]
) -> None:
    assert all(starts[b] - starts[a] >= 4 for a, b in zip(nodes, nodes[1:]))
    for a, aw, b, bw, c, cw in hits:
        assert starts[b] + bw - starts[a] - aw == 397
        assert starts[c] + cw - starts[a] - aw == 624


def main() -> None:
    test_graph_control()
    words = parse_ack_words()
    hits = source_triples(words)
    identities = edges_for(hits)
    boundaries = boundary_triples(words)
    ack_nodes = [*range(128), 129, 131, 132]
    all_nodes = list(range(133))
    ack = identities + gap_edges(ack_nodes)
    all_rows = identities + gap_edges(all_nodes)
    ack_min = lower_bound_distances(0, ack_nodes, ack)[132]
    all_min = lower_bound_distances(0, all_nodes, all_rows)[132]
    assert (ack_min, all_min) == (925, 933)
    assert_witness(lower_bound_distances(0, ack_nodes, ack), ack_nodes, hits)
    assert_witness(lower_bound_distances(0, all_nodes, all_rows), all_nodes, hits)
    # v2 Agent27's published witness had span 991, which was feasible but
    # not minimal. Hold this *arbitrary source-feasible* span fixed to test
    # whether it can pin the selected attempt's historical generator index.
    span = 991
    fixed = ack + [(0, 132, span), (132, 0, -span)]
    lower = lower_bound_distances(0, ack_nodes, fixed)[129]
    upper = -lower_bound_distances(129, ack_nodes, fixed)[0]
    assert (lower, upper) == (914, 980)
    # A branch-invariance test, NOT a search for accepting coupon values.
    for selected_index in range(lower, upper + 1):
        equality = [(0, 129, selected_index), (129, 0, -selected_index)]
        witness = lower_bound_distances(0, ack_nodes, fixed + equality)
        assert witness[0] == 0 and witness[132] == span
        assert witness[129] == selected_index
        assert_witness(witness, ack_nodes, hits)
        if selected_index in (lower, upper):
            print("EXTREME", selected_index, {k: witness[k] for k in
                  (0, 44, 52, 53, 83, 97, 127, 129, 131, 132)})
    augmented = ack + boundary_edges(boundaries)
    augmented_min = lower_bound_distances(0, ack_nodes, augmented)[132]
    assert augmented_min == 930
    augmented_fixed = augmented + [(0, 132, span), (132, 0, -span)]
    new_lower = lower_bound_distances(0, ack_nodes, augmented_fixed)[129]
    new_upper = -lower_bound_distances(129, ack_nodes, augmented_fixed)[0]
    assert (new_lower, new_upper) == (919, 980)
    generator = Random(7123)
    stream = [untemper(generator.getrandbits(32)) for _ in range(995)]
    source_witness = lower_bound_distances(
        0, ack_nodes, augmented_fixed +
        [(0, 129, new_lower), (129, 0, -new_lower)]
    )
    for a, b, bw, c, cw in boundaries:
        assert ((stream[source_witness[b] + bw] ^
                 stream[source_witness[c] + cw]) & 0xBFFFFFFF) == (
                     twist(0, stream[source_witness[a]]) & 0xBFFFFFFF
                 )
    assert_witness(source_witness, ack_nodes, hits)
    for candidate in range(new_lower, new_upper + 1):
        equality = [(0, 129, candidate), (129, 0, -candidate)]
        witness = lower_bound_distances(
            0, ack_nodes, augmented_fixed + equality
        )
        assert witness[129] == candidate
        assert_witness(witness, ack_nodes, hits)
    print("CONTROL: toy graph/positive-cycle and CPython MT original law PASS")
    print("BOUNDARY: 3 original source-only 31-bit reverse-word triples")
    print("AUGMENTED: min ACK span", augmented_min,
          "and fixed-span selected range", new_lower, "..", new_upper,
          "(62 feasible placements)")
    print("ORIGINAL: 19 routine + 2 late ACK-only reverse-word identities")
    print("MINIMUM SOURCE-NECESSARY SPAN: ACK-stage", ack_min,
          "vs mistaken REQUESTED-four-word floor", all_min)
    print("AT FIXED CONDITIONAL SPAN 991: selected index", lower, "..", upper,
          "inclusive; 67 feasible integer placements")
    print("K04 selected payload/mask/commitment unused; authenticated bits 0/128")


if __name__ == "__main__":
    main()
