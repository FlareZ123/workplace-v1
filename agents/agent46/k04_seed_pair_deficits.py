"""Inspect only bit-deficit positions adjacent to cross-source 227-pair runs.

A single additional complete pair around row7 could directly disclose the
third seed word of a shifted-origin 96-bit CPython numeric seed.
"""
from pathlib import Path
import sys
sys.path[:0]=[str(Path(__file__).resolve().parents[1]/"agent31"),
              str(Path(__file__).resolve().parent)]
from k04_mt_recursive_peel import close_group
from k04_cross_carrier_seed_windows import indexed_groups
ALL=0xffffffff

def main(source):
    words,clusters=indexed_groups(source,True)
    for row,delta in ((3,-1),(7,1),(9,2),(28,-1)):
        entries=next(entries for entries in clusters.values() if any(r==row for r,_ in entries))
        state,_=close_group(entries,words)
        start=dict(entries)[row]+delta
        print("GROUP",row,"physical_relative",start,flush=True)
        for j in range(-5,8):
            p=start+j
            m0,b0=state.get(p,(0,0))
            m1,b1=state.get(p+227,(0,0))
            print("PAIR",row,j,
                  f"p={p} mask0={m0:08X} bits0={b0:08X}",
                  f"mask1={m1:08X} bits1={b1:08X}",flush=True)
if __name__=="__main__":
    main(Path(sys.argv[1]))
