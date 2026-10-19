"""K04 cross-cycle 31-bit CPython init_by_array seed-length discriminator.

Run: python k04_ax_seed_divisor_gate.py c-energy-group-documents2026.zip
Uses only intact source spool and AX-derived MT alignment, not row129, the
K04 mask, K08 data, REC8 commitments or a recovery checker.
"""
import hashlib
import random
import re
import struct
import sys
import zipfile

MASK = 0xFFFFFFFF
SPOOL_HASH = '7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
TRANSFER_HASH = '32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf'
LATE = [0x6CE0E225, 0xF4E8FCB2, 0xC517EB25, 0x7D3AAF35]


def untemper(value):
    x = value
    for shift, mask, left in ((18, MASK, False), (15, 0xEFC60000, True),
                              (7, 0x9D2C5680, True), (11, MASK, False)):
        base = x
        for _ in range(6):
            x = base ^ (((x << shift) & mask) if left else x >> shift)
        x &= MASK
    return x


def inverse_twist(a, b):
    z = a ^ b
    bit = z >> 31
    return (((z ^ (0x9908B0DF if bit else 0)) << 1) | bit) & MASK


def initialized_pair(left, right):
    mixed = [inverse_twist(a, b) for a, b in zip(left, right)]
    return [(mixed[j] & 0x7FFFFFFF) | (mixed[j + 1] & 0x80000000)
            for j in range(len(mixed) - 1)]


def constants():
    state = [19650218]
    for i in range(1, 624):
        state.append((1812433253 * (state[-1] ^ (state[-1] >> 30)) + i) & MASK)
    return state


INITIAL = constants()


def seed_word(a, b, c, index):
    first = ((b + index - 1) ^ ((a ^ (a >> 30)) * 1566083941)) & MASK
    second = ((c + index) ^ ((b ^ (b >> 30)) * 1566083941)) & MASK
    return (second - (INITIAL[index] ^ ((first ^ (first >> 30)) * 1664525))) & MASK


def next_state(a, b, key, index, count):
    key_index = (index - 1) % count
    first = (b + index - 1) ^ (((a ^ (a >> 30)) * 1566083941) & MASK)
    second = (INITIAL[index] ^ (((first ^ (first >> 30)) * 1664525) & MASK)) + key + key_index
    return (((second & MASK) ^ (((b ^ (b >> 30)) * 1566083941) & MASK)) - index) & MASK


def initialized_state(seed):
    words = []
    while seed:
        words.append(seed & MASK)
        seed >>= 32
    if not words:
        words = [0]
    state = INITIAL.copy()
    i, j = 1, 0
    for _ in range(max(624, len(words))):
        state[i] = ((state[i] ^ ((state[i-1] ^ (state[i-1] >> 30)) * 1664525)) + words[j] + j) & MASK
        i += 1
        j = (j + 1) % len(words)
        if i == 624:
            state[0], i = state[623], 1
    for _ in range(623):
        state[i] = ((state[i] ^ ((state[i-1] ^ (state[i-1] >> 30)) * 1566083941)) - i) & MASK
        i += 1
        if i == 624:
            state[0], i = state[623], 1
    state[0] = 0x80000000
    return state


def source_window(zip_path):
    with zipfile.ZipFile(zip_path) as archive:
        spool = archive.read('evidence/print/spool-reconstruction.log')
        transfer = archive.read('evidence/transfers/transfer-audit.jsonl')
    assert hashlib.sha256(spool).hexdigest() == SPOOL_HASH
    assert hashlib.sha256(transfer).hexdigest() == TRANSFER_HASH
    records = [line for line in spool.decode().splitlines() if line.startswith('2026-')]
    assert len(records) == 133
    def states(row):
        # Never inspect the disputed selected row129.
        assert row in (10, 34, 64)
        hex_data = re.search(r'PAYLOAD=([0-9A-F]{32})', records[row]).group(1)
        return [untemper(w) for w in struct.unpack('<4I', bytes.fromhex(hex_data))]
    early_printer, middle, late = states(10), states(34), states(64)
    # From the source-matched AX-7778 row34/64 227-draw bridge.
    predecessor = initialized_pair(middle, late)
    assert predecessor == [0xBFD3ACA1, 0xEF2DD8BC, 0x611914B2]
    halves = [inverse_twist(a, b) for a, b in zip(predecessor, early_printer[1:4])]
    earlier = [(halves[j] & 0x7FFFFFFF) | (halves[j + 1] & 0x80000000) for j in range(2)]
    assert earlier == [0x0A9DE247, 0xFBBBB07E]
    # Previously unutilized low 31 bits of the third inverse-twist result.
    return earlier, halves[2] & 0x7FFFFFFF


def gate(phase, earlier, late, observed_low31, key_count):
    keys = {}
    for j in (2, 3):
        index = phase - 1 + j
        slot = (index - 1) % key_count
        val = (seed_word(*late[j-2:j+1], index) - slot) & MASK
        if slot in keys and keys[slot] != val:
            return 'quartet_conflict'
        keys[slot] = val
    index = phase - 166
    key_slot = (index - 1) % key_count
    if key_slot not in keys:
        return 'unknown_key'
    prediction = next_state(*earlier, keys[key_slot], index, key_count)
    return 'match' if prediction & 0x7FFFFFFF == observed_low31 else 'mismatch'


def synthetic_controls():
    count = 0
    for phase in (396, 400, 500, 535, 555, 584, 605, 621):
        for key_count in (1, 2, 3, 4, 6, 7, 8):
            seed = sum((0xA1234567 + j * 0x12BCD3) << (32*j) for j in range(key_count))
            state = initialized_state(seed)
            assert state == list(random.Random(seed).getstate()[1][:-1])
            rng = random.Random(seed)
            output = [untemper(rng.getrandbits(32)) for _ in range(phase + 231)]
            predecessor = initialized_pair(output[phase:phase+4], output[phase+227:phase+231])
            early = initialized_pair(predecessor, output[phase-169:phase-166])
            assert early == state[phase-168:phase-166]
            partial = inverse_twist(predecessor[2], output[phase-167]) & 0x7FFFFFFF
            assert partial == state[phase-166] & 0x7FFFFFFF
            assert gate(phase, early, state[phase-1:phase+3], partial, key_count) == 'match'
            count += 1
    print('SYNTHETIC_PASS', count)


def main(zip_path):
    synthetic_controls()
    earlier, partial = source_window(zip_path)
    print('SOURCE_EARLIER', ' '.join(f'{v:08X}' for v in earlier))
    print('SOURCE_NEXT_LOW31', f'{partial:08X}')
    lengths = (1, 2, 3, 4, 6, 7, 8, 12, 14, 21, 24, 28, 42, 56, 84, 167, 168)
    for n in lengths:
        outcomes = [gate(phase, earlier, LATE, partial, n) for phase in range(396, 622)]
        assert all(outcome in ('mismatch', 'quartet_conflict') for outcome in outcomes)
        print('ORIGINAL_REJECT', n, len(outcomes), 'phases')
    print('SOURCE_MODEL_SEED_CLASSES_REJECTED', len(lengths))
    print('K04_K08_MISSING; no original acceptance tested')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python k04_ax_seed_divisor_gate.py case.zip')
    main(sys.argv[1])
