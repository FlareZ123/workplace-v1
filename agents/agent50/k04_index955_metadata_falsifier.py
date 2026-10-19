"""Check original-source indexed printer metadata against one MT19937 chronology.

Usage: python agents/agent50/k04_index955_metadata_falsifier.py original-export.zip
No selected row129, recovery mask, K04/K08 hashes, or verifier are consulted.
"""
import json
import re
import sys
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent33"))
from k04_global_target_projection import source_rows, state_expressions, tempered_expressions

ROOT = Path(__file__).resolve().parents[2]
DEST = {"store": 0, "desk": 1, "bench": 2}
CLASS = {"LABEL": 0, "STORES": 1, "RECOVER": 2}

def add(basis, expr, bit):
    v = (expr << 1) | bit
    while v:
        if v == 1:
            raise ValueError("Inconsistent original-source GF(2) constraints")
        k = v.bit_length() - 1
        old = basis.get(k)
        if old is None:
            basis[k] = v
            return
        v ^= old

def codes(terms, basis, index, width):
    exprs = tempered_expressions(terms[index])
    accepted = set()
    for code in range(1 << width):
        trial = basis.copy()
        try:
            for bit in range(32 - width, 32):
                add(trial, exprs[bit], (code >> (bit - 32 + width)) & 1)
        except ValueError:
            continue
        accepted.add(code)
    return accepted

def main(source):
    path = ROOT / "results/h17-k04-source-consistent-index955.json"
    starts = json.loads(path.read_text(encoding="utf-8"))["row_starts"]
    assert len(starts) == 133 and starts[0] == 0 and starts[129] == 955
    assert all(starts[r + 1] >= starts[r] + 4 for r in range(132))
    rows = source_rows(source)  # Original spool SHA-pinned; selected row129 removed.
    terms = state_expressions(starts[-1] + 3)
    basis = {}
    for r, words in enumerate(rows):
        for j, word in enumerate(words):
            for b, expr in enumerate(terms[starts[r] + j]):
                add(basis, expr, (word >> b) & 1)
    assert len(basis) == 15305
    with ZipFile(source) as z:
        lines = [line.decode() for line in z.read("evidence/print/spool-reconstruction.log").splitlines()
                 if line.startswith(b"2026-")]
    labels = [(re.search(r"CLASS=([A-Z]+)", line).group(1),
               re.search(r"DEST=([a-z]+)", line).group(1)) for line in lines]
    assert len(labels) == 133
    errors = []
    two_draw = 0
    for r in range(127):  # Only ordinary-to-ordinary boundaries use both samplers.
        if starts[r + 1] - starts[r] != 6:
            continue
        two_draw += 1
        # Exactly two hidden draws means accepted DEST then accepted CLASS,
        # with no room for a rejected candidate or an extra producer call.
        got_dest = codes(terms, basis, starts[r] + 4, 2)
        got_class = codes(terms, basis, starts[r] + 5, 3)
        expected_dest = DEST[labels[r][1]]
        expected_class = CLASS[labels[r + 1][0]]
        if expected_dest not in got_dest or expected_class not in got_class:
            errors.append((r, r + 1, labels[r][1], sorted(got_dest),
                           labels[r + 1][0], sorted(got_class)))
    assert two_draw == 50 and len(errors) == 15, (two_draw, errors)
    print("source_rank", len(basis), "indexed_row129", starts[129])
    print("two_draw_transitions", two_draw, "contradictory_transitions", len(errors))
    for row in errors:
        print("r,next,dest,allowed_dest,next_class,allowed_class:", *row)

if __name__ == "__main__":
    main(Path(sys.argv[1]))
