"""K04: complete 96-bit CPython first-cycle numeric seed inversion, source only.

Run: python agents/agent8/k04_n3_complete_firstcycle_seed.py ORIGINAL_ZIP

Uses just the intact row3/34 printer MT pair window, 392 absolute phases,
and a separately withheld intact row34 fourth output. No AX, recorder,
target row129, acceptance, mask, K08, or original verifier is consulted.
"""
import hashlib
import itertools
import random
import re
import struct
import sys
import zipfile
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"agent18"))
from k04_ax_31bit_seed_sieve import (
    M, SHA, inverse_pair, seed_word, source_words, untemper
)
from k04_extra_late31_residue_sieve import original_late_extra

LOW = 0x7FFFFFFF
TOP = 0x80000000


def possible_seeds(phase, late):
    assert 229 <= phase <= 620
    residues = {}
    for i, triple in ((phase+1,late[:3]),(phase+2,late[1:4])):
        index=(i-1)%3
        residues[index] = [(seed_word(*triple,i)-index)&M]
    i=phase+3
    index=(i-1)%3
    low=(seed_word(*late[2:5],i)-index)&LOW
    residues[index] = [low,low|TOP]
    assert len(residues)==3 and sorted(map(len,residues.values()))==[1,1,2]
    return [
        sum(word << (32*j) for j,word in enumerate(words))
        for words in itertools.product(*(residues[j] for j in range(3)))
    ]


def output_at(seed, index):
    generator=random.Random(seed)
    for _ in range(index):
        generator.getrandbits(32)
    return generator.getrandbits(32)


def temper(v):
    v ^= v>>11
    v ^= (v<<7)&0x9D2C5680
    v ^= (v<<15)&0xEFC60000
    return (v^(v>>18))&M


def synthetic():
    successes=0
    for phase in (229,230,300,396,535,620):
        for trial in range(15):
            words=[
                (0xDEADBEEF+trial*0xAAB76513+j*0x31415927)&M
                for j in range(3)
            ]
            seed=sum(word << (32*j) for j,word in enumerate(words))
            original=random.Random(seed)
            state=list(original.getstate()[1][:624])
            outputs=[
                untemper(original.getrandbits(32))
                for _ in range(phase+228)
            ]
            inverse=[
                inverse_pair(outputs[phase-229+j],outputs[phase-2+j])
                for j in range(5)
            ]
            late=[
                (inverse[j]&LOW)|(inverse[j+1]&TOP) for j in range(4)
            ]+[inverse[4]&LOW]
            assert late == state[phase-1:phase+3]+[state[phase+3]&LOW]
            proposals=possible_seeds(phase,late)
            assert len(proposals)==2 and seed in proposals
            intact=temper(outputs[phase+3])
            assert [s for s in proposals if output_at(s,phase+3)==intact]==[seed]
            successes+=1
    assert successes==90
    print("ACTUAL_SEEDED_96BIT_WINDOW_RECONSTRUCTION_CONTROLS_PASS",successes)


def original(source):
    _early,_late=source_words(source)
    last_low=original_late_extra(source)
    late=[*_late,last_low]
    assert late==[
        0x6CE0E225,0xF4E8FCB2,0xC517EB25,0x7D3AAF35,0x31FD69FC
    ]
    with zipfile.ZipFile(source) as archive:
        raw=archive.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw).hexdigest()==SHA
    lines=[v for v in raw.decode().splitlines() if v.startswith("2026-")]
    assert len(lines)==133
    r34=bytes.fromhex(re.search(
        r"PAYLOAD=([0-9A-F]{32})",lines[34]
    ).group(1))
    heldout=struct.unpack("<4I",r34)[3]
    assert heldout==0x2AC160B4

    surviving=[]
    trials=0
    for phase in range(229,621):
        for key in possible_seeds(phase,late):
            trials+=1
            if output_at(key,phase+3)==heldout:
                surviving.append((phase,key))
    print("SOURCE_INITIALIZED_STATE",*[f"{w:08X}" for w in late])
    print("INTACT_ROW34_WORD3_HELDOUT",f"{heldout:08X}")
    print("FIRST_CYCLE_PHASES",392,"96BIT_FULL_SEEDS",trials,
          "SOURCE_HELDOUT_MATCHES",len(surviving))
    assert trials==784 and surviving==[]
    print("SELECTED_K04_COUPON_AND_REC8_COMMITMENTS_UNREAD")


if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: python k04_n3_complete_firstcycle_seed.py ORIGINAL_ZIP")
    synthetic()
    original(sys.argv[1])
