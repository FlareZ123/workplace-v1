"""K04 conditional common-stream MT prefix lower bound from original control bytes.

Usage: python agents/agent43/k04_prefix_shared_controls.py original-case.zip
Selected printer row129 and original REC8 commitments are deliberately withheld.
"""
import hashlib
import re
import struct
import sys
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'agent23'))
from k04_mt_rowstart import discover, untemper, SHA, SPOOL

A = 0x9908B0DF
H = 0x7FFFFFFF


def inverse_twist(v):
    parity = v >> 31
    return (((v ^ (A if parity else 0)) << 1) | parity) & 0xFFFFFFFF


def inspect_source(path):
    with ZipFile(path) as archive:
        spool = archive.read(SPOOL)
        trp = archive.read('evidence/recorder/trip-recorder.raw')
        rc17 = archive.read('evidence/procedures/RC-17-scans.txt').decode()
    assert hashlib.sha256(spool).hexdigest() == SHA
    lines = [line for line in spool.decode().splitlines() if line.startswith('2026-')]
    assert len(lines) == 133
    words = [[untemper(w) for w in struct.unpack('<4I', bytes.fromhex(
        re.search(r'PAYLOAD=([0-9A-F]{32})', line).group(1)))] for line in lines]
    words[129] = []
    assert trp[:8] == b'TRP2DUMP' and struct.unpack_from('<I', trp, 12)[0] == 88
    assert len(trp) == 16 + 24 * 88
    controls = [(i, trp[16+24*i+12:16+24*i+16]) for i in (26, 40, 12, 28, 17, 72, 45)]
    strips = re.findall(r'Footer control strip: ([A-F0-9]{8})', rc17)
    assert len(strips) == 12
    records = [(f'TRP2#{i}', c, a, j, b, k) for (i, c), (a,j,b,k) in zip(controls, [
        (7,3,38,0), (9,2,40,0), (9,3,40,1), (10,0,41,0),
        (10,1,41,1), (10,2,41,2), (10,3,41,3)])]
    records += [('RC17-B-PURGE', bytes.fromhex('759E0027'), 28,2,59,3),
                ('RC17-B-VERIFY', bytes.fromhex('C130C9BB'),28,1,59,2)]
    assert '759E0027' in strips and 'C130C9BB' in strips
    for name, payload, a, j, b, k in records:
        inferred = inverse_twist(words[a][j] ^ words[b][k])
        original = untemper(struct.unpack('<I', payload)[0])
        assert inferred & H == original & H, (name, inferred, original)
    return records


def calculate(path, regular_floor):
    within, boundary = discover(path)
    assert (len(within), len(boundary)) == (25, 17)
    records = inspect_source(path)
    edges = []
    def eq(a,b,d):
        edges.append((a,b,d))
        edges.append((b,a,-d))
    for (a,j),(b,k),(c,l) in within:
        eq(a,b,397+j-k)
        eq(a,c,624+j-l)
    for a,bit,(b,k),(c,l) in boundary:
        eq(a,b,396-k)
        eq(a,c,623-l)
    for row in range(132):
        edges.append((row+1,row, -(regular_floor if row<127 else 4)))
    for name,raw,a,j,b,k in records:
        eq(a,b,227+j-k)

    distance=[float('inf')]*133
    distance[0]=0
    for _ in range(132):
        changed=False
        for u,v,d in edges:
            if distance[u]+d<distance[v]:
                distance[v]=distance[u]+d
                changed=True
        if not changed:
            break
    assert not any(distance[u]+d<distance[v] for u,v,d in edges)

    # A source-matched recurrence middle word at s[a]+j has an earlier
    # state predecessor at s[a]+j-397; absolute MT output indices start at 0.
    bounds = [(397-j-distance[a],name,a,j) for name,raw,a,j,b,k in records]
    return sorted(bounds,reverse=True)


def main(source):
    for regular_floor, expected in [(4,307),(6,335)]:
        results=calculate(source,regular_floor)
        assert results[0][0] == expected,results
        print('ordinary_minimum_gap',regular_floor,'first_printer_absolute_index_at_least',expected)
        for bound,name,row,column in results:
            print(' ',name,'middle_row',row,'column',column,'minimum_s0',bound)
    print('source_only_recorder_RC17_bridge_model_conditional; selected_row129_withheld; K04_K08_UNRESOLVED')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
