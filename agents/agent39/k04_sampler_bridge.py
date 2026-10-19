"""Conditional K04 two-sampler bridge: row80 -> row81 -> hidden row111 DEST.

Run: python agents/agent39/k04_sampler_bridge.py original-case.zip

Reads original spool through established 42-witness group builder. Selected
row129 is withheld by the group builder. No acceptance, route, or mask reads.
"""
import re
import sys
from pathlib import Path
from zipfile import ZipFile

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "agent31"))
from k04_mt_recursive_peel import rows, groups, close_group, temper

ALL = 0xFFFFFFFF
SPOOL = "evidence/print/spool-reconstruction.log"
CLASSES = {"LABEL": 0, "STORES": 1, "RECOVER": 2}
DESTS = {"store": 0, "desk": 1, "bench": 2}


def main(source):
    with ZipFile(source) as z:
        spool = z.read(SPOOL).decode("utf-8")
    lines = [line for line in spool.splitlines() if line.startswith("2026-")]
    assert len(lines) == 133
    source_class = [CLASSES[re.search(r"CLASS=([A-Z]+)", x).group(1)] for x in lines]
    source_dest = [DESTS[re.search(r"DEST=([a-z]+)", x).group(1)] for x in lines]

    words = rows(source)
    assert words[129] == []
    clusters = list(groups(source, words).values())
    left = next(c for c in clusters if any(r == 80 for r, p in c))
    right = next(c for c in clusters if any(r == 81 for r, p in c))
    assert left is not right
    pos80 = dict(left)[80]
    pos81 = dict(right)[81]
    old_left, _ = close_group(left, words)
    old_right, _ = close_group(right, words)

    # Exact observed independent state words, recovered from row28 / row111
    # recurrence witnesses. Dest first, class second, both accepted.
    assert all(old_left[pos80 + d][0] == ALL for d in (4, 5))
    destination_sample = temper(old_left[pos80 + 4][1]) >> 30
    class_sample = temper(old_left[pos80 + 5][1]) >> 29
    assert destination_sample == source_dest[80] == 2
    assert class_sample == source_class[81] == 0

    # CONDITIONAL producer hypothesis: immediately after payload row80,
    # DEST uses 2-bit rejection-sampled index; CLASS immediately before
    # payload row81 uses 3-bit threshold-3 index. No unrelated RNG draws.
    # Since both samples accept, next payload begins after exactly 2 draws.
    delta = pos80 + 6 - pos81
    merged = left + [(r, p + delta) for r, p in right]
    merged_state, _ = close_group(merged, words)
    pos111 = dict(merged)[111]
    target_pos = pos111 + 4
    assert target_pos not in old_left or old_left[target_pos][0] != ALL
    old_right_local = target_pos - delta
    assert old_right_local not in old_right or old_right[old_right_local][0] != ALL
    mask, hidden_word = merged_state[target_pos]
    assert mask == ALL

    # Destination row111 was never consulted to infer the row80->81 link.
    predicted_dest = temper(hidden_word) >> 30
    assert predicted_dest == source_dest[111] == 0
    assert hidden_word == 0xB08D384B
    assert temper(hidden_word) == 0x12597B7A

    known_before = {
        p: w for p, w in old_left.items() if w[0] == ALL
    }
    for p, w in old_right.items():
        if w[0] == ALL:
            assert p + delta not in known_before or known_before[p + delta] == w
            known_before[p + delta] = w
    known_after = {p: w for p, w in merged_state.items() if w[0] == ALL}
    newly_complete = sorted(set(known_after) - set(known_before))

    print("row129_selected_withheld", True)
    print("row80_destination_index", destination_sample, "expected", source_dest[80])
    print("row81_class_index", class_sample, "expected", source_class[81])
    print("model_conditional_row81_minus_row80", 6)
    print("merged_group_rows", sorted(r for r, _ in merged))
    print("newly_complete_untempered", [(p - pos80, f"{known_after[p][1]:08X}")
                                      for p in newly_complete])
    print("row111_predicted_destination", predicted_dest, "observed", source_dest[111])
    print("row111_hidden_untempered", f"{hidden_word:08X}")
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python agents/agent39/k04_sampler_bridge.py original-case.zip")
    main(Path(sys.argv[1]))
