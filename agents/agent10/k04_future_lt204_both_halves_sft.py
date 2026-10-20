"""Read-only p955 future-donor LT204 sibling gate, both 16-bit halves.

Run from repo root:
    python -m agents.agent10.k04_future_lt204_both_halves_sft.py ORIGINAL_43_MEMBER.zip

The selected printer row129, route, K04/K08 commitments and checker are never used.
The p955 MT producer chronology is a conditional source-compatible fixture.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import zipfile

from agents.agent3 import k04_future_companion_donor_sft as carrier

TELEMETRY_SHA = "3787dbd6bab3930ea5293c25a995175161a1c0d7683daad29f498026e057639f"


def original_runs(source):
    assert hashlib.sha256(source).hexdigest() == TELEMETRY_SHA
    rows = [json.loads(line) for line in source.splitlines()]
    diag = [x for x in rows if x.get("tag") == "LT-204"
            and x.get("field") == "DIAG_WORD"]
    assert len(diag) == 33
    ordinary = [x for x in diag if x.get("seq") in range(8)
                and x.get("revision") in range(1, 5)]
    assert len(ordinary) == 32
    assert Counter(x["revision"] for x in ordinary) == {1: 8, 2: 8, 3: 8, 4: 8}

    groups = {
        f"revision-{rev}": sorted((x for x in ordinary
                                   if x["revision"] == rev), key=lambda x: x["seq"])
        for rev in range(1, 5)
    }
    groups["seq-revision"] = sorted(ordinary,
                                    key=lambda x: (x["seq"], x["revision"]))
    groups["revision-seq"] = sorted(ordinary,
                                    key=lambda x: (x["revision"], x["seq"]))
    groups["original-file"] = list(ordinary)
    groups["UTC-time"] = sorted(
        ordinary,
        key=lambda x: datetime.fromisoformat(x["ts"]).astimezone(timezone.utc),
    )
    chosen = {}
    for x in ordinary:
        if x["quality"] == "GOOD" and x["state"] == "HOLD":
            if x["seq"] not in chosen or x["revision"] > chosen[x["seq"]]["revision"]:
                chosen[x["seq"]] = x
    assert set(chosen) == set(range(8))
    groups["K02-selected"] = [chosen[i] for i in range(8)]
    assert len(groups) == 9

    out = []
    for name, ordered in groups.items():
        for first in range(len(ordered)):
            for count in (3, 4, 5):
                selected = ordered[first:first + count]
                if len(selected) < count:
                    continue
                if name.startswith("revision-") or name == "K02-selected":
                    if any(selected[i + 1]["seq"] != selected[i]["seq"] + 1
                           for i in range(count - 1)):
                        continue
                out.append((name, first, tuple(x["value"] for x in selected)))
    assert len(out) == 423, len(out)
    return out


def companion_windows(masks):
    windows = []
    for count in (3, 4, 5):
        for donor in carrier.DONORS:
            for start in range(max(971, donor - count + 1), donor + 1):
                companions = tuple(
                    (i, masks[i][1]) for i in range(start, start + count)
                    if i != donor and masks[i][0] == 0xFFFFFFFF
                )
                if len(companions) >= 2:
                    windows.append((count, donor, start, companions))
    assert len(windows) == 24, len(windows)
    return windows


def byte_swap16(x):
    return ((x & 255) << 8) | (x >> 8)


def main(source_path):
    starts = json.loads(
        (carrier.ROOT / "results/h17-k04-source-consistent-index955.json").read_text()
    )["row_starts"]
    assert len(starts) == 133 and starts[129] == 955
    masks = carrier.original_future_masks(source_path, starts)
    windows = companion_windows(masks)
    with zipfile.ZipFile(source_path) as original:
        runs = original_runs(original.read("evidence/telemetry/freeze-export.jsonl"))

    counts = {"upper16": 0, "lower16": 0}
    hits = {"upper16": [], "lower16": []}
    for name, first, observed in runs:
        for count, donor, start, companions in windows:
            if len(observed) != count:
                continue
            for orientation in ("native", "swap16"):
                values = observed if orientation == "native" else tuple(
                    byte_swap16(x) for x in observed
                )
                for half, shift in (("upper16", 16), ("lower16", 0)):
                    counts[half] += 1
                    if all(values[index - start] == (
                            (carrier.temper(word) >> shift) & 0xFFFF)
                            for index, word in companions):
                        hits[half].append((name, first, donor, start, orientation))

    assert counts == {"upper16": 6588, "lower16": 6588}, counts
    assert not hits["upper16"] and not hits["lower16"], hits

    # Calibration uses two genuine source-forced future siblings, without
    # inserting any disputed coupon or unobserved source target value.
    count, donor, start, companions = windows[0]
    for shift in (16, 0):
        synthetic = [0x1234] * count
        for index, word in companions:
            synthetic[index - start] = (carrier.temper(word) >> shift) & 0xFFFF
        assert all(synthetic[index - start] ==
                   ((carrier.temper(word) >> shift) & 0xFFFF)
                   for index, word in companions)

    print(json.dumps({
        "source_model": "p955 source-compatible common-MT hypothesis only",
        "ordinary_original_telemetry_values": 32,
        "excluded_edge_revision99": "2026-10-03T21:13:48+00:00 value FFFF",
        "order_families": 9,
        "telemetry_windows": len(runs),
        "source_forced_future_companion_windows": len(windows),
        "tested_comparisons": counts,
        "matching_original_donors": hits,
        "synthetic_sibling_positive": "PASS",
        "authenticated_K04_bits": 0,
        "K08_exact_final_words": 0,
    }, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m agents.agent10.k04_future_lt204_both_halves_sft.py ORIGINAL.zip")
    main(Path(sys.argv[1]))
