"""H-17 source-only K04: detect independent MT state carriers in transfer checkpoints.

Reads the original 43-member case ZIP. Selected printer row129, REC8 masks,
acceptance commitments, and verification code are never examined.
"""
import hashlib
import json
import random
import re
import sys
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

SPOOL_SHA256 = '7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
TRANSFER_SHA256 = '32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf'
MASK = (1 << 32) - 1


def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9D2C5680
    x ^= (x << 15) & 0xEFC60000
    return (x ^ (x >> 18)) & MASK


def untemper(x):
    for _ in range(5):
        x ^= x >> 18
    for shift, mask in ((15, 0xEFC60000), (7, 0x9D2C5680)):
        y = x
        for _ in range(6):
            y = x ^ ((y << shift) & mask)
        x = y
    y = x
    for _ in range(5):
        y = x ^ (y >> 11)
    return y & MASK


def ancestor_low31(middle, end):
    mixed = middle ^ end
    if mixed & 0x80000000:
        mixed ^= 0x9908B0DF
    return ((mixed << 1) | ((middle ^ end) >> 31)) & 0x7FFFFFFF


def high16_options(low31):
    return (temper(low31) >> 16, temper(low31 | 0x80000000) >> 16)


def synth_control():
    rng = random.Random(314159)
    words = [untemper(rng.getrandbits(32)) for _ in range(700)]
    for i in (0, 12, 74):
        assert ancestor_low31(words[i + 397], words[i + 624]) == words[i + 1] & 0x7FFFFFFF
        assert temper(words[i + 1]) >> 16 in high16_options(words[i + 1] & 0x7FFFFFFF)


def read_sources(path):
    with ZipFile(path) as archive:
        spool = archive.read('evidence/print/spool-reconstruction.log')
        transfers = archive.read('evidence/transfers/transfer-audit.jsonl')
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA256
    assert hashlib.sha256(transfers).hexdigest() == TRANSFER_SHA256
    payloads = [bytes.fromhex(m.group(1)) for line in spool.decode().splitlines()
                if (m := re.search(r'PAYLOAD=([0-9A-F]{32})', line))]
    assert len(payloads) == 133
    payloads[129] = None
    states = [None if item is None else [untemper(int.from_bytes(item[j:j + 4], 'little'))
                                          for j in (0, 4, 8, 12)] for item in payloads]
    runs = defaultdict(list)
    for line in transfers.decode().splitlines():
        obj = json.loads(line)
        if obj.get('kind') == 'CHUNK':
            runs[obj['transfer']].append(obj)
    for transfer in runs:
        runs[transfer].sort(key=lambda item: (int(item['seq']), int(item['attempt'])))
    return states, runs


def find_fingerprints(states, runs, width):
    assert width in (3, 4)
    matches = []
    for a, first in enumerate(states):
        if first is None:
            continue
        for b in range(a + 1, len(states)):
            last = states[b]
            if last is None:
                continue
            for i in range(5 - width):
                for j in range(5 - width):
                    predecessor = [ancestor_low31(first[i + k], last[j + k]) for k in range(width)]
                    options = [high16_options(word) for word in predecessor]
                    for transfer, records in runs.items():
                        for start in range(len(records) - width + 1):
                            window = records[start:start + width]
                            for byteorder in ('little', 'big'):
                                values = [int.from_bytes(bytes.fromhex(record['checkpoint']), byteorder)
                                          for record in window]
                                if all(value in opt for value, opt in zip(values, options)):
                                    full = [word | (0x80000000 if opt[0] != value else 0)
                                            for word, opt, value in zip(predecessor, options, values)]
                                    assert all(temper(word) >> 16 == value
                                               for word, value in zip(full, values))
                                    matches.append({
                                        'printer_pair': [a, b], 'word_offsets': [i, j],
                                        'printer_start_gap_if_shared': 227 + i - j,
                                        'transfer': transfer, 'transfer_run_start': start,
                                        'byteorder': byteorder,
                                        'source_checkpoints': [(int(x['seq']), int(x['attempt']),
                                                                x['checkpoint']) for x in window],
                                        'inferred_ancestor_states': [f'{x:08X}' for x in full],
                                    })
    return matches


def main(path):
    synth_control()
    states, runs = read_sources(path)
    triples = find_fingerprints(states, runs, 3)
    quads = find_fingerprints(states, runs, 4)
    assert len(quads) == 1 and quads[0]['printer_pair'] == [34, 64]
    assert quads[0]['transfer'] == 'AX-7778' and quads[0]['transfer_run_start'] == 11
    head = [hit for hit in triples if hit['printer_pair'] == [33, 63]]
    assert len(head) == 1 and head[0]['transfer_run_start'] == 5
    assert all(hit['byteorder'] == 'little' for hit in head + quads)
    print('selected_ACK_row129_excluded', True)
    print('three_word_exact_matches', len(triples))
    print('four_word_exact_matches', len(quads))
    print('independent_AX7778_run_pos5_to7', head[0])
    print('independent_AX7778_run_pos11_to14', quads[0])
    print('conditional_printer_row34_minus_33_draws', 11 - 5)
    print('conditional_printer_row64_minus_63_draws', 11 - 5 + 227 - 226)
    print('K04_K08_NOT_RECOVERED')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
