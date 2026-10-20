"""Joint original printer / CRC-valid TRP2 / RC-17 MT index and K04 quotient.

Run: python agents/agent45/k04_joint_crosscarrier_sft.py ORIGINAL_CASE.zip

Uses only original evidence, retains disputed printer row129 as an empty block,
and does not use recovery masks, K04/K08 commitments, or the verifier.
Requires scipy and z3-solver. The single-MT producer/order assumption is conditional.
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
import zipfile
import zlib
from pathlib import Path

import numpy as np
from scipy.sparse.csgraph import floyd_warshall
import z3

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from agents.agent37.k04_global_inverse_chronology_sft import source, conflicts, ut, inverse
from agents.agent45.k04_z3_target_sft import graph
from agents.agent33.k04_global_target_projection import state_expressions, tempered_expressions

REC_SHA = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
SRC_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
# Original intact supporting middle/end words: control precedes middle by 396
TRP = [
    (40, 9, 2, 40, 0), (12, 9, 3, 40, 1),
    (28, 10, 0, 41, 0), (17, 10, 1, 41, 1),
    (45, 10, 3, 41, 3), (26, 7, 3, 38, 0),
]
# The original recorder record72 fails its CRC and is excluded from independent constraints.
REV_B = [("PURGE", 28, 2, 59, 3), ("VERIFY", 28, 1, 59, 2)]
SHIFT = 624


def source_carriers(archive: Path, words: list[list[int]]) -> list[tuple[int, int, int, str]]:
    with zipfile.ZipFile(archive) as z:
        raw = z.read("evidence/recorder/trip-recorder.raw")
        proc = z.read("evidence/procedures/RC-17-scans.txt").decode("utf8")
    assert hashlib.sha256(raw).hexdigest() == REC_SHA
    assert raw.startswith(b"TRP2DUMP")
    assert struct.unpack_from("<I", raw, 12)[0] == 88
    assert len(raw) == 16 + 88 * 24
    carriers = []
    for idx, middle, word, later, nextword in TRP:
        rec = raw[16 + idx * 24:16 + (idx + 1) * 24]
        assert zlib.crc32(rec[:20]) == struct.unpack_from("<I", rec, 20)[0], idx
        state = ut(struct.unpack_from("<I", rec, 12)[0])
        assert (state ^ inverse(words[middle][word] ^ words[later][nextword])) & 0x7FFFFFFF == 0
        carriers.append((middle, word, state, f"TRP2 record {idx}"))
    pages = proc.split("\f")
    assert len(pages) == 12
    for section, middle, word, later, nextword in REV_B:
        page = next(x for x in pages if f"REV B / SECTION {section}" in x)
        field = re.search(r"Footer control strip: ([A-F0-9]{8})", page).group(1)
        state = ut(struct.unpack("<I", bytes.fromhex(field))[0])
        assert (state ^ inverse(words[middle][word] ^ words[later][nextword])) & 0x7FFFFFFF == 0
        carriers.append((middle, word, state, f"RC17 Rev B {section}"))
    return carriers


def source_test(words: list[list[int]], starts: list[int], carriers: list[tuple[int, int, int, str]]) -> dict:
    """Full GF(2) linearization; dependency-traced inconsistency or actual target quotient."""
    terms = state_expressions(max(starts) + SHIFT + 3)
    basis = {}
    dep = {}
    observations = [(SHIFT + starts[r] + j, value, r * 128 + j * 32)
                    for r, row in enumerate(words) for j, value in enumerate(row)]
    observations += [(SHIFT + starts[r] + j - 396, state, 133 * 128 + i * 32)
                     for i, (r, j, state, _) in enumerate(carriers)]

    def reduce(expr, val=0):
        v = (expr << 1) | (val & 1)
        while v and (v.bit_length() - 1) in basis:
            v ^= basis[v.bit_length() - 1]
        return v

    for pos, value, label in observations:
        assert pos >= 0
        for bit, expr in enumerate(terms[pos]):
            v = (expr << 1) | ((value >> bit) & 1)
            depmask = 1 << (label + bit)
            while v and (v.bit_length() - 1) in basis:
                pivot = v.bit_length() - 1
                v ^= basis[pivot]
                depmask ^= dep[pivot]
            if v == 1:
                original_rows = {r for r in range(133) if (depmask >> (r * 128)) & ((1 << 128) - 1)}
                original_rows.update(carriers[i][0] for i in range(len(carriers))
                                     if (depmask >> (133 * 128 + 32 * i)) & ((1 << 32) - 1))
                return {"contradiction_rows": sorted(original_rows)}
            if v:
                pivot = v.bit_length() - 1
                basis[pivot] = v
                dep[pivot] = depmask

    # Joint source+target elimination: a target XOR can expose an earlier
    # source pivot. Reducing only once against source overcounts target rank.
    target_basis = dict(basis)
    fixed = {}
    for j in range(4):
        for bit, expr in enumerate(tempered_expressions(terms[SHIFT + starts[129] + j])):
            residual = reduce(expr)
            idx = j * 32 + bit
            if residual in (0, 1):
                fixed[idx] = residual
            joint = expr << 1
            while joint and (joint.bit_length() - 1) in target_basis:
                joint ^= target_basis[joint.bit_length() - 1]
            if joint > 1:
                target_basis[joint.bit_length() - 1] = joint
    masks = [f"{sum((32*j+b in fixed) << b for b in range(32)):08X}" for j in range(4)]
    return {"source_rank": len(basis), "target_rank": len(target_basis) - len(basis),
            "fixed_target_bits": len(fixed), "fixed_masks": masks}



def test_joint_target_quotient_regression() -> None:
    """Guard against admitting an already-known source equation as a new target."""
    source_basis = {2: 0b0011 << 1}
    joined = dict(source_basis)
    for expr in (0b0100, 0b0111):
        vector = expr << 1
        while vector and (vector.bit_length() - 1) in joined:
            vector ^= joined[vector.bit_length() - 1]
        if vector > 1:
            joined[vector.bit_length() - 1] = vector
    assert len(joined) - len(source_basis) == 1


def probe(archive: Path, position: int, strict_sampler=None) -> dict:
    words, within, boundary = source(str(archive))
    with zipfile.ZipFile(archive) as z:
        assert hashlib.sha256(z.read("evidence/print/spool-reconstruction.log")).hexdigest() == SRC_SHA
    carrier = source_carriers(archive, words)
    anchors = [(7, 38, 230), (28, 59, 226)]
    _, groups, row_group, off = graph((words, within, boundary), extra_fixed=anchors)
    n = 133
    # These two recorded controls add exact conditional row-start relations.
    fixed = []
    for (a, i), (b, j), (c, k) in within:
        fixed.extend(((a, b, 397+i-j), (a, c, 624+i-k)))
    for a, _, (b, j), (c, k) in boundary:
        fixed.extend(((a, b, 396-j), (a, c, 623-k)))
    fixed += [(9,40,229),(9,63,398),(9,124,852)] + anchors
    dist = np.full((n,n),np.inf)
    np.fill_diagonal(dist,0)
    for a,b,d in fixed:
        dist[a,b] = min(dist[a,b], d)
        dist[b,a] = min(dist[b,a], -d)
    for r in range(n-1):
        floor = 7 if r == 9 else (6 if r < 127 else 4)
        dist[r+1,r] = min(dist[r+1,r], -floor)
    dist[130,131] = min(dist[130,131],4)
    dist[131,130] = min(dist[131,130],-4)
    dist[0,129] = min(dist[0,129],position)
    dist[129,0] = min(dist[129,0],-position)
    dist=floyd_warshall(dist,directed=True)
    if min(np.diag(dist))<0:
        return {"position":position,"status":"difference_infeasible"}
    solver=z3.Solver()
    x=[z3.Int(f"root_{g}") for g in range(len(groups))]
    for g,rows in enumerate(groups):
        solver.add(x[g]>=int(max(-dist[r,0]-off[r] for r in rows)))
        solver.add(x[g]<=int(min(dist[0,r]-off[r] for r in rows)))
    for r in range(n-1):
        floor = 7 if r==9 else (6 if r<127 else 4)
        solver.add(x[row_group[r+1]]+off[r+1]>=x[row_group[r]]+off[r]+floor)
    solver.add(x[row_group[131]]+off[131]==x[row_group[130]]+off[130]+4)
    seen=set()
    for iteration in range(1,20001):
        status=solver.check()
        if status==z3.unsat:
            return {"position":position,"status":"infeasible","iterations":iteration,
                    "nogoods":len(seen)}
        if status!=z3.sat:
            return {"position":position,"status":"solver_unknown"}
        model=solver.model()
        base=[model.eval(v).as_long() for v in x]
        starts=[base[row_group[r]]+off[r] for r in range(133)]
        bad=conflicts(words,starts)
        if bad:
            rows=[{a,b,c} for a,i,b,j,c,k,_,_ in bad]
        else:
            out=source_test(words,starts,carrier)
            if "contradiction_rows" not in out:
                if strict_sampler is None:
                    return {"position":position,"status":"crosscarrier_GF2_consistent",
                            "iterations":iteration,"nogoods":len(seen),**out,
                            "row_starts":starts}
                sampler_cores = strict_sampler(words, starts, carrier, archive)
                if not sampler_cores:
                    return {"position":position,"status":"strict_sampler_GF2_consistent",
                            "iterations":iteration,"nogoods":len(seen),**out,
                            "row_starts":starts}
                rows = [set(core) for core in sampler_cores]
            else:
                rows=[set(out["contradiction_rows"])]
        for constraint_rows in rows:
            assigned=frozenset((row_group[r],base[row_group[r]]) for r in constraint_rows)
            if assigned in seen:
                continue
            seen.add(assigned)
            solver.add(z3.Or(*(x[g]!=v for g,v in assigned)))
    return {"position":position,"status":"iteration_limit"}


if __name__=="__main__":
    test_joint_target_quotient_regression()
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python agents/agent45/k04_joint_crosscarrier_sft.py <original-case.zip>")
    for position in range(949,956):
        print(json.dumps(probe(Path(sys.argv[1]),position),sort_keys=True),flush=True)
