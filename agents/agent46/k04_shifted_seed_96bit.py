"""K04: cycle-aware 96-bit first-cycle seed inversion with unknown RNG prefix.

Scan all 393 possible initial-state positions for the original row3 window;
the original recorder/TRP2 bridge requires the printer to begin late if the
sources share an MT stream. Earlier first-cycle scans constrained row3 to
14..68 and thus did not test most shifted-origin positions.

Selected row129 and REC8 acceptance/mask withheld.
"""
from pathlib import Path
import random
import sys

AGENTS=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(AGENTS/"agent1"),str(AGENTS/"agent23")]
from k04_python_seed_fragments import extract_pairs,fragments,verify_seed,ALL
from k04_mt_rowstart import untemper

def synthetic():
    n=3
    for p in (0,14,310,392):
        seed=sum(((0x31415926+0x123fed*i)&ALL)<<(i*32) for i in range(n))
        generator=random.Random(seed)
        words=[untemper(generator.getrandbits(32)) for _ in range(624)]
        pairs=[(words[p+j],words[p+j+227]) for j in range(5)]
        recovered=fragments(pairs,p,n)
        assert recovered is not None and len(recovered)==2
        assert all(recovered[j]==((seed>>(32*j))&ALL) for j in recovered)
        assert verify_seed(seed,[(p,pairs)])
    print("SYNTHETIC_96BIT_TWO_WORD_FRAGMENTS_PASS",flush=True)

def main(source):
    original=extract_pairs(source)[0]
    two_word_fragments=0
    for phase in range(393):
        keys=fragments(original,phase,3)
        assert keys is not None and len(keys)==2
        two_word_fragments+=1
    print("selected_row129_withheld",True)
    print("first_cycle_phase_count",393)
    print("source_phase_assignments_with_two_of_three_key_words",two_word_fragments)
    print("96bit_source_seed_status", "UNDERDETERMINED_ONE_UNKNOWN_32BIT_WORD")
    print("K04_K08_UNRESOLVED")

if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("python k04_shifted_seed_96bit.py source.zip")
    synthetic()
    main(Path(sys.argv[1]))
