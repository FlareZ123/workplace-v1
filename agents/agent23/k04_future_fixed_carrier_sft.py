"""Find independent original future-state donor anchors in H-17 external carriers.

Original p955 source-consistent MT model only. Source files and commitments unchanged;
selected printer row129, XOR mask, original K04/K08 commitments and verifier unused.
"""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import random
import runpy
import sys
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'resources'
TRANSFER_SHA = '32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf'
FUTURE_EXACT = {1413: 0x758243A9, 1414: 0xC4CA6CC8, 1415: 0xBAE2035E,
                1418: 0x9CC93D80, 1419: 0x300760A8, 1420: 0x7606C13B,
                1421: 0xD4A5BA9E, 1422: 0x3C241095}


def temper(w):
    w ^= w >> 11
    w ^= (w << 7) & 0x9D2C5680
    w ^= (w << 15) & 0xEFC60000
    return (w ^ (w >> 18)) & 0xFFFFFFFF


def fixed_word(basis, expression, infer_bit):
    mask = known = 0
    for i, vector in enumerate(expression):
        value = infer_bit(basis, vector)
        if value is not None:
            mask |= 1 << i
            known |= value << i
    return mask, known


def examine(source):
    source_tools = runpy.run_path(str(ROOT / 'agents/agent29/k04_future_donor_sft.py'))
    original_values, recorder, procedure = source_tools['original_source'](source)
    original_controls = source_tools['external_controls'](recorder, procedure)
    assert len(original_controls) == 200
    with (ROOT / 'results/h17-k04-source-consistent-index955.json').open() as f:
        fixture = json.load(f)
    starts = fixture['row_starts']
    assert len(starts) == 133 and starts[129] == 955
    assert fixture['source_spool_sha256'] == source_tools['SPOOL_SHA']
    expressions = source_tools['symbolic_mt'](2250)
    basis = {}
    for row, start in enumerate(starts):
        if row == 129:
            continue
        for offset in range(4):
            for bit, vector in enumerate(expressions[start + offset]):
                source_tools['add_equation'](basis, vector, (original_values[row][offset] >> bit) & 1)
    assert len(basis) == 15305, len(basis)

    full = {}
    partial = {}
    for t in range(971, 2251):
        mask, known = fixed_word(basis, expressions[t], source_tools['infer_bit'])
        if mask == 0xFFFFFFFF:
            full[t] = known
        elif mask.bit_count() >= 24:
            partial[t] = (mask, known)
    assert len(full) == 318 and len(partial) == 178, (len(full), len(partial))
    for t, expected in FUTURE_EXACT.items():
        assert temper(full[t]) == expected, (t, temper(full[t]), expected)

    # A new raw four-byte external field is usable as a candidate future anchor
    # only if it agrees with a spool-fixed untempered word at that exact index.
    value_index = defaultdict(list)
    for t, known in full.items():
        value_index[known].append(t)
    exact_hits = [(label, endian, t)
                  for _, label, endian, value in original_controls
                  for t in value_index.get(value, ())]
    masked_hits = [(label, endian, t, f'{mask:08X}')
                   for _, label, endian, value in original_controls
                   for t, (mask, known) in partial.items() if (value & mask) == known]
    print('P955_ORIGINAL_SOURCE_RANK', len(basis), 'FULLY_FIXED_FUTURE_WORDS', len(full),
          'PARTIALLY_FIXED_GE24_BITS', len(partial))
    print('TRP2_AND_RC17_FULL32_DIRECT_COPY_HITS', len(exact_hits), exact_hits[:10])
    print('TRP2_AND_RC17_GE24BIT_DIRECT_COPY_HITS', len(masked_hits), masked_hits[:10])
    assert not exact_hits and not masked_hits

    # AX has an independently calibrated, byte-swapped upper16 representation.
    # Enumerate source-prescribed (seq,attempt) checkpoint order, both views.
    transfer = source.read('evidence/transfers/transfer-audit.jsonl')
    assert hashlib.sha256(transfer).hexdigest() == TRANSFER_SHA
    chunks = [json.loads(line) for line in transfer.splitlines()]
    chunks = [item for item in chunks if item['kind'] == 'CHUNK']
    assert len(chunks) == 64
    future_high = defaultdict(list)
    for t, u in full.items():
        future_high[temper(u) >> 16].append(t)
    ax_hits = []
    for transfer_name in ('AX-7778', 'AX-7781', 'AX-7782', 'AX-7783'):
        rows = sorted((item for item in chunks if item['transfer'] == transfer_name),
                      key=lambda item: (item['seq'], item['attempt']))
        assert len(rows) == 16
        for orientation in ('native', 'swapped'):
            values = [int(item['checkpoint'], 16) for item in rows]
            if orientation == 'swapped':
                values = [((v & 255) << 8) | (v >> 8) for v in values]
            for offset, value in enumerate(values):
                for t in future_high.get(value, ()):
                    adjacent = []
                    for step in (-2, -1, 1, 2):
                        if 0 <= offset + step < 16 and t + step in full:
                            predicted = temper(full[t + step]) >> 16
                            adjacent.append((step, values[offset + step] == predicted))
                    ax_hits.append((transfer_name, orientation, offset, t, adjacent))
    print('AX_CALIBRATED_HIGH16_FUTURE_ANCHOR_HITS', len(ax_hits), ax_hits)
    assert ax_hits == [
        ('AX-7781', 'swapped', 11, 1025, [(1, False)]),
        ('AX-7783', 'swapped', 12, 1383, [(-1, False), (2, False)]),
    ], ax_hits
    assert not any(hit[3] in range(t+1, t+16)
                   for hit in ax_hits for t in (1185, 1411, 1412, 1865, 1866, 1974))

    # Synthetic positive control for exact 32-bit carrier indexing and untempering.
    assert 1413 in value_index[source_tools['untemper'](FUTURE_EXACT[1413])]
    rng = random.Random(8131)
    for _ in range(100):
        w = rng.getrandbits(32)
        assert temper(source_tools['untemper'](w)) == w
    print('SYNTHETIC_INSERTED_FULLWORD_AND_100_UNTEMPER_CONTROLS_PASS')
    print('ORIGINAL_TARGET_INFORMATION_GAIN', 0, 'K04_K08_ACCEPTANCE_NOT_READ')


class FolderSource:
    def read(self, name):
        return (SRC / name).read_bytes()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with ZipFile(sys.argv[1]) as archive:
            examine(archive)
    else:
        examine(FolderSource())
