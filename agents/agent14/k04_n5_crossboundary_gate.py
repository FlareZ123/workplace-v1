"""Source-only cross-boundary initialized-state bridge for CPython five-word seeds.

Tests p=568..620. Selected row129, REC8 commitments, masks and K08 withheld.
Run: python k04_n5_crossboundary_gate.py original-case.zip
"""
import random
import sys
from k04_ax_seed_divisor_gate import (
    MASK, LATE, seed_word, INITIAL, initialized_state, source_window,
    untemper, inverse_twist, initialized_pair)
from k04_n5_three_window_seed import source_rows, partial_key


def bridge(first, second, earlier):
    """Cross-cycle row10/41 output ancestors and one initialized-state word."""
    mixed = [inverse_twist(x, y) for x, y in zip(first, second)]
    earlyoutputs = [(mixed[i] & 0x7fffffff) | (mixed[i+1] & 0x80000000)
                    for i in range(3)]
    # For p>=567 these are first-cycle X[p-566..p-564].
    pair1 = inverse_twist(earlyoutputs[1], earlier[0])
    pair2 = inverse_twist(earlyoutputs[2], earlier[1])
    initial = (pair1 & 0x7fffffff) | (pair2 & 0x80000000)
    return initial, earlyoutputs, pair1 & 0x80000000, pair2 & 0x7fffffff


N = 5
INV1664 = pow(1664525, -1, 1 << 32)
INV1566 = pow(1566083941, -1, 1 << 32)


def multiplier(value, factor):
    return ((value ^ (value >> 30)) * factor) & MASK


def inv_multiplier(value, inverse):
    x = (value * inverse) & MASK
    return x ^ (x >> 30)


def previous(b, c, key, index, n):
    ki = (index - 1) % n
    second = (c + index) ^ multiplier(b, 1566083941)
    first = inv_multiplier(INITIAL[index] ^ ((second - key - ki) & MASK), INV1664)
    return inv_multiplier(first ^ ((b + index - 1) & MASK), INV1566)


def twist(a, b):
    v = (a & 0x80000000) | (b & 0x7fffffff)
    return (v >> 1) ^ (0x9908b0df if v & 1 else 0)


def test(p, late, earlier, earlyx, source_s3, partial_s4, high_s2, partial_late):
    j = p - 567
    keys = {}
    for ii in (p+1, p+2):
        ki = (ii-1) % N
        keys[ki] = (seed_word(*late[ii-p-1:ii-p+2], ii) - ki) & MASK
    candidates = []
    for upper in (0, 0x80000000):
        s4 = partial_s4 | upper
        s2 = previous(source_s3, s4, keys[(j+3) % N], j+4, N)
        if s2 & 0x80000000 != high_s2:
            continue
        s1 = previous(s2, source_s3, keys[(j+2) % N], j+3, N)
        s398 = earlyx[0] ^ twist(s1, s2)
        index = j + 400
        k = (index-1) % N
        derived_key = (seed_word(s398, *earlier, index) - k) & MASK
        candidates.append((upper, derived_key & 0x7fffffff == partial_late, derived_key))
    return candidates


def synthetic():
    count = 0
    for p in range(568, 621):
        seed = sum((0xA1245687 + 0x51317*k) << (32*k) for k in range(N))
        rng = random.Random(seed)
        x = [untemper(rng.getrandbits(32)) for _ in range(p+231)]
        state = initialized_state(seed)
        pre = initialized_pair(x[p:p+4], x[p+227:p+231])
        earlier = initialized_pair(pre, x[p-169:p-166])
        late = initialized_pair(x[p-229:p-224], x[p-2:p+3])
        tail = inverse_twist(x[p-225], x[p+2]) & 0x7fffffff
        s3, earlyx, high_s2, low_s4 = bridge(x[p-170:p-166],
                                             x[p+57:p+61], earlier)
        recovered = partial_key(p+3, late[2], late[3], tail, N)
        hits = test(p, late, earlier, earlyx, s3, low_s4, high_s2, recovered)
        assert sum(hit[1] for hit in hits) == 1, (p, hits)
        winner = next(hit for hit in hits if hit[1])
        assert winner[2] == ((seed >> (32*((p+2) % 5))) & MASK)
        assert s3 == state[p-564]
        count += 1
    print('SYNTHETIC_CROSSBOUNDARY_SEED_BRIDGE_PASS', count)


def original(zip_path):
    rows = source_rows(zip_path)
    earlier, _ = source_window(zip_path)
    late = LATE
    s3, earlyx, high_s2, low_s4 = bridge(rows[10], rows[41], earlier)
    tail = inverse_twist(rows[3][3], rows[34][2]) & 0x7fffffff
    assert tail == 0x31FD69FC
    print('SOURCE_S[p-564]', f'{s3:08X}')
    print('SOURCE_S[p-563]_LOW31', f'{low_s4:08X}')
    print('SOURCE_S[p-565]_TOP', int(bool(high_s2)))
    third_key_partial = partial_key(568+3, late[2], late[3], tail, N)
    survivors = []
    precondition_pass = 0
    for p in range(568, 621):
        # Partial third-key fingerprint depends on phase; derive for each p.
        third_key_partial = partial_key(p+3, late[2], late[3], tail, N)
        hits = test(p, late, earlier, earlyx, s3, low_s4, high_s2,
                    third_key_partial)
        precondition_pass += len(hits)
        for upper, match, word in hits:
            if match:
                survivors.append((p, upper, f'{word:08X}'))
    print('SOURCE_PHASES', 53, 'TOPBIT_PRECONDITION_BRANCHES', precondition_pass)
    print('THIRD_KEY_LOW31_MATCHES', survivors)
    print('K04_K08_MISSING; no acceptance read')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python k04_n5_crossboundary_gate.py case.zip')
    synthetic()
    original(sys.argv[1])
