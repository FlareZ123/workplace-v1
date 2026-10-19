"""Recover five withheld original MT printer selector state words from two-twist quartets.

Original H-17 43-member ZIP required. Original selected row129, recovery mask,
all original commitment digests and nonce are deliberately excluded.
"""
import random
import sys

from k04_source_dest_parity_projection import original_rows, temper, untemper

A=0x9908B0DF
KEEP=0xBFFFFFFF
MSB=0x80000000

def f(y):
    x=y & 0x7FFFFFFF
    return ((x>>1) ^ (A if x&1 else 0)) & KEEP

def invf(v):
    bit=v>>31
    return ((((v^(A if bit else 0))<<1)&0x7FFFFFFF)|bit)

def predict_first(rows,b,c,d,shift):
    """Predict only low31 at shifted first position of a valid anchored quartet."""
    def word(label):
        r,j=label
        assert 0<=j+shift<4
        return rows[r][j+shift]
    result=((word(d)^word(c))&KEEP)^f(word(b))
    return invf(result)

def restrict(lo,bits,allowed,why):
    found=[state for state in (lo,lo|MSB) if temper(state)>>(32-bits) in allowed]
    assert len(found)==1,(why,hex(lo),found)
    return found[0]

def synthetic():
    rng=random.Random(20261019)
    for _ in range(1024):
        w=untemper(rng.getrandbits(32))
        assert invf(f(w))==w&0x7FFFFFFF
    print("1024 genuine MT temper inversion/31-bit function controls PASS")

def recover(zip_path):
    rows,classes,dests=original_rows(zip_path)
    # The three independent original 31-bit quartets are verified directly.
    originals=[
        ((4,3),(35,0),(58,0),(118,1)),
        ((5,3),(36,0),(59,1),(119,3)),
        ((9,2),(40,0),(63,0),(124,0)),
    ]
    # Original quadruple check uses only 528 intact printer words.
    for a,b,c,d in originals:
        assert ((rows[d[0]][d[1]]^rows[c[0]][c[1]])&KEEP)==(
            f(rows[a[0]][a[1]])^f(rows[b[0]][b[1]]))
    q4,q5,q9=originals
    selected={}
    def save(row,relative,lo,bits,allowed,why):
        w=restrict(lo,bits,allowed,why)
        selected[(row,relative)]=w
        print(why,"latent untempered",f"{w:08X}","tempered",f"{temper(w):08X}",
              "sample code",temper(w)>>(32-bits))
    assert dests[4]==0 and dests[9]==0 and classes[36]==0
    # Row4's next two draws must be DEST rejects: each can only be code1 or code3.
    for n in (1,2):
        lo=predict_first(rows,*q4[1:],shift=n)
        save(4,3+n,lo,2,{3},"original r4 DEST reject "+str(n))
    # Row9 first DEST must reject. Following first accepted DEST is the required store.
    lo=predict_first(rows,*q9[1:],shift=2)
    save(9,4,lo,2,{3},"original r9 DEST reject")
    lo=predict_first(rows,*q9[1:],shift=3)
    save(9,5,lo,2,{0},"original r9 DEST accept store")
    # Earlier r5 triple and r59/r119 post relations fix the accepted CLASS for r36.
    lo=invf(((rows[119][2]^rows[59][0])&KEEP)^f(rows[5][2]))
    save(36,-1,lo,3,{0},"original r36 final CLASS accept LABEL")
    assert selected=={
        (4,4):0x81BB818B,
        (4,5):0x8AF3AD7E,
        (9,4):0x8DAE2276,
        (9,5):0xDE28452A,
        (36,-1):0xA0EB5B13,
    }
    print("FIVE newly source-reconstructed full original latent MT words; original row129 omitted.")
    print("Original MT producer and sampler causal assumptions remain conditional.")
    return selected

if __name__=="__main__":
    synthetic()
    if len(sys.argv)>1:
        recover(sys.argv[1])
