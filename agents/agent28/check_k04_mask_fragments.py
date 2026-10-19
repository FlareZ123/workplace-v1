"""Read-only source-layer hypothesis: reorder transcribed K04 mask fragments.

From repo root: python agents/agent28/check_k04_mask_fragments.py resources
No mutation of spool, route, acceptance or original checker.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
from math import comb
import configparser
import json
import sys


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("resources")
    routing = json.loads((root / "evidence/recovery-routing.json").read_text())
    acceptance = json.loads((root / "acceptance.json").read_text())
    labels = configparser.ConfigParser()
    labels.read(root / "evidence/archive-labels.ini")
    job = labels["printer_routes_2026-09-01_to_2026-10-03"]["ESC-N"]
    mask = bytes.fromhex(routing["K04"]["masked_component"])
    target = bytes.fromhex(acceptance["slot_sha256"]["K04"])

    selected = []
    for line in (root / "evidence/print/spool-reconstruction.log").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        fields = dict(field.split("=", 1) for field in line.split()[1:])
        if fields["JOB"] == job and fields["STATE"] == "ACK" and fields["CLASS"] == "RECOVER":
            selected.append((int(fields["ATTEMPT"]), bytes.fromhex(fields["PAYLOAD"])))
    payload = max(selected)[1]

    def digest_of_mask(other: bytes) -> bytes:
        return sha256(bytes(a ^ b for a, b in zip(payload, other))).digest()

    assert len(mask) == len(payload) == 16
    synthetic_mask = mask[8:] + mask[:8]
    synthetic_target = digest_of_mask(synthetic_mask)
    counts = Counter()
    synthetic_hits = 0
    original_hits = []

    for sections in range(2, 6):
        for cuts in combinations(range(1, 16), sections - 1):
            bounds = (0, *cuts, 16)
            pieces = [mask[bounds[i]:bounds[i + 1]] for i in range(sections)]
            for rev in product((False, True), repeat=sections):
                oriented = [part[::-1] if flip else part for part, flip in zip(pieces, rev)]
                for order in permutations(range(sections)):
                    proposed_mask = b"".join(oriented[i] for i in order)
                    digest = digest_of_mask(proposed_mask)
                    counts[sections] += 1
                    if sections == 2 and digest == synthetic_target:
                        synthetic_hits += 1
                    if digest == target:
                        original_hits.append({"parts": sections, "cuts": cuts, "reverse": rev, "order": order, "mask": proposed_mask.hex().upper()})
        expected = comb(15, sections - 1) * __import__("math").factorial(sections) * (1 << sections)
        assert counts[sections] == expected
    assert synthetic_hits > 0
    print(json.dumps({
        "source_route_job": job,
        "selected_ack_attempt": max(selected)[0],
        "assignment_counts": {str(k): counts[k] for k in sorted(counts)},
        "total_assignments": sum(counts.values()),
        "synthetic_positive_matches_in_two_part_class": synthetic_hits,
        "original_commitment_matches": original_hits
    }, indent=2))


if __name__ == "__main__":
    main()
