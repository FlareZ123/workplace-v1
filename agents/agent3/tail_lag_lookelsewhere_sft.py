"""Read-only original-source calibration of the late DEST-lag bit-pair cue."""
import hashlib
import re
from collections import Counter
from pathlib import Path

SPOOL = Path(__file__).resolve().parents[2] / 'resources' / 'evidence' / 'print' / 'spool-reconstruction.log'
PIN = '7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
DEST = {'store': 0, 'desk': 1, 'bench': 2}


def count_matches(rows, predecessors):
    payloads = [bytes.fromhex(rows[i]['PAYLOAD']) for i in predecessors]
    codes = [DEST[rows[i + 1]['DEST']] for i in predecessors]
    matches = []
    for word in range(4):
        for shift in range(31):
            if all(((int.from_bytes(payload[4 * word:4 * word + 4], 'little') >> shift) & 3) == code
                   for payload, code in zip(payloads, codes)):
                matches.append((word, shift))
    return matches


def main():
    raw = SPOOL.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PIN, 'Unexpected spool bytes'
    rows = [dict(re.findall(r'(CLASS|PAYLOAD|DEST)=([^ ]+)', line))
            for line in raw.decode('utf-8').splitlines() if 'PAYLOAD=' in line]
    assert len(rows) == 133
    assert all({'CLASS', 'PAYLOAD', 'DEST'} <= row.keys() for row in rows)

    # The target row129 payload is never read by either test. Its DEST is
    # independently recorded and is allowed as a successor label only.
    late = (127, 128, 130, 131)
    late_matches = count_matches(rows, late)
    print('late controls indices:', late)
    print('exact four-comparison predictor matches:', late_matches)
    assert late_matches == [(1, 20), (3, 30)]

    # Match the noncontiguous shape (i,i+1,i+3,i+4), skipping the hypothetical
    # disputed middle row; both predictors and successor DEST stay in r0..r127.
    distribution = Counter()
    examples = []
    for i in range(123):
        matches = count_matches(rows, (i, i + 1, i + 3, i + 4))
        distribution[len(matches)] += 1
        if len(matches) >= 2:
            examples.append(i)
    print('ordinary same-gap 123 windows distribution:', dict(sorted(distribution.items())))
    print('ordinary windows with >=2 exact predictors:', len(examples), '/123', examples)
    assert distribution == Counter({0: 69, 1: 40, 2: 12, 3: 2})
    assert len(examples) == 14
    print('Scope: descriptive look-elsewhere calibration, overlapping ordinary windows and')
    print('nonexchangeable late cohort; NO authenticated selected coupon bits.')


if __name__ == '__main__':
    main()
