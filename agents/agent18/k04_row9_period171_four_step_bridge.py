"""K04: row9 six-draw AX seed window bridges first-cycle 171-index key residues.

Run: python agents/agent18/k04_row9_period171_four_step_bridge.py original.zip

Imports SHA-pinned original source derivation from Agents26/28, and local
CPython init-by-array forward. Read-only; withholds selected printer row129,
K04/K08 acceptance, mask, verifier. Six-draw row9->10 producer premise
explicit and unverified.
"""
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent26"))
sys.path.insert(0, str(ROOT / "agent28"))

from k04_seven_residue_gate import infer, read_rows
from k04_row9_ax_seed_gates import early as row9_early, original as row9_original
from k04_ax_31bit_seed_sieve import M, forward, seed_word

TOP = 0x80000000
LOW = 0x7FFFFFFF
LENGTHS = (1, 3, 9, 19, 57, 171)


def test_phase(p, n, row9_state, pre168, late):
    """Return all possible A->B exact initial-state bridge matches.

    For n|171, the late initialized-state 5-word block supplies
    KEY at forward steps p-171, p-170, p-169. Its trailing low31
    supplies 31 bits at step p-168. There are exactly 2*2 branches.
    """
    assert 402 <= p <= 620 and 171 % n == 0
    keys = {}
    for index, j in ((p, 2), (p+1, 3), (p+2, 4)):
        residue = (index-1) % n
        value = (seed_word(late[j-2],late[j-1],late[j],index)-residue) & M
        if residue in keys and keys[residue] != value:
            return []
        keys[residue] = value
    residue2 = (p+2) % n
    low = (seed_word(late[3],late[4],late[5],p+3)-residue2) & LOW

    survivors = []
    for s172top in (0, TOP):
        s172 = row9_state[2] | s172top
        s171 = forward(
            row9_state[1],s172,p-171,
            keys[(p-172)%n],(p-172)%n,
        )
        s170 = forward(
            s172,s171,p-170,keys[(p-171)%n],(p-171)%n,
        )
        s169 = forward(
            s171,s170,p-169,keys[(p-170)%n],(p-170)%n,
        )
        for key2top in (0, TOP):
            s168 = forward(s170,s169,p-168,low | key2top,residue2)
            if s168 == pre168[0]:
                survivors.append((p,s172top,key2top,s168))
    return survivors


def positives():
    passed = 0
    for n in LENGTHS:
        seed = sum(
            ((0x8316F1A3 + 0x09E377B9*j + n*12345) & M) << (32*j)
            for j in range(n)
        )
        state = random.Random(seed).getstate()[1][:624]
        for p in (402,430,535,564,620):
            a = (state[p-174],state[p-173],state[p-172]&LOW)
            b = (state[p-168],state[p-167],state[p-166]&LOW)
            c = (*state[p-2:p+3],state[p+3]&LOW)
            predictions = test_phase(p,n,a,b,c)
            assert (
                p,state[p-172]&TOP,
                (seed>>(32*((p+2)%n)))&TOP,state[p-168]
            ) in predictions, (n,p,predictions)
            passed += 1
    assert passed == 30
    print("ACTUAL_CPYTHON_SEEDED_30_POSITIVE_CONTROLS_PASS")


def source(filename):
    # Agent26 reconstructs old early/late initialized state from 12
    # intact printer rows and checks original spool SHA. Agent28
    # constructs old AX5..7 ancestors from original transfer audit,
    # checks spool/audit SHA, and joins original printer row9.
    earlier, later, _ = infer(read_rows(filename))
    ancestors, r9, _ = row9_original(filename)
    words, next_low = row9_early(ancestors,r9,6)
    row9_state = (*words,next_low)
    assert row9_state == (0x418BDA1E,0x2E02BC3D,0x38EBB043)
    assert earlier[0] == [0x0A9DE247,0xFBBBB07E]
    assert earlier[1] == 0x2A07F662
    assert later[0] == [
        0xB30BF870,0x6CE0E225,0xF4E8FCB2,
        0xC517EB25,0x7D3AAF35
    ]
    assert later[1] == 0x31FD69FC
    return row9_state,earlier[0],(*later[0],later[1])


def original(filename):
    row9_state, earlier, late = source(filename)
    for n in LENGTHS:
        survived = [
            answer for p in range(402,621)
            for answer in test_phase(p,n,row9_state,earlier,late)
        ]
        print("CPYTHON_NUMERIC_KEY_WORDS",n,
              "VALID_FIRSTCYCLE_PHASES",219,
              "FOUR_BRANCH_COMPARISONS",876,
              "EXACT_S_pminus168_MATCHES",len(survived))
        assert not survived
    print("K04_K08_MISSING; NO_ACCEPTANCE_INPUTS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_row9_period171_four_step_bridge.py case.zip")
    positives()
    original(sys.argv[1])
