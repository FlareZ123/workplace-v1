"""Enumerate new 227-separated MT windows made available by cross-source bridges.

No K04 row129, commitments or mask are inspected. We seek additional
initialized-state windows to generalize the existing two-bridge seed inverter.
"""
from collections import defaultdict
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"agent23"))
from k04_mt_inverse_peel import groups, rows
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"agent31"))
from k04_mt_recursive_peel import close_group
ALL=0xffffffff

def indexed_groups(source,with_cross):
    value=rows(source)
    assert len(value)==133 and not value[129]
    original=groups(source,value)
    parent=list(range(133))
    delta=[0]*133
    def find(x):
        if parent[x]!=x:
            old=parent[x]
            root=find(old)
            delta[x]+=delta[old]
            parent[x]=root
        return parent[x]
    def equal(a,b,d):
        ra,rb=find(a),find(b)
        va,vb=delta[a],delta[b]
        if ra==rb:
            assert vb-va==d
        else:
            parent[rb]=ra
            delta[rb]=d+va-vb
    for root,entries in original.items():
        for row,offset in entries:equal(root,row,offset)
    if with_cross:
        for a,b,d in ((9,40,229),(7,38,230),(28,59,226)):
            equal(a,b,d)
    out=defaultdict(list)
    for row in range(133):
        if value[row]:out[find(row)].append((row,delta[row]))
    return value,out

def window_runs(state):
    available={i for i,(mask,_) in state.items() if mask==ALL}
    overlap={i for i in available if i+227 in available}
    runs=[]
    for i in sorted(overlap):
        if i-1 in overlap:continue
        j=i
        while j in overlap:j+=1
        if j-i>=2:runs.append((i,j-i))
    return runs

def main(source):
    for flag in (False,True):
        words,groups_=indexed_groups(source,flag)
        total=0
        print("SOURCE_BRIDGES_ENABLED",flag,"groups",len(groups_),flush=True)
        for root,entries in groups_.items():
            state,_=close_group(entries,words)
            rs=window_runs(state)
            for start,length in rs:
                total+=1
                print("WINDOW", "group",root,"rows",','.join(str(r) for r,_ in entries),
                      "index",start,"length",length,flush=True)
        print("RUNS_TOTAL",total,flush=True)

if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("python k04_cross_carrier_seed_windows.py source.zip")
    main(Path(sys.argv[1]))
