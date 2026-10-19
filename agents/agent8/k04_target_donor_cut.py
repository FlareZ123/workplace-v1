"""K04 source-indexed donor cut: count external anchors touching target groups.

Run: python agents/agent8/k04_target_donor_cut.py ORIGINAL_ZIP

No selected ACK source, acceptance, mask, K08, or verifier is read. The
seven external relations are *conditional* index claims cited in report;
the original 42 printer witnesses are recomputed from the SHA-pinned spool.
This certifies source-index topology, not physical common-RNG provenance.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"agent23"))
from k04_mt_rowstart import discover

ORIGINAL_RELATIONS = (
    ("TRP2 rec40/12",9,40),
    ("TRP2 rec28/17/72/45",10,41),
    ("TRP2 rec26",7,38),
    ("RC17 withdrawn B strips",28,59),
    ("AX7778 seq2-3",33,63),
    ("AX7778 seq5-7",34,64),
    ("AX7778 contiguous-checkpoint assumption",33,34),
)


def inspect(original_zip):
    within,boundary=discover(original_zip)
    assert len(within)==25 and len(boundary)==17
    parent={j:j for j in range(133) if j!=129}

    def root(j):
        while parent[j]!=j:
            parent[j]=parent[parent[j]]
            j=parent[j]
        return j

    def join(a,b):
        a,b=root(a),root(b)
        if a!=b:parent[b]=a

    for (r,j),(m,k),(t,l) in within:
        join(r,m)
        join(r,t)
    for r,bit,(m,k),(t,l) in boundary:
        join(r,m)
        join(r,t)

    before={r:root(r) for r in parent}
    target={before[43],before[44]}
    assert len(target)==2
    print("SELECTED_SPOOL_ROW129_WITHHELD",True)
    print("PRINTER_RECURRENCE_WITNESSES",len(within)+len(boundary))
    print("PRINTER_SOURCE_COMPONENTS",len(set(before.values())))
    for row in (43,44):
        print("TARGET_GROUP",row,"ROWS",[
            r for r in before if before[r]==before[row]
        ])

    touched=0
    for label,a,b in ORIGINAL_RELATIONS:
        in_target=before[a] in target or before[b] in target
        touched+=in_target
        print("SOURCE_ANCHOR",label,"FROM",a,"TO",b,
              "TOUCHES_TARGET",bool(in_target))
        join(a,b)

    print("ALL_SEVEN_CONDITIONAL_EXTERNAL_LINKS_COMPONENTS",
          len(set(root(r) for r in parent)))
    print("TARGET_GROUPS_STILL_DISCONNECTED",root(43)!=root(44))
    print("SOURCE_EXTERNAL_ANCHORS_TOUCHING_TARGET",touched)
    assert touched==0
    assert root(43)!=root(44)
    assert len(set(root(r) for r in parent))==77
    print("NEED_FRESH_INDEPENDENT_SOURCE_LINKS_TO_BOTH_TARGET_GROUPS")


if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: python k04_target_donor_cut.py ORIGINAL_ZIP")
    inspect(sys.argv[1])
