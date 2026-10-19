"""Conditional K04 sampler bridge at regular rows 33->34; predicts row86 CLASS.

Run: python agents/agent30/k04_row33_sampler_bridge.py original-case.zip

Reads only source printer spool through existing 42-witness source-pinned
modules. The selected spool row129 and all REC8 commitments are withheld.
This is conditional on no extra RNG draws between row33 DEST and row34 CLASS.
"""
import re
import sys
from pathlib import Path
from zipfile import ZipFile

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "agent31"))
from k04_mt_recursive_peel import rows, groups, close_group, temper

SPOOL = "evidence/print/spool-reconstruction.log"
CLASS = {"LABEL": 0, "STORES": 1, "RECOVER": 2}
DEST = {"store": 0, "desk": 1, "bench": 2}
ALL = 0xFFFFFFFF


def twist(a, b):
    y = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return ((y >> 1) ^ (0x9908B0DF if y & 1 else 0)) & ALL


def main(source):
    words = rows(source)
    assert not words[129]
    clusters = list(groups(source, words).values())
    left = next(g for g in clusters if any(r == 33 for r, _ in g))
    right = next(g for g in clusters if any(r == 34 for r, _ in g))
    assert left is not right
    pos33, pos34 = dict(left)[33], dict(right)[34]
    old_left, _ = close_group(left, words)
    old_right, _ = close_group(right, words)

    # Independent right-hand group reconstructs two outputs immediately
    # preceding row34's payload. Under exactly two intervening metadata
    # draws they can be DEST(row33) then CLASS(row34), respectively.
    assert all(old_right[pos34 - d][0] == ALL for d in (1, 2))
    dest_index = temper(old_right[pos34 - 2][1]) >> 30
    class_index = temper(old_right[pos34 - 1][1]) >> 29
    assert (dest_index, class_index) == (2, 0)

    shift = pos33 + 6 - pos34
    joined = left + [(r, p + shift) for r, p in right]
    state, _ = close_group(joined, words)
    newly_full = sorted(
        p - pos33 for p, (mask, value) in state.items()
        if mask == ALL
        and old_left.get(p, (0, 0))[0] != ALL
        and old_right.get(p - shift, (0, 0))[0] != ALL
    )
    assert newly_full == [-620, -224, 399], newly_full
    recovered = {
        p: state[pos33 + p][1] for p in newly_full
    }
    assert recovered == {
        -620: 0xB30BF870,
        -224: 0x4C457F5B,
        399: 0x8E4AFDB6,
    }

    # Direct recurrence witness from intact row33 and row116 payloads.
    # No row86 CLASS field is used in this calculation.
    assert recovered[399] == (
        state[pos33 + 626][1] ^
        twist(state[pos33 + 2][1], state[pos33 + 3][1])
    )
    predicted = temper(recovered[399]) >> 29
    assert predicted == 1

    # Only now inspect the independent original row86 class metadata.
    with ZipFile(source) as archive:
        lines = [
            line for line in archive.read(SPOOL).decode().splitlines()
            if line.startswith("2026-")
        ]
    assert len(lines) == 133
    actual = CLASS[re.search(r"CLASS=([A-Z]+)", lines[86]).group(1)]
    destination33 = DEST[re.search(r"DEST=([a-z]+)", lines[33]).group(1)]
    class34 = CLASS[re.search(r"CLASS=([A-Z]+)", lines[34]).group(1)]
    assert (destination33, class34) == (dest_index, class_index)
    assert predicted == actual == 1

    print("selected_row129_withheld", True)
    print("bridge_row33_to_row34", "s34-s33=6 (conditional)")
    print("sample_indices", {"DEST33": dest_index, "CLASS34": class_index})
    print("new_untempered_words", {p: f"{v:08X}" for p, v in recovered.items()})
    print("row86_CLASS_independent_prediction", predicted, "actual", actual)
    print("original_K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_row33_sampler_bridge.py original-case.zip")
    main(Path(sys.argv[1]))
