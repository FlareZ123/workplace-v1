"""Construct a 128-dimensional K04 nullspace for a source-consistent MT layout.

Requires only the original case ZIP and Agent11's source-consistent index955
layout JSON. The selected printer payload, REC8 digests and mask are withheld.
"""
import hashlib
import json
import random
import sys
from zipfile import ZipFile

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MASK32 = 0xFFFFFFFF


def stream(initial, limit):
    words = list(initial)
    for t in range(limit - 623):
        x = (words[t] & 0x80000000) | (words[t + 1] & 0x7FFFFFFF)
        words.append((words[t + 397] ^ (x >> 1) ^
                      (0x9908B0DF if x & 1 else 0)) & MASK32)
    return words


def rank(vectors):
    basis = {}
    for vector in vectors:
        while vector:
            bit = vector.bit_length() - 1
            if bit not in basis:
                basis[bit] = vector
                break
            vector ^= basis[bit]
    return len(basis)


def universal_source_window():
    """Check every bounded local row-group placement, independent of payloads."""
    total = 0
    for p in range(945, 956):
        u, q, m = p - 851, p - 623, p - 227
        assert 0 <= u < 397 and 0 <= q + 3 < 397
        for d in range(11, 66):
            for delta in range(627, d + 617):
                s43 = p - delta
                s44 = s43 + d
                s12, s13 = s43 - 229, s44 - 227
                s96, s97 = s43 + 393, s44 + 394
                assert s12 + 3 < u < s13
                assert s43 + 3 < q and q + 3 < s44
                assert s96 + 3 < m and m + 3 < s97
                for g97 in (3, 94):
                    s45 = s44 + 4 + g97
                    s132 = s45 + 621
                    assert s132 + 3 <= p + 160 < p + 227
                total += 1
    assert total == 16940
    return total


def main(archive_path, fixture_path):
    with ZipFile(archive_path) as z:
        spool = z.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    assert sum(line.startswith("2026-") for line in spool.decode().splitlines()) == 133
    with open(fixture_path, encoding="utf-8") as f:
        layout = json.load(f)
    starts = layout["row_starts"]
    assert len(starts) == 133 and starts[0] == 0
    assert all(starts[i] + 4 <= starts[i + 1] for i in range(132))
    assert layout["source_spool_sha256"] == SPOOL_SHA

    p = starts[129]
    assert p == 955
    q = p - 623
    early = p - 851
    middle = p - 227
    observations = {starts[i] + j for i in range(133) if i != 129 for j in range(4)}
    horizon = max(observations)
    assert starts[43] + 3 < q and q + 3 < starts[44]
    assert starts[12] + 3 < early < starts[13]
    assert starts[96] + 3 < middle and middle + 3 < starts[97]
    assert q + 3 < 397 and horizon < p + 227
    assert starts[130] == p + 4
    assert not observations.intersection({early, middle, *(q + j for j in range(4))})

    perturbations = [(q + j, bit, p + j)
                     for j in range(4) for bit in range(31)]
    perturbations += [(q + j, 31, p + j + 1) for j in range(3)]
    perturbations += [(early, 31, p)]
    assert len(perturbations) == 128
    basis_vectors = []
    for seed in (20261020, 1733):
        rng = random.Random(seed)
        initial = [rng.getrandbits(32) for _ in range(624)]
        base = stream(initial, horizon)
        for index, bit, affected_target in perturbations:
            changed = list(initial)
            changed[index] ^= 1 << bit
            after = stream(changed, horizon)
            changed_positions = {i for i in range(horizon + 1) if base[i] != after[i]}
            predicted = ({index, affected_target} if index != early
                         else {early, middle, p})
            assert changed_positions == predicted, (seed, index, bit, changed_positions)
            assert changed_positions.isdisjoint(observations)
            if seed == 20261020:
                basis_vectors.append((after[affected_target] ^ base[affected_target])
                                     << (32 * (affected_target - p)))
        changed = list(initial)
        changed[q + 3] ^= 0x80000000
        after = stream(changed, horizon)
        assert {i for i in range(horizon + 1) if base[i] != after[i]} == {q + 3, p + 4}
        assert p + 4 in observations
        print("independent_synthetic_seed", seed, "PASS")
    assert rank(basis_vectors) == 128
    print("global_placement_cases_tested", universal_source_window())
    print("original_source_spool_sha256", SPOOL_SHA)
    print("selected_row_withheld", 129, "MT_index", p)
    print("hidden_first_cycle", early, q, q + 1, q + 2, q + 3)
    print("hidden_middle", middle, "latest_observed_MT_index", horizon)
    print("explicit_original_payload_nullspace_dimension", rank(basis_vectors), "/128")
    print("scope", "unrestricted_initial_MT_state and published index955 fixture; CLASS/DEST metadata not constrained")
    print("no_original_K04_bytes_recovered")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
