"""Source-only K04: reconstruct all four CPython 32-bit integer seed words.

Usage: python agents/agent8/k04_n4_two_partial_seed_completion.py ORIGINAL_ZIP

Reuses the source-pinned AX5..7/row9 window from Agent28 and the independent
row3/34 partial state window from Agent41. No selected row129, original mask,
acceptance commitment, K08 text or verifier is read. A source-only intact
row33 word3 is withheld as the full 32-bit prediction target.
"""
import hashlib
import itertools
import random
import re
import struct
import sys
import zipfile
from pathlib import Path

sys.path[:0] = [
    str(Path(__file__).resolve().parents[1] / "agent28"),
    str(Path(__file__).resolve().parents[1] / "agent41"),
]
import k04_row9_ax_seed_gates as mt
import k04_gap6_period175_two_partial as witness

LOW = 0x7FFFFFFF
TOP = 0x80000000
MASK = 0xFFFFFFFF


def candidate_seeds(p, early, late):
    """Four seed possibilities from two full and two low31 seed words."""
    assert 402 <= p <= 620
    residues = {}
    for index, triple in ((p+1, late[:3]), (p+2, late[1:4])):
        key_index = (index-1) % 4
        residues[key_index] = [(mt.plus(*triple, index)-key_index) & MASK]
    for index, triple in ((p-172, early), (p+3, late[2:5])):
        key_index = (index-1) % 4
        assert key_index not in residues
        low = (mt.plus(*triple, index)-key_index) & LOW
        residues[key_index] = [low, low | TOP]
    assert len(residues) == 4
    assert sorted(len(x) for x in residues.values()) == [1,1,2,2]
    return [
        sum(word << (32*j) for j, word in enumerate(words))
        for words in itertools.product(*(residues[j] for j in range(4)))
    ]


def heldout_word(seed, p):
    rng = random.Random(seed)
    for _ in range(p-3):
        rng.getrandbits(32)
    return rng.getrandbits(32)


def actual_seeded_controls():
    tested = 0
    for p in (402,404,430,535,562,620):
        for trial in range(15):
            words = [
                (0x1234567A + trial*0x97F4A7C5 + j*0x9E3779B9) & MASK
                for j in range(4)
            ]
            seed = sum(w << (32*j) for j,w in enumerate(words))
            rng = random.Random(seed)
            state = list(rng.getstate()[1][:624])
            out = [mt.untemper(rng.getrandbits(32)) for _ in range(p+228)]
            ax = [mt.temper(w)>>16 for w in out[p-402:p-399]]
            ancestors = mt.ancestor(out[p-6:p-2], out[p+220:p+224], ax)
            early_full, early_low = mt.early(ancestors, out[p-176:p-172], 6)
            early = [*early_full, early_low]
            assert early == [state[p-174],state[p-173],state[p-172]&LOW]
            inverse = [
                mt.invpair(out[p-227+j], out[p+j]) for j in range(3)
            ]
            late = [
                state[p-1],state[p],
                (inverse[0]&LOW)|(inverse[1]&TOP),
                (inverse[1]&LOW)|(inverse[2]&TOP),
                inverse[2]&LOW,
            ]
            assert late == state[p-1:p+3]+[state[p+3]&LOW]
            proposals = candidate_seeds(p, early, late)
            assert len(proposals) == 4 and seed in proposals
            expected = mt.temper(out[p-3])
            matches = [s for s in proposals if heldout_word(s,p)==expected]
            assert matches == [seed], (p,trial,matches)
            tested += 1
    assert tested == 90
    print("ACTUAL_PYTHON_SEEDED_FULL_WINDOW_RECOVERY_CONTROLS_PASS", tested)


def original(path):
    early, late_tail = witness.source(path)
    late = [*mt.LATE[:2], *late_tail]
    assert early == (0x418BDA1E,0x2E02BC3D,0x38EBB043)
    assert late == [
        0x6CE0E225,0xF4E8FCB2,0xC517EB25,0x7D3AAF35,0x31FD69FC
    ]
    with zipfile.ZipFile(path) as archive:
        spool = archive.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(spool).hexdigest() == mt.P_SHA
    lines = [s for s in spool.decode().splitlines() if s.startswith("2026-")]
    assert len(lines) == 133
    payload = bytes.fromhex(re.search(
        r"PAYLOAD=([0-9A-F]{32})", lines[33]
    ).group(1))
    heldout = struct.unpack("<4I", payload)[3]
    assert heldout == 0x910E0FB0

    survivors = []
    checked = 0
    for phase in range(402,621):
        for seed in candidate_seeds(phase,early,late):
            checked += 1
            if heldout_word(seed, phase) == heldout:
                survivors.append((phase,seed))
    print("SOURCE_EARLY_S_pminus174_173_and_pminus172_low31",
          [f"{x:08X}" for x in early])
    print("SOURCE_LATE_S_pminus1_to_pplus2_and_pplus3_low31",
          [f"{x:08X}" for x in late])
    print("INDEPENDENT_ROW33_WORD3_HELDOUT", f"{heldout:08X}")
    print("N4_FIRSTCYCLE_PHASES", 219,
          "COMPLETE_128BIT_SEED_CANDIDATES", checked,
          "SOURCE_HELDOUT_MATCHES", len(survivors))
    assert checked == 876 and survivors == []
    print("ORIGINAL_K04_K08_AND_COMMITMENTS_UNREAD")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_n4_two_partial_seed_completion.py ORIGINAL_ZIP")
    actual_seeded_controls()
    original(sys.argv[1])
