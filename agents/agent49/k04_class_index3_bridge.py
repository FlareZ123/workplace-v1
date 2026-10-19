"""K04: row99 hidden sampler index3 distinguishes two source producer families.

Run: python agents/agent49/k04_class_index3_bridge.py original-case.zip
Selected printer row129 and acceptance commitments are never read.
"""
import re
import sys
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent31"))
from k04_mt_recursive_peel import rows, groups, close_group, temper


def main(source):
    words = rows(source)
    assert words[129] == []
    clusters = groups(source, words)
    group = next(entries for entries in clusters.values()
                 if any(row == 99 for row, _ in entries))
    start = next(position for row, position in group if row == 99)
    state, _ = close_group(group, words)
    assert (start, state[start + 4], state[start + 5]) == (
        621, (0xFFFFFFFF, 0xFA3CA1BF), (0xFFFFFFFF, 0xA58E3D83)
    )

    with ZipFile(source) as z:
        lines = [line for line in
                 z.read("evidence/print/spool-reconstruction.log").decode().splitlines()
                 if line.startswith("2026-")]
    assert len(lines) == 133
    assert re.search(r"DEST=(\w+)", lines[99]).group(1) == "store"
    assert re.search(r"CLASS=(\w+)", lines[100]).group(1) == "LABEL"

    post = temper(state[start + 4][1])
    next_sample = temper(state[start + 5][1])
    assert post == 0x0247F23A and post >> 30 == 0
    assert next_sample == 0x6F9C95A3 and next_sample >> 29 == 3

    print("source_rows", "99->100")
    print("row99_postpayload_DEST", f"{post:08X}", "index0=store")
    print("next_hidden_full_output", f"{next_sample:08X}", "top3=3")
    print("next_source_CLASS", "LABEL")
    print("hypothesis_n4_no_intervening_draws",
          "s100-s99=6, CLASS index3 maps to LABEL")
    print("hypothesis_custom_threshold3_no_intervening_draws",
          "index3 rejected, requires s100-s99>=7")
    print("both_inferences_model_conditional", True)
    print("selected_row129_and_verifier_untouched", True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: k04_class_index3_bridge.py original-case.zip")
    main(Path(sys.argv[1]))
