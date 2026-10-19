"""Bound CPython first-cycle seeded inversion windows by source-linked MT prefix.

Usage: python agents/agent43/k04_firstcycle_gate.py original-case.zip
Reads only original source; selected printer row129 and REC8 commitments withheld.
"""
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from k04_prefix_shared_controls import calculate,discover,inspect_source


def row_bounds(source,floor):
    within,boundary=discover(source)
    controls=inspect_source(source)
    edges=[]
    def same(a,b,delta):
        edges.append((a,b,delta))
        edges.append((b,a,-delta))
    for (a,j),(b,k),(c,l) in within:
        same(a,b,397+j-k)
        same(a,c,624+j-l)
    for a,bit,(b,k),(c,l) in boundary:
        same(a,b,396-k)
        same(a,c,623-l)
    for r in range(132):
        edges.append((r+1,r,-(floor if r<127 else 4)))
    for name,payload,a,j,b,k in controls:
        same(a,b,227+j-k)
    def upper(start,end):
        d=[float("inf")]*133
        d[start]=0
        for _ in range(132):
            changed=False
            for a,b,c in edges:
                if d[a]+c<d[b]:
                    d[b]=d[a]+c
                    changed=True
            if not changed:
                break
        assert not any(d[a]+c<d[b] for a,b,c in edges)
        return d[end]
    return {r:(-upper(r,0),upper(0,r)) for r in (3,10,13)}


def main(source):
    bounds=row_bounds(source,6)
    assert bounds=={3:(21,25),10:(74,84),13:(102,112)},bounds
    prefix=calculate(source,6)[0][0]
    assert prefix==335
    start3_min=prefix+bounds[3][0]-1
    start10_min=prefix+bounds[10][0]
    start13_min=prefix+bounds[13][0]-1
    # Four adjacent 227-separated pairs must start by 623-(227+3)=393.
    # Five such pairs must start by 623-(227+4)=392.
    assert (start3_min,start10_min,start13_min)==(355,409,436)
    assert start3_min<=392 and start10_min>393 and start13_min>392
    print("selected_row129_and_acceptance_withheld",True)
    print("model","one common MT stream, CRC-valid TRP/RC17 controls, six-draw regular floor")
    print("absolute_first_printer_index_min",prefix)
    print("firstcycle_row3_five_pair_start_min",start3_min,"latest",392)
    print("firstcycle_row10_four_pair_start_min",start10_min,"latest",393,
          "first_cycle_ELIMINATED",True)
    print("firstcycle_row13_five_pair_start_min",start13_min,"latest",392,
          "first_cycle_ELIMINATED",True)
    print("consequence","only row3 eligible among these three; cycle-aware later windows required")
    print("K04_K08_UNRESOLVED")


if __name__=="__main__":
    main(Path(sys.argv[1]))
