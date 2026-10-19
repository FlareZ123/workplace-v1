"""H-17 K04: seven-residue CPython seed-array period sieve from intact printer.
Usage: python k04_seven_residue_gate.py ORIGINAL_CASE_ZIP

Selected printer row129, original commitment, XOR mask, K08 and verifier unread.
Source-only hypothetical shared-MT / first-output-cycle producer model.
"""
import hashlib
import random
import re
import struct
import sys
import zipfile

M = 0xFFFFFFFF
SOURCE = 'evidence/print/spool-reconstruction.log'
SOURCE_SHA = '7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
POSITIONS = {3:-228,10:-170,33:-6,34:0,41:57,56:166,63:220,
             64:227,86:394,94:451,116:620,125:680}
BASE = [19650218]
for i in range(1, 624):
    BASE.append((1812433253 * (BASE[-1] ^ (BASE[-1] >> 30)) + i) & M)


def untemper(x):
    for shift, mask, left in ((18,M,False),(15,0xEFC60000,True),
                              (7,0x9D2C5680,True),(11,M,False)):
        a = x
        for _ in range(6):
            x = a ^ (((x << shift) & mask) if left else x >> shift)
        x &= M
    return x


def inverse_pair(a, b):
    v = a ^ b
    return (((v ^ (0x9908B0DF if v >> 31 else 0)) << 1) | (v >> 31)) & M


def twist(high, low):
    y = ((high & 1) << 31) | (low & 0x7FFFFFFF)
    return ((y >> 1) ^ (0x9908B0DF if y & 1 else 0)) & M


def infer(rows):
    state = {}

    def add(i, mask, value):
        mask &= M
        value &= mask
        oldmask, oldvalue = state.get(i, (0, 0))
        assert ((oldvalue ^ value) & oldmask & mask) == 0, ('inconsistent', i)
        if oldmask | mask == oldmask:
            return 0
        state[i] = oldmask | mask, oldvalue | value
        return 1

    for row, start in POSITIONS.items():
        for j, word in enumerate(rows[row]):
            add(start + j, M, word)
    for iteration in range(30):
        changed = 0
        for i, (mask, value) in list(state.items()):
            other = state.get(i + 227)
            if mask == M and other and other[0] == M:
                mixed = inverse_pair(value, other[1])
                changed += add(i - 397, 0x80000000, mixed)
                changed += add(i - 396, 0x7FFFFFFF, mixed)
        for i, (mask, value) in list(state.items()):
            nxt = state.get(i + 1)
            if not nxt or not mask & 0x80000000 or nxt[0] & 0x7FFFFFFF != 0x7FFFFFFF:
                continue
            t = twist(value >> 31, nxt[1])
            for left, right in ((i + 397, i + 624), (i + 624, i + 397)):
                neighbor = state.get(left)
                if neighbor and neighbor[0] == M:
                    changed += add(right, M, neighbor[1] ^ t)
        if not changed:
            break

    def window(a, b, width):
        assert all(state[x][0] == M for j in range(width) for x in (a + j, b + j))
        mixed = [inverse_pair(state[a + j][1], state[b + j][1]) for j in range(width)]
        full = [(mixed[j] & 0x7FFFFFFF) | (mixed[j + 1] & 0x80000000)
                for j in range(width - 1)]
        return full, mixed[-1] & 0x7FFFFFFF

    early = window(-396, -169, 3)  # S[p-168..p-167], S[p-166].low31
    late = window(-230, -3, 6)     # S[p-2..p+2], S[p+3].low31
    middle = window(-170, 57, 4)   # S[p+58..p+60], S[p+61].low31
    return early, late, middle


def mix(x, c):
    return ((x ^ (x >> 30)) * c) & M


def seed_term(a, b, c, i):
    previous = ((b + i - 1) ^ mix(a, 1566083941)) & M
    current = ((c + i) ^ mix(b, 1566083941)) & M
    return (current - (BASE[i] ^ mix(previous, 1664525))) & M


TERM_OFFSETS = (-166, 0, 1, 2, 3, 60, 61)


