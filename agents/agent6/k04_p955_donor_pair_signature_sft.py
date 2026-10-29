"""Source-only H-17 K04 31-bit MT19937 donor-pair signature.

Historical p955/common-MT placement is hypothetical. Never decodes disputed
printer row129, and does not open mask, verifier, or REC8 commitments.
Run from repository root:
    python agents/agent6/k04_p955_donor_pair_signature_sft.py original-export.zip
"""
import hashlib
import itertools
import json
import random
import re
import struct
import sys
import zipfile
from pathlib import Path
from agents.agent33.k04_global_target_projection import (
    state_expressions, untemper, tempered_expressions,
)

ORIGINAL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
DONORS = (728, 1185, 1411, 1412)
MASK = 0xBFFFFFFF
A = 0x9908B0DF

def add(basis, expr):
    while expr:
        k = expr.bit_length() - 1
        old = basis.get(k)
        if old is None:
            basis[k] = expr
            return True
        expr ^= old
    return False

def reduce(basis, expr):
    while expr:
        old = basis.get(expr.bit_length() - 1)
        if old is None:
            return expr
        expr ^= old
    return 0

def twist(a, b):
    combined = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return ((combined >> 1) ^ (A if b & 1 else 0)) & 0xFFFFFFFF

def source_rows(path):
    with zipfile.ZipFile(path) as z:
        raw = z.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw).hexdigest() == ORIGINAL_SHA
    lines = [line for line in raw.splitlines() if b"PAYLOAD=" in line]
    assert len(lines) == 133
    lines[129] = re.sub(rb"PAYLOAD=[A-F0-9]{32}", b"PAYLOAD=WITHHELD", lines[129])
    rows = []
    for i, line in enumerate(lines):
        match = re.search(rb"PAYLOAD=([A-F0-9]{32})", line)
        if i == 129:
            assert match is None
            rows.append([])
        else:
            assert match is not None
            rows.append([untemper(w) for w in struct.unpack("<4I", bytes.fromhex(match.group(1).decode("ascii")))])
    return rows

def extra_dimension(source_basis, terms, positions):
    basis = source_basis.copy()
    for position in positions:
        for expr in terms[position]:
            add(basis, expr)
    return len(basis) - len(source_basis)

def synthetic_controls():
    for seed in (0, 1, 20261029, 908193, 0xFFFFFFFF):
        rng = random.Random(seed)
        words = [untemper(rng.getrandbits(32)) for _ in range(1413)]
        assert words[1412] == words[1185] ^ twist(words[788], words[789])
        assert ((words[1185] ^ words[1412]) & MASK) == (twist(0, words[789]) & MASK)
    print("independently seeded MT recurrence controls: 5/5 PASS")

def run(zip_path):
    synthetic_controls()
    root = Path(__file__).resolve().parents[2]
    starts = json.loads((root / "results/h17-k04-source-consistent-index955.json").read_text(encoding="utf-8"))["row_starts"]
    assert len(starts) == 133 and starts[129] == 955 and starts[105] == 789
    rows = source_rows(zip_path)
    assert rows[129] == [] and rows[105][0] == 0xEB3D818E
    terms = state_expressions(1412)
    source_basis, affine_basis = {}, {}
    count = 0
    for r, row in enumerate(rows):
        for j, word in enumerate(row):
            for bit, expr in enumerate(terms[starts[r] + j]):
                equation = (expr << 1) | ((word >> bit) & 1)
                remainder = reduce(affine_basis, equation)
                assert remainder != 1, (r,j,bit)
                if remainder:
                    add(affine_basis, remainder)
                add(source_basis, expr)
                count += 1
    assert count == 16896 and len(source_basis) == len(affine_basis) == 15305
    assert all(extra_dimension(source_basis, terms, (t,)) == 32 for t in DONORS)

    signature = twist(0, rows[105][0])
    assert signature == 0x359EC0C7
    assert extra_dimension(source_basis, terms, (788,)) == 32
    assert extra_dimension(source_basis, terms, (789,)) == 0
    for bit in range(32):
        xor_expr = terms[1185][bit] ^ terms[1412][bit]
        observed = reduce(affine_basis, xor_expr << 1)
        if bit == 30:
            assert observed not in (0,1)
        else:
            assert observed == ((signature >> bit) & 1), bit

    pairs = []
    for a, b in itertools.combinations(DONORS, 2):
        rank = extra_dimension(source_basis, terms, (a,b))
        pairs.append({"positions": [a,b], "unknown_bits": rank, "known_parities": 64 - rank})
    assert [(item["positions"], item["known_parities"]) for item in pairs] == [
        ([728,1185],0), ([728,1411],0), ([728,1412],0),
        ([1185,1411],0), ([1185,1412],31), ([1411,1412],0),
    ]
    target = [e for pos in range(955,959) for e in tempered_expressions(terms[pos])]
    def target_rank(donors):
        b=source_basis.copy()
        for pos in donors:
            for e in terms[pos]:
                add(b,e)
        before=len(b)
        for e in target:
            add(b,e)
        return len(b)-before
    ranks = {"original":target_rank(()), "1185":target_rank((1185,)),
             "1412":target_rank((1412,)), "pair":target_rank((1185,1412))}
    assert ranks == {"original":128,"1185":97,"1412":96,"pair":96}
    print(json.dumps({"original_rank":len(source_basis),"selected_erased":True,
        "known_source_state_789":"EB3D818E",
        "pair_xor_mask":"BFFFFFFF","pair_xor_value":"359EC0C7",
        "pairs":pairs,"conditional_target_ranks":ranks,
        "historically_recovered_K04_bits":0},indent=2))

if __name__ == "__main__":
    assert len(sys.argv) == 2, "usage: script.py original-export.zip"
    run(Path(sys.argv[1]))
