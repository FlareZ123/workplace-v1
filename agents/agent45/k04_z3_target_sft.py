"""Source-only K04 global MT chronology and target-bit probe (Agent 45).

Run from the repository root with an untouched original case ZIP:
    python agents/agent45/k04_z3_target_sft.py c-energy-group-documents2026.zip

Requires scipy and z3-solver (Python bindings). Discards selected row129 before inference; no selected payload values, K04
route/mask, acceptance commitments, or K08 wording influence the model.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import sys
import numpy as np
from scipy.sparse.csgraph import floyd_warshall
import z3

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from agents.agent37.k04_global_inverse_chronology_sft import source, conflicts
from agents.agent21.k04_double_twist_sft import sig
from agents.agent33.k04_global_target_projection import solve_target, state_expressions, test_synthetic

def graph(words, extra_fixed=()):
    ws, within, boundary = words
    assert len(within) == 25 and len(boundary) == 17
    fixed = []
    for (a, i), (b, j), (c, k) in within:
        fixed.extend(((a, b, 397 + i - j), (a, c, 624 + i - k)))
    for a, bit, (b, j), (c, k) in boundary:
        fixed.extend(((a, b, 396 - j), (a, c, 623 - k)))
    # Two adjacent full 31-bit double-twist witnesses, original rows only.
    for k in (0, 1):
        assert sig(ws[9][k + 2], ws[40][k]) == ((ws[63][k] ^ ws[124][k]) & 0xBFFFFFFF)
    fixed += [(9, 40, 229), (9, 63, 398), (9, 124, 852)]
    fixed += list(extra_fixed)
    parent = list(range(133))
    offset = [0] * 133
    def find(x):
        if parent[x] == x:
            return x, 0
        r, d = find(parent[x])
        parent[x] = r
        offset[x] += d
        return r, offset[x]
    def join(a, b, d):
        ra, da = find(a)
        rb, db = find(b)
        if ra == rb:
            assert db - da == d
        else:
            parent[rb] = ra
            offset[rb] = d + da - db
    for a, b, d in fixed:
        join(a, b, d)
    components = defaultdict(list)
    for r in range(133):
        root, d = find(r)
        components[root].append((r, d))
    group = [0] * 133
    offs = [0] * 133
    groups = []
    for members in components.values():
        g = len(groups)
        reference = members[0][1]
        groups.append([r for r, _ in members])
        for r, d in members:
            group[r] = g
            offs[r] = d - reference
    assert len(groups) == 81 - len(extra_fixed)
    return fixed, groups, group, offs

def first_gf2_conflict(words, starts):
    """Exact original-bit-equation provenance of the first GF(2) contradiction."""
    terms = state_expressions(max(starts) + 3)
    basis = {}
    deps = {}
    for r, row in enumerate(words):
        for j, value in enumerate(row):
            for b, expr in enumerate(terms[starts[r] + j]):
                v = (expr << 1) | ((value >> b) & 1)
                witnesses = 1 << (r * 128 + j * 32 + b)
                while v:
                    p = v.bit_length() - 1
                    existing = basis.get(p)
                    if existing is None:
                        break
                    v ^= existing
                    witnesses ^= deps[p]
                if v == 1:
                    return [rr for rr in range(133) if (witnesses >> (rr * 128)) & ((1 << 128) - 1)]
                if v:
                    p = v.bit_length() - 1
                    basis[p] = v
                    deps[p] = witnesses
    return None

def probe(zip_path, position, max_iterations=20000):
    words, within, boundary = source(str(zip_path))
    fixed, groups, group, offs = graph((words, within, boundary))
    n = 133
    D = np.full((n, n), np.inf)
    np.fill_diagonal(D, 0)
    for a, b, delta in fixed:
        D[a, b] = min(D[a, b], delta)
        D[b, a] = min(D[b, a], -delta)
    for r in range(n - 1):
        floor = 7 if r == 9 else (6 if r < 127 else 4)
        D[r + 1, r] = min(D[r + 1, r], -floor)
    D[130, 131] = min(D[130, 131], 4)
    D[131, 130] = min(D[131, 130], -4)
    D[0, 129] = min(D[0, 129], position)
    D[129, 0] = min(D[129, 0], -position)
    D = floyd_warshall(D, directed=True)
    if min(np.diag(D)) < 0:
        return {"position": position, "status": "infeasible_difference_bounds"}
    solver = z3.Solver()
    variables = [z3.Int(f"group_{i}") for i in range(len(groups))]
    for g, rows in enumerate(groups):
        low = int(max(-D[r, 0] - offs[r] for r in rows))
        high = int(min(D[0, r] - offs[r] for r in rows))
        solver.add(variables[g] >= low, variables[g] <= high)
    for r in range(n - 1):
        floor = 7 if r == 9 else (6 if r < 127 else 4)
        solver.add(variables[group[r + 1]] + offs[r + 1]
                   >= variables[group[r]] + offs[r] + floor)
    solver.add(variables[group[131]] + offs[131]
               == variables[group[130]] + offs[130] + 4)
    seen = set()
    gf2_cores = 0
    for iteration in range(1, max_iterations + 1):
        status = solver.check()
        if status == z3.unsat:
            return {"position": position, "status": "infeasible", "iterations": iteration,
                    "nogoods": len(seen), "gf2_cores": gf2_cores}
        if status != z3.sat:
            return {"position": position, "status": "solver_unknown", "iterations": iteration}
        model = solver.model()
        base = [model.eval(v).as_long() for v in variables]
        starts = [base[group[r]] + offs[r] for r in range(n)]
        bad = conflicts(words, starts)
        if bad:
            subsets = [{a, b, c} for a, i, b, j, c, k, d1, d2 in bad]
        else:
            core = first_gf2_conflict(words, starts)
            if core is None:
                output = solve_target(words, starts)
                return {"position": position, "status": "source_consistent",
                        "iterations": iteration, "nogoods": len(seen),
                        "gf2_cores": gf2_cores, "projection": output,
                        "row_starts": starts}
            subsets = [set(core)]
            gf2_cores += 1
        for rows in subsets:
            choices = tuple(sorted({(group[r], base[group[r]]) for r in rows}))
            if choices in seen:
                continue
            seen.add(choices)
            solver.add(z3.Or(*(variables[g] != value for g, value in choices)))
    return {"position": position, "status": "iteration_limit", "nogoods": len(seen)}

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python agents/agent45/k04_z3_target_sft.py <original-case.zip>")
    import json
    test_synthetic()
    for p in range(945, 956):
        result = probe(Path(sys.argv[1]), p)
        print(json.dumps(result, sort_keys=True), flush=True)

if __name__ == "__main__":
    main()
