"""K04 cross-slot route constants as MT seed and hidden-window donors.

Usage: python agents/agent25/k04_route_constants_sft.py original-case.zip
Original selected spool row129 is withheld from inference. The two shared-RNG
hypotheses are conditional and not asserted as historical fact.
"""
import hashlib
import json
import random
import re
import struct
import sys
from collections import defaultdict
from itertools import permutations, product
from zipfile import ZipFile

ALL = 0xffffffff
MATRIX = 0x9908b0df

def untemper(x):
    for shift, left, mask in ((18,False,ALL),(15,True,0xefc60000),
                              (7,True,0x9d2c5680),(11,False,ALL)):
        y = x
        for _ in range(6):
            x = (y ^ ((x<<shift)&mask) if left else y ^ (x>>shift)) & ALL
    return x

def temper(x):
    x ^= x>>11
    x ^= (x<<7)&0x9d2c5680
    x ^= (x<<15)&0xefc60000
    return (x ^ (x>>18)) & ALL

def twist(a,b):
    y = (a & 0x80000000) | (b & 0x7fffffff)
    return ((y>>1) ^ (MATRIX if y&1 else 0)) & ALL

def seed_hits(seed, target, limit=65536):
    stream = random.Random(seed).randbytes(4*limit)
    return [i//4 for i in range(0,len(stream)-15,4)
            if stream[i:i+16]==target]

def donor_witnesses(donors, source_words):
    by_value = defaultdict(list)
    for row,col,word in source_words:
        by_value[word].append((row,col))
    found = []
    for name,endian,run in donors:
        for i in range(3):
            delta = twist(run[i],run[i+1])
            for row,col,mid in source_words:
                for later,other_col in by_value.get(delta^mid,()):
                    if later>row:
                        found.append((name,endian,i,row,col,later,other_col))
    return found

def main(path):
    with ZipFile(path) as z:
        route = json.loads(z.read('evidence/recovery-routing.json'))
        acceptance = json.loads(z.read('acceptance.json'))
        spool = z.read('evidence/print/spool-reconstruction.log')
    assert hashlib.sha256(spool).hexdigest()==(
        '7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083')
    payloads = [bytes.fromhex(b.decode()) for b in
                re.findall(rb'PAYLOAD=([0-9A-F]{32})',spool)]
    assert len(payloads)==133
    words = [(row,j,untemper(w)) for row,payload in enumerate(payloads)
             if row!=129 for j,w in enumerate(struct.unpack('<4I',payload))]
    assert len(words)==528
    source = {
        'K04_mask':bytes.fromhex(route['K04']['masked_component']),
        'K08_nonce':bytes.fromhex(route['K08']['desk_nonce'])
    }

    # Untouched synthetic positive tests for seed and recurrence predictors.
    seed = b'H17-SYNTHETIC-CONTROL'
    rng = random.Random(seed)
    stream = rng.randbytes(4*16385)
    assert 16000 in seed_hits(seed,stream[64000:64016],16385)
    rng = random.Random(789)
    state = [untemper(rng.getrandbits(32)) for _ in range(625)]
    fake = [(i,0,state[i]) for i in (397,398,399,624)]
    assert donor_witnesses([('control','little',state[:4])],fake)
    print('synthetic_controls', 'PASS')

    seed_results = []
    for name,value in source.items():
        h = value.hex().upper()
        recipes = {'bytes':value,'hex_upper':h,'hex_lower':h.lower(),
                   'integer_big':int.from_bytes(value,'big'),
                   'integer_little':int.from_bytes(value,'little'),
                   'ascii_hex':h.encode()}
        for recipe,seed in recipes.items():
            for pos in seed_hits(seed,payloads[3]):
                seed_results.append((name,recipe,pos))
    print('seed_recipes',12,'words_per_seed',65536,
          'intact_row3_matches',seed_results)

    donors = [(name,endian,[untemper(w) for w in struct.unpack(
             ('<4I' if endian=='little' else '>4I'),value)])
             for name,value in source.items() for endian in ('little','big')]
    print('commissioning_donor_runs',4,'adjacent_pairs',12,
          'intact_recurrence_witnesses',donor_witnesses(donors,words))

    # Conditional placement d=11, p=627: X[4..7] and X[400..403]
    # are the two route constants, X[3] comes from intact row43.
    state3 = untemper(struct.unpack('<4I',payloads[43])[3])
    commitment = acceptance['slot_sha256']['K04']
    accepted = []
    count = 0
    for next_name,mid_name in permutations(source,2):
        for a_endian,b_endian in product('><',repeat=2):
            next_words = [untemper(w) for w in struct.unpack(
                a_endian+'4I',source[next_name])]
            mid_words = [untemper(w) for w in struct.unpack(
                b_endian+'4I',source[mid_name])]
            predecessor = [state3]+next_words[:-1]
            payload = struct.pack('<4I',*(temper(mid_words[i]^twist(
                predecessor[i],next_words[i])) for i in range(4)))
            coupon = bytes(x^y for x,y in zip(payload,source['K04_mask']))
            count += 1
            if hashlib.sha256(coupon).hexdigest()==commitment:
                accepted.append((next_name,mid_name,a_endian,
                                 b_endian,coupon.hex().upper()))
    print('conditional_d11_p627_candidates',count,'accepted',accepted)
    print('K08_final_words_unknown',True)

if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('usage: python k04_route_constants_sft.py original-case.zip')
    main(sys.argv[1])
