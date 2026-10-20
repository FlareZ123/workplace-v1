"""Check source-labeled administrative fields as conditional MT future-donor pairs.

The four source-predicted masks and constants are from the previously published
p955 printer-only future-state equations. The selected printer coupon and
original acceptance commitments are never read.
"""

import argparse
import hashlib
import json
import re
import struct
import zipfile
import zlib
from pathlib import Path

SOURCE_ZIP_SHA256 = "a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec"
PREDICTIONS = {
    "1412/1866": (0xFFFFFFFF, 0xBD2761F8),
    "1185/1412": (0xBFFFFFFF, 0x359EC0C7),
    "1185/1866": (0xBFFFFFFF, 0x88B9A13F),
    "1411/1865": (0x9FFFFFFF, 0x0CDE27B9),
}


def undo_rshift(value, shift):
    x = value
    for _ in range(6):
        x = value ^ (x >> shift)
    return x & 0xFFFFFFFF


def undo_lshift(value, shift, mask):
    x = value
    for _ in range(6):
        x = value ^ ((x << shift) & mask)
    return x & 0xFFFFFFFF


def untemper(value):
    value = undo_rshift(value, 18)
    value = undo_lshift(value, 15, 0xEFC60000)
    value = undo_lshift(value, 7, 0x9D2C5680)
    return undo_rshift(value, 11)


def temper(value):
    value ^= value >> 11
    value ^= (value << 7) & 0x9D2C5680
    value ^= (value << 15) & 0xEFC60000
    return (value ^ (value >> 18)) & 0xFFFFFFFF


def carrier_views(zf):
    views = []
    def add(label, raw):
        assert len(raw) == 4
        for order in ('little', 'big'):
            views.append((label, order, untemper(int.from_bytes(raw, order))))

    for member in ('03.eml', '06.eml'):
        path = f'evidence/mail/{member}'
        content = zf.read(path).decode('utf-8')
        for group, token in re.findall(r'WN-14 / group ([ABCD]) / ([0-9A-F]{8})', content):
            add(f'K01/{member}/{group}', bytes.fromhex(token))

    for line, content in enumerate(zf.read('evidence/maintenance/seal-receipts.jsonl').splitlines(), 1):
        token = json.loads(content)['serial'].split('-')[-1]
        add(f'seal/{line}', bytes.fromhex(token))

    routing = json.loads(zf.read('evidence/recovery-routing.json'))
    for field, value in (('K04/mask', routing['K04']['masked_component']),
                         ('K08/nonce', routing['K08']['desk_nonce'])):
        raw = bytes.fromhex(value)
        for i in range(4):
            add(f'{field}/{i}', raw[4 * i:4 * i + 4])

    raw = zf.read('evidence/recorder/trip-recorder.raw')
    assert raw[:8] == b'TRP2DUMP'
    version, stride, count = struct.unpack_from('<HHI', raw, 8)
    assert (version, stride, count) == (2, 24, 88)
    for i in range(count):
        record = raw[16 + i * stride:16 + (i + 1) * stride]
        assert len(record) == stride
        actual_crc = zlib.crc32(record[:20]) & 0xFFFFFFFF
        saved_crc = struct.unpack_from('<I', record, 20)[0]
        add(f'TRP2/{i}/crc_{actual_crc == saved_crc}', record[12:16])

    text = zf.read('evidence/procedures/RC-17-scans.txt').decode('utf-8')
    for i, token in enumerate(re.findall(r'Footer control strip:\s*([0-9A-F]{8})', text)):
        add(f'RC17/{i}', bytes.fromhex(token))
    assert len(views) == 312 and len({label for label, _, _ in views}) == 156
    return views


def scan(views):
    for name, (mask, constant) in PREDICTIONS.items():
        seen = {}
        matches = []
        for label, order, word in views:
            expected = (word ^ constant) & mask
            for other_label, other_order in seen.get(expected, ()):
                if label != other_label:
                    matches.append((other_label, other_order, label, order))
            seen.setdefault(word & mask, []).append((label, order))
        print(f'{name}: matches={len(matches)}')
        for item in matches:
            print(' ', item)
    print('Conditional pairwise scan complete; no historical producer attribution implied.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original_zip', type=Path)
    args = parser.parse_args()
    assert hashlib.sha256(args.original_zip.read_bytes()).hexdigest() == SOURCE_ZIP_SHA256
    for value in (0, 1, 0xFFFFFFFF, 0x12345678, 0xDEADBEEF):
        assert untemper(temper(value)) == value
    with zipfile.ZipFile(args.original_zip) as zf:
        scan(carrier_views(zf))


if __name__ == '__main__':
    main()
