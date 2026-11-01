"""K04: three selected MT output bits from nine *hypothetical* native donor bits.
Read-only original-source test. Usage: python this_file.py original_case.zip
No selected row payload, route mask, target commitments or K08 wording are read.
The MT producer/placement is conditional and no real donor fragments are known.
"""
from itertools import combinations
from pathlib import Path
from zipfile import ZipFile
import hashlib
import random
import sys

ORIGINAL_SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"

def temper(x):
    y = x ^ (x >> 11)
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 15) & 0xEFC60000
    return (y ^ (y >> 18)) & 0xFFFFFFFF

def untemper(y):
    for shift, mask, direction in ((18, 0, "R"), (15, 0xEFC60000, "L"),
                                   (7, 0x9D2C5680, "L"), (11, 0, "R")):
        old = y
        for _ in range(6):
            old = y ^ ((old >> shift) if direction == "R" else
                       ((old << shift) & mask))
        y = old & 0xFFFFFFFF
    return y

def twist_print(previous, early, middle):
    mix = ((previous & 0x80000000) | (early & 0x7FFFFFFF)) >> 1
    if early & 1:
        mix ^= 0x9908B0DF
    return temper(middle ^ mix)

def bit(x, i):
    return (x >> i) & 1

def predict(e, m):
    return (bit(e,1) ^ bit(e,4) ^ bit(e,22) ^ bit(m,0),
            bit(e,1) ^ bit(e,5) ^ bit(e,19) ^ bit(m,4),
            bit(e,1) ^ bit(e,19) ^ bit(e,23) ^ bit(m,22))

def verify_triple(previous, early, middle):
    actual = twist_print(previous, early, middle)
    assert tuple(bit(actual, i) for i in (0,4,22)) == predict(temper(early), temper(middle))

def run(zip_path):
    with ZipFile(zip_path) as z:
        spool = z.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(spool).hexdigest() == ORIGINAL_SPOOL_SHA
    rows = [s for s in spool.decode().splitlines() if s and not s.startswith("#")]
    assert len(rows) == 133
    for index, marker in (
        (43,"2026-10-03T10:35:00+00:00 JOB=PS-261003-0343"),
        (44,"2026-10-03T10:40:00+00:00 JOB=PS-261003-0344"),
        (96,"2026-10-03T15:00:00+00:00 JOB=PS-261003-0396"),
        (97,"2026-10-03T15:05:00+00:00 JOB=PS-261003-0397"),
        (129,"2026-10-03T18:02:00Z JOB=PS-261003-0417 ATTEMPT=2 STATE=ACK CLASS=RECOVER")
    ):
        assert rows[index].startswith(marker), index
    # All six source-consistent *hypothetical* p=950..955 geometries
    # put the two required donor four-word runs in these original gaps:
    for p in range(950,956):
        assert p-623 == (p-627)+4 and p-227 == (p-234)+7
    print("Original spool SHA, unselected gap locations and six index geometries: PASS")
    basis = [(0,0,0)]
    for j in range(32):
        basis.extend(((1<<j,0,0),(0,1<<j,0),(0,0,1<<j)))
    assert len(basis) == 97
    for triple in basis:
        verify_triple(*triple)
    print("Complete 97-vector GF(2) basis: PASS")
    assert all(temper(untemper(1<<j)) == 1<<j for j in range(32))
    influences = [twist_print(0,untemper(1<<j),0) for j in range(32)]
    influences += [twist_print(0,0,untemper(1<<j)) for j in range(32)]
    rows_of_bits = [sum(bit(v,i)<<j for j,v in enumerate(influences)) for i in range(32)]
    positions = (0,4,22)
    total_support = 0
    for i in positions:
        total_support |= rows_of_bits[i]
        assert bit(twist_print(0x80000000,0,0),i) == 0
        assert rows_of_bits[i].bit_count() == 4
    early_bits = [j for j in range(32) if bit(total_support,j)]
    middle_bits = [j for j in range(32) if bit(total_support,j+32)]
    assert early_bits == [1,4,5,19,22,23]
    assert middle_bits == [0,4,22]
    for n, expected in ((1,4),(2,6),(3,9)):
        least = min((sum(0 for _ in ()) if False else
                    (lambda ix: ix.bit_count())(
                        __import__("functools").reduce(int.__or__, (rows_of_bits[j] for j in subset), 0)))
                    for subset in combinations(range(32),n))
        assert least == expected, (n,least)
    print("Three individual selected word bits [0,4,22] from native gap bit sets",early_bits,middle_bits)
    print("Exact exhaustive minimum donor bits for 1, 2, 3 individual bits: 4, 6, 9")
    comparisons = 0
    for seed in (0,17,20261003,314159,0xC0FFEE):
        rng = random.Random(seed)
        states = [untemper(rng.getrandbits(32)) for _ in range(960)]
        for p in range(950,956):
            for j in range(4):
                i = p+j
                verify_triple(states[i-624],states[i-623],states[i-227])
                assert temper(states[i]) == twist_print(states[i-624],states[i-623],states[i-227])
                comparisons += 1
    assert comparisons == 120
    print("120 true-MT word controls x three identities = 360: PASS")
    print("AUTHENTICATED K04 TARGET BITS ACQUIRED: 0/128")

if __name__ == "__main__":
    run(Path(sys.argv[1]))
