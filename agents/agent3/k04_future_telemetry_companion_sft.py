"""Conditional original-source LT-204 future-sibling K04 donor search.
Run: python agents/agent3/k04_future_telemetry_companion_sft.py original-case.zip
Requires colocated agent3 k04_future_companion_donor_sft.py. Never tests
selected spool row129, original coupon/mask/hash, K08 nonce or verifier.
"""
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import zipfile

import k04_future_companion_donor_sft as carrier

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
TELEMETRY_SHA = "3787dbd6bab3930ea5293c25a995175161a1c0d7683daad29f498026e057639f"


def telemetry_runs(raw):
    assert hashlib.sha256(raw).hexdigest() == TELEMETRY_SHA
    entries = []
    for line in raw.splitlines():
        x = json.loads(line)
        if (x.get("tag") == "LT-204" and x.get("field") == "DIAG_WORD"
                and x.get("seq") in range(8) and x.get("revision") in range(1, 5)):
            entries.append(x)
    assert len(entries) == 32
    groups = {}
    for rev in range(1, 5):
        group = sorted((x for x in entries if x["revision"] == rev), key=lambda x:x["seq"])
        assert len(group) == 8 and [x["seq"] for x in group] == list(range(8))
        groups[f"revision-{rev}"] = group
    groups["seq-revision"] = sorted(entries, key=lambda x:(x["seq"], x["revision"]))
    groups["revision-seq"] = sorted(entries, key=lambda x:(x["revision"], x["seq"]))
    groups["original-file"] = list(entries)
    groups["UTC-time"] = sorted(entries, key=lambda x:datetime.fromisoformat(x["ts"]).astimezone(timezone.utc))
    selected = {}
    for x in entries:
        if x["quality"] == "GOOD" and x["state"] == "HOLD":
            if x["seq"] not in selected or x["revision"] > selected[x["seq"]]["revision"]:
                selected[x["seq"]] = x
    assert sorted(selected) == list(range(8))
    groups["K02-selected"] = [selected[i] for i in range(8)]
    assert len(groups) == 9
    runs = []
    for name, records in groups.items():
        for start in range(len(records)):
            for length in (3, 4, 5):
                sample = records[start:start+length]
                if len(sample) != length:
                    continue
                if (name.startswith("revision-") or name == "K02-selected") and any(
                        sample[j+1]["seq"] != sample[j]["seq"]+1 for j in range(length-1)):
                    continue
                runs.append((name, start, tuple(x["value"] for x in sample)))
    assert len(runs) == 396
    return runs


def future_windows(masks):
    found = []
    for length in (3, 4, 5):
        for donor in carrier.DONORS:
            for start in range(max(971, donor-length+1), donor+1):
                companions = tuple((i, masks[i][1]) for i in range(start,start+length)
                                   if i != donor and masks[i][0] == 0xFFFFFFFF)
                if len(companions) >= 2:
                    found.append((length, donor, start, companions))
    assert len(found) == 24
    assert sum(donor == 1866 for _, donor, _, _ in found) == 6
    return found


def byteswap16(x):
    return int.from_bytes(x.to_bytes(2, "little"), "big")


def main(path):
    with zipfile.ZipFile(path) as z:
        spool = z.read("evidence/print/spool-reconstruction.log")
        telemetry = z.read("evidence/telemetry/freeze-export.jsonl")
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    starts = json.loads((carrier.ROOT / "results/h17-k04-source-consistent-index955.json").read_text())["row_starts"]
    assert len(starts) == 133 and starts[129] == 955
    masks = carrier.original_future_masks(path, starts)
    windows = future_windows(masks)
    runs = telemetry_runs(telemetry)
    tests = 0
    matches = []
    for name, offset, observed in runs:
        for length, donor, start, companions in windows:
            if length != len(observed):
                continue
            for orientation in ("direct", "swap16"):
                tests += 1
                words = observed if orientation == "direct" else tuple(map(byteswap16,observed))
                if all(words[i-start] == carrier.temper(value)>>16 for i,value in companions):
                    matches.append((name,offset,length,donor,start,orientation))
    assert tests == 6096, tests
    _, _, start, companions = next(w for w in windows if w[1] == 1866 and w[2] == 1866 and w[0] == 3)
    control = [0x1234] * 3
    for index, value in companions:
        control[index-start] = carrier.temper(value)>>16
    assert all(control[index-start] == carrier.temper(value)>>16 for index,value in companions)
    print(json.dumps({
        "hypothesis":"conditional MT19937 single producer, original p955 source-consistent chronology",
        "telemetry_values":32,
        "source_order_families":9,
        "ordered_runs":len(runs),
        "future_target_adjacent_windows":len(windows),
        "comparisons":tests,
        "matches":matches,
        "synthetic_X1866_twin_positive":"PASS",
        "actual_K04_bits":0,
        "new_exact_K08_words":0
    }, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python agents/agent3/k04_future_telemetry_companion_sft.py original-case.zip")
    main(Path(sys.argv[1]))
