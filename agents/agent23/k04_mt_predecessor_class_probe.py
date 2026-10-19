"""Probe source-restored pre-payload MT words as potential binary class flags.

Usage: python agents/agent23/k04_mt_predecessor_class_probe.py original-case.zip
The selected row129 and all REC8 acceptance commitments are excluded.
Hypothesis is exploratory and source-conditional, not the recovered K04.
"""
from collections import Counter
import re
import struct
import sys
from pathlib import Path
from zipfile import ZipFile

from k04_mt_inverse_peel import groups, recover, rows, SPOOL


def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9D2C5680
    x ^= (x << 15) & 0xEFC60000
    x ^= x >> 18
    return x & 0xFFFFFFFF


def run(source):
    with ZipFile(source) as archive:
        raw = archive.read(SPOOL)
    lines = [line for line in raw.decode().splitlines() if line.startswith("2026-")]
    assert len(lines) == 133
    word_rows = rows(source)
    clusters = groups(source, word_rows)
    observations = []
    for root, members in clusters.items():
        full, partial, evidence = recover(members, word_rows)
        for row, start in members:
            if row == 129 or start - 1 not in full:
                continue
            line = lines[row]
            label = re.search(r"CLASS=([A-Z]+)", line).group(1)
            previous = temper(full[start-1])
            observations.append((row, label, previous, previous >> 30))
    observations.sort()
    assert len(observations) == 10
    assert len({r for r, _, _, _ in observations}) == 10
    # Fixed binary predicate after inspecting first five rows. The last
    # five are a chronological holdout *within this selected dataset*.
    def predicted(label):
        return int(label == "RECOVER")
    train, test = observations[:5], observations[5:]
    assert all(index == predicted(label) for _,label,_,index in train)
    assert all(index == predicted(label) for _,label,_,index in test)
    print("selected_target_row129_excluded", True)
    print("source_derived_immediate_pre_payload_output_count",len(observations))
    for row,label,word,index in observations:
        print("row",row,"class",label,"prior_mt_output",f"{word:08X}",
              "prior_getrandbits2",index,"binary_class_prediction",predicted(label))
    print("training_matches",len(train),"of",len(train))
    print("chronological_holdout_matches",len(test),"of",len(test))
    print("upper_two_bit_counts",sorted(Counter(t[3] for t in observations).items()))
    print("source_empirical_binary_class_gate",True)
    print("generator_draw_rule", "HYPOTHESIS_UNCONFIRMED")
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_mt_predecessor_class_probe.py original-case.zip")
    run(Path(sys.argv[1]))
