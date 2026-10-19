"""K04: alternate five-output row9->10 branch, four-step CPython period171 gate.

Usage: python agents/agent18/k04_row9_g5_period171_bridge.py original.zip

Companion to g6 SFT; uses intact SHA-pinned AX5..7 / row9 g5
original-source positions and exact same four-step CPython algorithm.
Withholds selected row129, original K04/K08 commitments and verifier.
"""
import random
import sys
from k04_row9_period171_four_step_bridge import (
    LENGTHS, M, test_phase, source,
)
from k04_row9_ax_seed_gates import early as row9_early, original as row9_source

LOW=0x7FFFFFFF
TOP=0x80000000


def synthetic():
    passed=0
    for n in LENGTHS:
        seed=sum(
            ((0x4F8BA227 + j*0x9E3779B9 + n*0x1377)&M) << (32*j)
            for j in range(n)
        )
        st=random.Random(seed).getstate()[1][:624]
        for p in (402,430,535,564,620):
            row9=(st[p-174],st[p-173],st[p-172]&LOW)
            early=(st[p-168],st[p-167],st[p-166]&LOW)
            late=(*st[p-2:p+3],st[p+3]&LOW)
            proposed=test_phase(p,n,row9,early,late)
            expected=(p,st[p-172]&TOP,
                      (seed>>(32*((p+2)%n)))&TOP,st[p-168])
            assert expected in proposed,(p,n)
            passed+=1
    assert passed==30
    print("ACTUAL_PYTHON_SEEDED_30_POSITIVE_CONTROLS_PASS")


def original(filename):
    _, old_early, late=source(filename)
    ancestors,rows,_=row9_source(filename)
    full,low=row9_early(ancestors,rows,5)
    row9=(*full,low)
    assert row9==(0xFBB38820,0xCCA6D76A,0x4814FE5F)
    for n in LENGTHS:
        matches=[
            value for p in range(402,621)
            for value in test_phase(p,n,row9,old_early,late)
        ]
        print("ROW9_5DRAW_LENGTH",n,"PHASES",219,
              "COMPARISONS",876,"FULL_STATE_BRIDGE_MATCHES",len(matches))
        assert not matches
    print("FIVE_AND_SIX_DRAW_ROW9_MODELS_BOTH_REJECT_n9_n171")
    print("K04_K08_MISSING; ORIGINAL_ACCEPTANCE_UNREAD")


if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: python k04_row9_g5_period171_bridge.py original.zip")
    synthetic()
    original(sys.argv[1])
