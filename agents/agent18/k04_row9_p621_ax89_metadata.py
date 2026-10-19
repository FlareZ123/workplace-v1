"""K04 p621 period171 boundary: source AX8/9 and two printer metadata checks.

Run: python agents/agent18/k04_row9_p621_ax89_metadata.py original.zip
Read-only, selected row129 and acceptance withheld. Requires 6-draw
row9->10 and AX position8/9 contiguous source-generation premises.
"""
import hashlib
import json
import random
import re
import sys
from zipfile import ZipFile

from k04_row9_period171_four_step_bridge import source
from k04_ax_31bit_seed_sieve import M, forward, seed_word, untemper
from k04_ax_backward_checkpoint_sieve import temper, twist

P = 621
TOP = 0x80000000
LOW = 0x7FFFFFFF
LENGTHS = (9, 19, 57, 171)
TRANSFER_SHA = "32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf"


def predictions(p,n,initial,late,ax8,ax9):
    """Predicted metadata high16 outputs, both S[p-172] top completions."""
    assert 402 <= p <= 621 and 171 % n == 0
    key = {}
    for i,j in ((p,2),(p+1,3),(p+2,4)):
        slot = (i-1)%n
        value = (seed_word(late[j-2],late[j-1],late[j],i)-slot)&M
        if slot in key:
            assert key[slot] == value
        key[slot] = value
    out = []
    for hi in (0,TOP):
        s172 = initial[2] | hi
        s171 = forward(initial[1],s172,p-171,
                       key[(p-172)%n],(p-172)%n)
        s170 = forward(s172,s171,p-170,
                       key[(p-171)%n],(p-171)%n)
        # Original AX checkpoint positions8/9 give high16 tempered
        # of X[p−399],X[p−398] with no unknown lower bits required.
        dest = ax8 ^ (temper(twist(s172>>31,s171))>>16)
        label = ax9 ^ (temper(twist(s171>>31,s170))>>16)
        out.append((hi,dest,label))
    return out


def synthetic():
    count = 0
    for n in LENGTHS:
        for p in (402,430,535,620,621):
            seed = sum(
                ((0x5719BDA2+0x1397*j+p*13)&M)<<(32*j)
                for j in range(n)
            )
            state = random.Random(seed).getstate()[1][:624]
            rng = random.Random(seed)
            stream = [untemper(rng.getrandbits(32)) for _ in range(p+2)]
            initial = (state[p-174],state[p-173],state[p-172]&LOW)
            late = (*state[p-2:p+3],state[p+3]&LOW) if p<621 else (
                *state[p-2:p+3],0
            )
            ax8 = temper(stream[p-399])>>16
            ax9 = temper(stream[p-398])>>16
            cases = predictions(p,n,initial,late,ax8,ax9)
            expected = (
                state[p-172]&TOP,
                temper(stream[p-172])>>16,
                temper(stream[p-171])>>16,
            )
            assert expected in cases, (n,p,expected,cases)
            count += 1
    assert count == 20
    print("ACTUAL_CPYTHON_SEEDED_20_AX_METADATA_POSITIVES_PASS")


def original(filename):
    initial,_,late = source(filename)
    with ZipFile(filename) as archive:
        raw = archive.read("evidence/transfers/transfer-audit.jsonl")
        spool = archive.read("evidence/print/spool-reconstruction.log").decode()
    assert hashlib.sha256(raw).hexdigest() == TRANSFER_SHA
    transfer = sorted(
        (obj for line in raw.decode().splitlines()
         if (obj:=json.loads(line)).get("kind") == "CHUNK"
         and obj.get("transfer") == "AX-7778"),
        key=lambda a:(a["seq"],a["attempt"]),
    )
    ax8 = int.from_bytes(bytes.fromhex(transfer[8]["checkpoint"]),"little")
    ax9 = int.from_bytes(bytes.fromhex(transfer[9]["checkpoint"]),"little")
    assert (ax8,ax9)==(0xA77C,0x34A2)

    rows = [s for s in spool.splitlines() if s.startswith("2026-")]
    assert len(rows)==133
    assert "DEST=store" in rows[9] and "CLASS=STORES" in rows[10]
    # Hypothetical standard CPython upper-bit getrandbits(2) and (3).
    for n in LENGTHS:
        choices = predictions(P,n,initial,late,ax8,ax9)
        actual=[(h,a>>14,b>>13) for h,a,b in choices]
        print("N",n,"P",P,"AX8_AX9_METADATA_BRANCHES",actual)
        assert len(choices)==2
        assert [(a,b) for h,a,b in choices]==[
            (0x9CB3,0xFE9E),(0xBD0E,0xC666)
        ]
        assert all((a>>14,b>>13)!=(0,1) for h,a,b in choices)
    print("ORIGINAL_p621_n9_n19_n57_n171_AX8_9_METADATA_EXCLUDED")
    print("K04_K08_UNKNOWN; ACCEPTANCE_UNREAD")


if __name__ == "__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: python k04_row9_p621_ax89_metadata.py case.zip")
    synthetic()
    original(sys.argv[1])