def terms(early, late, middle, p):
    (e, el), (l, ll), (m, ml) = early, late, middle
    patterns = {
        -166: (e[:2], el), 0: (l[:3], None),
        1: (l[1:4], None), 2: (l[2:5], None),
        3: (l[3:5], ll), 60: (m[:3], None),
        61: (m[1:3], ml),
    }
    result = {}
    for shift, (prefix, low) in patterns.items():
        i = p + shift
        if not 2 <= i <= 623:
            continue
        if low is None:
            result[shift] = {seed_term(*prefix, i)}
        else:
            result[shift] = {seed_term(prefix[0], prefix[1], low | bit, i)
                             for bit in (0, 0x80000000)}
    return result


def synthetic_controls():
    gaps = sorted({b - a for j, a in enumerate(TERM_OFFSETS)
                   for b in TERM_OFFSETS[j + 1:]})
    lengths = sorted({n for gap in gaps for n in range(1, gap + 1) if gap % n == 0})
    phases = (396, 445, 535, 562)
    count = 0
    for length in lengths:
        seed = sum((((i * 2654435761 + 0x12345678) & M) << (32 * i))
                   for i in range(length))
        expected = random.Random(seed).getstate()[1][:624]
        rng = random.Random(seed)
        generated = [untemper(rng.getrandbits(32)) for _ in range(562 + 684)]
        for p in phases:
            rows = {row: generated[p + rel:p + rel + 4]
                    for row, rel in POSITIONS.items()}
            early, late, middle = infer(rows)
            assert early[0] == list(expected[p - 168:p - 166])
            assert early[1] == (expected[p - 166] & 0x7FFFFFFF)
            assert late[0] == list(expected[p - 2:p + 3])
            assert late[1] == (expected[p + 3] & 0x7FFFFFFF)
            assert middle[0] == list(expected[p + 58:p + 61])
            assert middle[1] == (expected[p + 61] & 0x7FFFFFFF)
            t = terms(early, late, middle, p)
            for j, a in enumerate(TERM_OFFSETS):
                for b in TERM_OFFSETS[j + 1:]:
                    if a in t and b in t and (b - a) % length == 0:
                        assert t[a] & t[b], (length, p, a, b)
            count += 1
    return count, len(lengths)


def read_rows(zip_path):
    with zipfile.ZipFile(zip_path) as archive:
        spool = archive.read(SOURCE)
    assert hashlib.sha256(spool).hexdigest() == SOURCE_SHA
    lines = [line for line in spool.decode().splitlines() if line.startswith('2026-')]
    assert len(lines) == 133
    rows = {}
    for index in POSITIONS:
        assert index != 129
        raw = bytes.fromhex(re.search(r'PAYLOAD=([0-9A-F]{32})', lines[index]).group(1))
        rows[index] = [untemper(w) for w in struct.unpack('<4I', raw)]
    return rows


def main(zip_path):
    passed, lengths = synthetic_controls()
    early, late, middle = infer(read_rows(zip_path))
    assert early[0] == [0x0A9DE247, 0xFBBBB07E]
    assert late[0][1:] == [0x6CE0E225, 0xF4E8FCB2, 0xC517EB25, 0x7D3AAF35]
    print('synthetic_positive_tests', passed, 'array_lengths', lengths)
    for name, window in [('early', early), ('late', late), ('middle', middle)]:
        print(name, 'full', ' '.join(f'{x:08X}' for x in window[0]),
              'next_low31', f'{window[1]:08X}')
    for j, a in enumerate(TERM_OFFSETS):
        for b in TERM_OFFSETS[j + 1:]:
            valid = [p for p in range(396, 622)
                     if a in terms(early, late, middle, p)
                     and b in terms(early, late, middle, p)]
            matches = [p for p in valid
                       if (lambda t: t[a] & t[b])(terms(early, late, middle, p))]
            print('offsets', a, b, 'gap', b - a,
                  'tested_phases', len(valid), 'matches', len(matches))
    print('selected_row129_and_commitments_unread', True)
    print('K04_K08_UNRESOLVED')


if __name__ == '__main__':
    main(sys.argv[1])
