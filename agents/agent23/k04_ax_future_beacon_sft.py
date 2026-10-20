"""Source-pinned, read-only AX upper16 future-beacon check for original H-17 ZIP.

Tests a *conditional* MT19937 index955 model, not a documented historical producer.
The original selected printer row129, mask, acceptance and K08 text are unused.
"""
import hashlib
import json
import random
import re
import struct
import sys
import zipfile
from pathlib import Path

TRANSFER_SHA = '32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf'
SPOOL_SHA = '7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
# The original-spool p955 source-only GF(2) forecast in Agent29's future suffix report.
FUTURE_BEACON = (0x9CC93D80, 0x300760A8, 0x7606C13B, 0xD4A5BA9E, 0x3C241095)
FUTURE_BACKSTOP = (0x758243A9, 0xC4CA6CC8, 0xBAE2035E) # X1413..X1415
BEACON16 = tuple(value >> 16 for value in FUTURE_BEACON)
BACKSTOP16 = tuple(value >> 16 for value in FUTURE_BACKSTOP)


def temper(w):
    w ^= w >> 11
    w ^= (w << 7) & 0x9D2C5680
    w ^= (w << 15) & 0xEFC60000
    return (w ^ (w >> 18)) & 0xFFFFFFFF


def untemper(w):
    original = w
    for shift in (18,):
        for _ in range(6):
            w = original ^ (w >> shift)
    original = w
    for shift, mask in ((15, 0xEFC60000), (7, 0x9D2C5680)):
        w = original
        for _ in range(8):
            w = original ^ ((w << shift) & mask)
        original = w
    w = original
    for _ in range(6):
        w = original ^ (w >> 11)
    return w & 0xFFFFFFFF


def windows(values, needle):
    return [i for i in range(len(values) - len(needle) + 1)
            if tuple(values[i:i+len(needle)]) == tuple(needle)]


def swap16(v):
    return ((v & 0xFF) << 8) | (v >> 8)


def synthetic_control():
    rng = random.Random(20261020)
    generated = [rng.getrandbits(32) for _ in range(1424)]
    segment = [swap16(w >> 16) for w in generated[1408:1424]]
    inferred = [swap16(w) for w in segment]
    assert windows(inferred, tuple(w >> 16 for w in generated[1418:1423])) == [10]
    assert inferred[4] == (generated[1412] >> 16)
    for _ in range(100):
        sample = rng.getrandbits(32)
        assert untemper(temper(sample)) == sample
        assert temper(untemper(sample)) == sample
    # Temper is GF(2)-linear. A donor halfword transfers directly to a target
    # output halfword via the published source-fixed X958 xor X1412 relation.
    delta = 0x24D1E0F2
    for _ in range(100):
        a = rng.getrandbits(32)
        assert (temper(a ^ delta) >> 16) == ((temper(a) >> 16) ^ (temper(delta) >> 16))
    print('SYNTHETIC_BEACON_AND_DONOR_HIGH16_PASS', 'beacon_offset=10', 'donor_position=4')


def original_test(zip_path=None):
    if zip_path is not None:
        with zipfile.ZipFile(zip_path) as archive:
            transfer = archive.read('evidence/transfers/transfer-audit.jsonl')
            spool = archive.read('evidence/print/spool-reconstruction.log')
    else:
        root = Path(__file__).resolve().parents[2] / 'resources/evidence'
        transfer = (root / 'transfers/transfer-audit.jsonl').read_bytes()
        spool = (root / 'print/spool-reconstruction.log').read_bytes()
    assert hashlib.sha256(transfer).hexdigest() == TRANSFER_SHA
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    rows = [json.loads(line) for line in transfer.splitlines()]
    chunks = [r for r in rows if r['kind'] == 'CHUNK']
    assert len(chunks) == 64
    groups = {name: sorted((r for r in chunks if r['transfer'] == name),
                           key=lambda r: (r['seq'], r['attempt']))
              for name in ('AX-7778', 'AX-7781', 'AX-7782', 'AX-7783')}
    assert all(len(group) == 16 for group in groups.values())

    # Independent original-data positive lane calibration, originally Agent9:
    # known AX-7778 swapped 16-bit checkpoints match printer row34/64 inverse twist.
    payload = re.findall(rb'PAYLOAD=([A-F0-9]{32})', spool)
    assert len(payload) == 133
    left = [untemper(w) for w in struct.unpack('<4I', bytes.fromhex(payload[34].decode()))]
    right = [untemper(w) for w in struct.unpack('<4I', bytes.fromhex(payload[64].decode()))]
    for k, record in enumerate(groups['AX-7778'][11:15]):
        diff = left[k] ^ right[k]
        predecessor_low31 = (((diff ^ (0x9908B0DF if diff & 0x80000000 else 0)) << 1)
                             | (diff >> 31)) & 0x7FFFFFFF
        options = {temper(predecessor_low31) >> 16, temper(predecessor_low31 | 0x80000000) >> 16}
        assert swap16(int(record['checkpoint'], 16)) in options
    print('ORIGINAL_AX7778_SWAPPED_UPPER16_CALIBRATION_PASS 4/4')

    total = 0
    matches = []
    for name, records in sorted(groups.items()):
        for view in ('native', 'swapped'):
            values = [int(r['checkpoint'], 16) for r in records]
            if view == 'swapped':
                values = [swap16(v) for v in values]
            offsets = windows(values, BEACON16)
            total += len(values) - len(BEACON16) + 1
            for offset in offsets:
                backstop = offset >= 5 and tuple(values[offset-5:offset-2]) == BACKSTOP16
                donor = values[offset-6] if offset >= 6 else None
                matches.append((name, view, offset, backstop, donor))
            print(name, view, 'five_consecutive_high16_beacon_matches', offsets)
    assert total == 96, total
    print('SOURCE_WINDOWS', total, 'BEACON_HITS', len(matches), 'HIT_DETAILS', matches)
    print('CONDITIONAL_K04_SELECTED_PAYLOAD_BITS_RECOVERED', 0 if not matches else 'review matched index/provenance')
    print('NO_K04_OR_K08_ACCEPTANCE_HASH_READ')


if __name__ == '__main__':
    synthetic_control()
    original_test(sys.argv[1] if len(sys.argv) > 1 else None)
