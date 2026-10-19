"""K04: five-draw row9 p621 n|171 boundary, AX8 high16 heldout.

Run: python agents/agent18/k04_row9_g5_p621_ax8.py original.zip.
Requires contested row9 gap5, common original AX5..8 generator and CPython
first-cycle seed model. No selected coupon/acceptance/K08 source read.
"""
import random
import sys
from k04_row9_period171_four_step_bridge import source
from k04_row9_ax_seed_gates import early as row9_early, original as row9_source
from k04_ax_31bit_seed_sieve import M, forward, seed_word, untemper
from k04_ax_backward_checkpoint_sieve import temper, twist

TOP=0x80000000
LOW=0x7FFFFFFF
LENGTHS=(9,19,57,171)


def candidates(p,n,row9_state,late,row9_word3):
    """Original AX8 high16 predicted from exact initial-state recurrence."""
    slot=(p-1)%n
    key=(seed_word(late[0],late[1],late[2],p)-slot)&M
    out=[]
    for hi in (0,TOP):
        s172=row9_state[2]|hi
        s171=forward(row9_state[1],s172,p-171,key,(p-172)%n)
        predecessor=(row9_word3 ^ twist(s172>>31,s171))&M
        out.append((hi,temper(predecessor)>>16))
    return out


def positives():
    hits=0
    for n in LENGTHS:
        seed=sum(
            ((j*1664525+0x74857392+n*113)&M)<<(32*j)
            for j in range(n)
        )
        initial=random.Random(seed).getstate()[1][:624]
        rng=random.Random(seed)
        stream=[untemper(rng.getrandbits(32)) for _ in range(625)]
        for p in (402,430,535,620,621):
            a=(initial[p-174],initial[p-173],initial[p-172]&LOW)
            late=(*initial[p-2:p+3],0)
            predicted=candidates(p,n,a,late,stream[p-172])
            assert (initial[p-172]&TOP,temper(stream[p-399])>>16) in predicted
            hits+=1
    assert hits==20
    print("ACTUAL_CPYTHON_SEEDED_20_AX8_POSITIVE_CONTROLS_PASS")


def original(filename):
    _,_,late=source(filename)
    ancestors,row9,ax8=row9_source(filename)
    words,edge=row9_early(ancestors,row9,5)
    a=(*words,edge)
    assert a==(0xFBB38820,0xCCA6D76A,0x4814FE5F)
    assert ax8==0xA77C
    for n in LENGTHS:
        predicted=candidates(621,n,a,late,row9[3])
        assert predicted==[(0,0xDC18),(TOP,0xC583)]
        assert not any(val==ax8 for _,val in predicted)
        print("KEY_WORDS",n,"p621_AX8_EXPECTED",f"{ax8:04X}",
              "PREDICTED",*[f"{v:04X}" for _,v in predicted],
              "SURVIVORS",0)
    print("p621_n9_n19_n57_n171_g5_AX8_EXCLUDED")
    print("ORIGINAL_K04_K08_STILL_MISSING; ACCEPTANCE_UNREAD")


if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: python k04_row9_g5_p621_ax8.py original.zip")
    positives()
    original(sys.argv[1])
