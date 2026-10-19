"""Search AX checkpoint triples using original-source inferred MT state runs.

Run: python agents/agent9/k04_ax_newsource_sft.py ORIGINAL_H17_ZIP
K04 selected spool row129, masked component, all acceptance commitments withheld.
"""
import collections
import hashlib
import json
from pathlib import Path
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent31"))
from k04_mt_inverse_peel import rows, groups, inverse_twist
from k04_mt_recursive_peel import close_group, temper

ALL = 0xFFFFFFFF
LOW = 0x7FFFFFFF
TRANSFER_SHA = "32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf"


def check(case_path):
    values = rows(case_path)
    assert len(values) == 133 and not values[129]
    cluster = groups(case_path, values)
    original = {root: {start + j for row, start in entries
                       for j in range(len(values[row]))}
                for root, entries in cluster.items()}
    inferred = {}
    new_full = 0
    for root, entries in cluster.items():
        state, new = close_group(entries, values)
        inferred[root] = state
        new_full += len(new)
    assert (len(cluster), new_full) == (84, 65)  # includes empty withheld row129

    with zipfile.ZipFile(case_path) as z:
        raw = z.read("evidence/transfers/transfer-audit.jsonl")
    assert hashlib.sha256(raw).hexdigest() == TRANSFER_SHA
    transfers = [json.loads(line) for line in raw.splitlines()]
    original_triples = collections.defaultdict(list)
    total_triples = 0
    for transfer in ("AX-7778", "AX-7781", "AX-7782", "AX-7783"):
        fragments = [v for v in transfers if v.get("kind") == "CHUNK" and v["transfer"] == transfer]
        assert len(fragments) == 16
        series = {
            "all": sorted(fragments, key=lambda r: (r["seq"], r["attempt"])),
            "winning": [max((r for r in fragments if r["seq"] == s), key=lambda r: r["attempt"])
                        for s in range(8)]
        }
        for kind, records in series.items():
            for endian in ("little", "big"):
                codes = [int.from_bytes(bytes.fromhex(r["checkpoint"]), endian) for r in records]
                for start in range(len(codes) - 2):
                    triple = tuple(codes[start:start + 3])
                    original_triples[triple[:2]].append((transfer, kind, endian, start, triple[2]))
                    total_triples += 1
    assert total_triples == 160

    runs = []
    for root, state in inferred.items():
        for index, (mask, val) in state.items():
            middle = state.get(index + 1, (0, 0))
            last = state.get(index + 2, (0, 0))
            if mask != ALL or middle[0] != ALL or last[0] & LOW != LOW:
                continue
            for high in ((0, 1) if last[0] != ALL else (last[1] >> 31,)):
                runs.append((root, index, val, middle[1], (last[1] & LOW) | (high << 31),
                             last[0] != ALL))
    assert len(runs) == 336

    matches = []
    for a in runs:
        for b in runs:
            if a[0] == b[0] and b[1] - a[1] != 227:
                continue
            derived = [inverse_twist(a[2 + j] ^ b[2 + j]) for j in range(3)]
            p1 = (derived[1] & 0x80000000) | (derived[0] & LOW)
            p2 = (derived[2] & 0x80000000) | (derived[1] & LOW)
            pair = (temper(p1) >> 16, temper(p2) >> 16)
            for transfer, kind, endian, offset, third in original_triples.get(pair, ()):
                if third not in (temper(derived[2] & LOW) >> 16,
                                 temper(derived[2] | 0x80000000) >> 16):
                    continue
                novel = (a[5] or b[5] or any(a[1] + j not in original[a[0]]
                                               or b[1] + j not in original[b[0]]
                                               for j in range(3)))
                matches.append((transfer, kind, endian, offset, a[0], a[1], b[0], b[1], novel))
    assert len(matches) == 6, matches
    assert all(m[0] == "AX-7778" and m[1] == "all" and m[2] == "little"
               and not m[-1] for m in matches), matches
    assert sorted(set(m[3] for m in matches)) == [5, 11, 12]
    print("WITHHELD_K04_ROW129", not values[129])
    print("ORIGINAL_COHORT_STATE_GROUPS", len(cluster), "NEW_FULL_INFERRED", new_full)
    print("THREE_WORD_SOURCE_RUNS", len(runs), "AX_TRIPLES", total_triples)
    print("THREE_CHECKPOINT_HITS", len(matches), "UNPREVIOUSLY_INFERRED_OR_PARTIAL_HITS", 0)
    print("ONLY_PRIOR_AX7778_WITNESSES", sorted(set(m[3] for m in matches)))
    print("NO_NEW_K04_TARGET_ANCHOR")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python k04_ax_newsource_sft.py ORIGINAL_H17_ZIP")
    check(sys.argv[1])
